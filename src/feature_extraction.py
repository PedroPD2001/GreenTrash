"""
Módulo de extração de features visuais e textuais para classificação de resíduos.
Implementa extração de características HSV, LBP, GLCM, Canny, Hu Moments e text scores.
"""

import cv2
import numpy as np
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
from skimage import img_as_ubyte


class FeatureExtractor:
    """Extrai features visuais e textuais de imagens e textos."""
    
    # Dicionário de termos associados a cada classe
    KEYWORDS = {
        'Orgânico': [
            'alimento', 'comida', 'fruta', 'legume', 'verdura', 'casca',
            'resto', 'compostagem', 'folha', 'galho', 'planta', 'vegetal',
            'banana', 'maçã', 'tomate', 'batata', 'cenoura', 'alface',
            'laranja', 'restos alimentares', 'orgânico', 'biodegradável'
        ],
        'Reciclável': [
            'papel', 'papelão', 'plástico', 'garrafa', 'pet', 'metal',
            'alumínio', 'lata', 'vidro', 'caixa', 'embalagem', 'revista',
            'jornal', 'cartolina', 'pote', 'sacola', 'reciclagem', 'reciclável',
            'tetra pak', 'aço', 'ferro', 'cobre', 'papelão ondulado'
        ],
        'Rejeito': [
            'papel higiênico', 'absorvente', 'fralda', 'guardanapo sujo',
            'adesivo', 'etiqueta', 'papel plastificado', 'papel metalizado',
            'cerâmica', 'porcelana', 'espelho', 'vidro temperado', 'cabo',
            'esponja', 'bituca', 'cigarro', 'rejeito', 'não reciclável'
        ],
        'Perigoso': [
            'bateria', 'pilha', 'tinta', 'solvente', 'veneno', 'inseticida',
            'pesticida', 'remédio', 'medicamento', 'lâmpada', 'fluorescente',
            'termômetro', 'mercúrio', 'óleo', 'graxa', 'aerosol', 'spray',
            'tóxico', 'corrosivo', 'inflamável', 'químico', 'perigoso',
            'hospitalar', 'agulha', 'seringa', 'eletrônico', 'celular'
        ]
    }
    
    def __init__(self):
        self.lbp_radius = 3
        self.lbp_n_points = 24
        
    def extract_visual_features(self, image):
        """
        Extrai features visuais de uma imagem.
        
        Args:
            image: Imagem numpy array (BGR)
            
        Returns:
            numpy array com todas as features visuais concatenadas
        """
        # Validar imagem
        if image is None or image.size == 0:
            raise ValueError("Imagem inválida ou vazia")
        
        # Redimensionar para tamanho padrão
        image_resized = cv2.resize(image, (256, 256))
        
        # Converter para HSV
        hsv = cv2.cvtColor(image_resized, cv2.COLOR_BGR2HSV)
        
        # 1. Histograma HSV (30 bins por canal = 90 features)
        hist_features = self._extract_hsv_histogram(hsv)
        
        # 2. Estatísticas HSV (média e std de cada canal = 6 features)
        stats_features = self._extract_hsv_stats(hsv)
        
        # 3. LBP (Local Binary Pattern) - 10 bins
        lbp_features = self._extract_lbp(image_resized)
        
        # 4. GLCM (Gray Level Co-occurrence Matrix) - 4 features
        glcm_features = self._extract_glcm(image_resized)
        
        # 5. Canny edges - 1 feature (densidade de bordas)
        canny_features = self._extract_canny(image_resized)
        
        # 6. Hu Moments - 7 features
        hu_features = self._extract_hu_moments(image_resized)
        
        # Concatenar todas as features
        all_features = np.concatenate([
            hist_features,
            stats_features,
            lbp_features,
            glcm_features,
            canny_features,
            hu_features
        ])
        
        return all_features
    
    def _extract_hsv_histogram(self, hsv):
        """Extrai histograma HSV normalizado."""
        hist_h = cv2.calcHist([hsv], [0], None, [30], [0, 180])
        hist_s = cv2.calcHist([hsv], [1], None, [30], [0, 256])
        hist_v = cv2.calcHist([hsv], [2], None, [30], [0, 256])
        
        # Normalizar
        hist_h = hist_h.flatten() / hist_h.sum()
        hist_s = hist_s.flatten() / hist_s.sum()
        hist_v = hist_v.flatten() / hist_v.sum()
        
        return np.concatenate([hist_h, hist_s, hist_v])
    
    def _extract_hsv_stats(self, hsv):
        """Extrai estatísticas (média e desvio padrão) de cada canal HSV."""
        stats = []
        for i in range(3):
            channel = hsv[:, :, i]
            stats.append(np.mean(channel))
            stats.append(np.std(channel))
        return np.array(stats)
    
    def _extract_lbp(self, image):
        """Extrai features LBP (Local Binary Pattern)."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lbp = local_binary_pattern(gray, self.lbp_n_points, self.lbp_radius, method='uniform')
        
        # Histograma do LBP
        n_bins = 10
        hist, _ = np.histogram(lbp.ravel(), bins=n_bins, range=(0, n_bins), density=True)
        return hist
    
    def _extract_glcm(self, image):
        """Extrai features GLCM (Gray Level Co-occurrence Matrix)."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Reduzir níveis de cinza para acelerar computação
        gray = img_as_ubyte(gray // 32)
        
        # Calcular GLCM
        distances = [1]
        angles = [0]
        glcm = graycomatrix(gray, distances=distances, angles=angles, 
                           levels=8, symmetric=True, normed=True)
        
        # Extrair propriedades
        contrast = graycoprops(glcm, 'contrast')[0, 0]
        dissimilarity = graycoprops(glcm, 'dissimilarity')[0, 0]
        homogeneity = graycoprops(glcm, 'homogeneity')[0, 0]
        energy = graycoprops(glcm, 'energy')[0, 0]
        
        return np.array([contrast, dissimilarity, homogeneity, energy])
    
    def _extract_canny(self, image):
        """Extrai densidade de bordas usando Canny."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        # Densidade de bordas (proporção de pixels de borda)
        edge_density = np.sum(edges > 0) / edges.size
        return np.array([edge_density])
    
    def _extract_hu_moments(self, image):
        """Extrai Hu Moments invariantes."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        moments = cv2.moments(gray)
        hu_moments = cv2.HuMoments(moments).flatten()
        
        # Aplicar transformação logarítmica para estabilizar valores
        hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-10)
        
        return hu_moments
    
    def extract_text_features(self, text):
        """
        Extrai features textuais baseadas em keywords.
        
        Args:
            text: String com descrição do resíduo
            
        Returns:
            numpy array com 4 valores (score para cada classe)
        """
        text_lower = text.lower()
        scores = []
        
        for class_name in ['Orgânico', 'Reciclável', 'Rejeito', 'Perigoso']:
            keywords = self.KEYWORDS[class_name]
            score = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            scores.append(score)
        
        # Normalizar scores
        total = sum(scores)
        if total > 0:
            scores = [s / total for s in scores]
        
        return np.array(scores)
    
    def extract_combined_features(self, image=None, text=""):
        """
        Extrai features combinadas (visuais + textuais).
        
        Args:
            image: Imagem numpy array (BGR) ou None
            text: String com descrição ou ""
            
        Returns:
            numpy array com todas as features concatenadas
        """
        features = []
        
        # Features visuais
        if image is not None:
            visual_features = self.extract_visual_features(image)
            features.append(visual_features)
        else:
            # Se não houver imagem, preencher com zeros
            features.append(np.zeros(118))  # Total de features visuais
        
        # Features textuais
        text_features = self.extract_text_features(text)
        features.append(text_features)
        
        return np.concatenate(features)

