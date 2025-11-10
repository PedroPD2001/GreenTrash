"""
Módulo para geração de dados sintéticos de treinamento.
Cria dataset de exemplo para treinar o classificador.
"""

import numpy as np
from src.feature_extraction import FeatureExtractor


class DataGenerator:
    """Gera dados sintéticos para treinamento do classificador."""
    
    def __init__(self):
        self.extractor = FeatureExtractor()
        self.classes = ['Orgânico', 'Reciclável', 'Rejeito', 'Perigoso']
    
    def generate_training_data(self, samples_per_class=100):
        """
        Gera dados sintéticos de treinamento.
        
        Args:
            samples_per_class: Número de amostras por classe
            
        Returns:
            tuple (X, y) com features e labels
        """
        X = []
        y = []
        
        for class_idx, class_name in enumerate(self.classes):
            print(f"Gerando {samples_per_class} amostras para {class_name}...")
            
            for _ in range(samples_per_class):
                # Gerar imagem sintética característica da classe
                synthetic_image = self._generate_synthetic_image(class_name)
                
                # Gerar texto sintético da classe
                synthetic_text = self._generate_synthetic_text(class_name)
                
                # Extrair features
                features = self.extractor.extract_combined_features(
                    synthetic_image, 
                    synthetic_text
                )
                
                X.append(features)
                y.append(class_name)
        
        return np.array(X), np.array(y)
    
    def _generate_synthetic_image(self, class_name):
        """
        Gera imagem sintética característica de cada classe.
        
        Args:
            class_name: Nome da classe
            
        Returns:
            numpy array representando imagem BGR
        """
        image = np.zeros((256, 256, 3), dtype=np.uint8)
        
        if class_name == 'Orgânico':
            # Tons de verde, marrom e amarelo
            colors = [
                (34, 139, 34),   # Verde floresta
                (0, 128, 0),     # Verde
                (0, 100, 0),     # Verde escuro
                (19, 69, 139),   # Marrom
                (0, 255, 127),   # Verde primavera
            ]
            self._fill_with_patches(image, colors)
            
        elif class_name == 'Reciclável':
            # Tons de azul, cinza e transparente (branco)
            colors = [
                (255, 165, 0),   # Azul
                (255, 144, 30),  # Azul dodger
                (255, 255, 255), # Branco
                (192, 192, 192), # Cinza claro
                (128, 128, 128), # Cinza
            ]
            self._fill_with_patches(image, colors)
            
        elif class_name == 'Rejeito':
            # Tons de cinza e preto
            colors = [
                (64, 64, 64),    # Cinza escuro
                (128, 128, 128), # Cinza médio
                (96, 96, 96),    # Cinza
                (0, 0, 0),       # Preto
                (160, 160, 160), # Cinza claro
            ]
            self._fill_with_patches(image, colors)
            
        elif class_name == 'Perigoso':
            # Tons de vermelho, amarelo (perigo) e laranja
            colors = [
                (0, 0, 255),     # Vermelho
                (0, 69, 255),    # Vermelho alaranjado
                (0, 140, 255),   # Laranja escuro
                (0, 215, 255),   # Ouro
                (0, 255, 255),   # Amarelo
            ]
            self._fill_with_patches(image, colors)
        
        # Adicionar ruído
        noise = np.random.randint(0, 30, image.shape, dtype=np.uint8)
        image = np.clip(image.astype(np.int16) + noise - 15, 0, 255).astype(np.uint8)
        
        return image
    
    def _fill_with_patches(self, image, colors):
        """Preenche imagem com patches de cores variadas."""
        h, w = image.shape[:2]
        
        # Criar 4-8 patches aleatórios
        n_patches = np.random.randint(4, 9)
        
        for _ in range(n_patches):
            color = colors[np.random.randint(0, len(colors))]
            
            # Posição e tamanho aleatórios
            x1 = np.random.randint(0, w // 2)
            y1 = np.random.randint(0, h // 2)
            x2 = np.random.randint(w // 2, w)
            y2 = np.random.randint(h // 2, h)
            
            image[y1:y2, x1:x2] = color
    
    def _generate_synthetic_text(self, class_name):
        """
        Gera texto sintético com keywords da classe.
        
        Args:
            class_name: Nome da classe
            
        Returns:
            String com descrição sintética
        """
        keywords = self.extractor.KEYWORDS[class_name]
        
        # Selecionar 2-4 keywords aleatórias
        n_keywords = np.random.randint(2, 5)
        selected = np.random.choice(keywords, size=min(n_keywords, len(keywords)), replace=False)
        
        # Adicionar algumas keywords de outras classes (ruído) - 20% de chance
        if np.random.random() < 0.2:
            other_classes = [c for c in self.classes if c != class_name]
            other_class = np.random.choice(other_classes)
            other_keywords = self.extractor.KEYWORDS[other_class]
            noise_keyword = np.random.choice(other_keywords)
            selected = np.append(selected, noise_keyword)
        
        return ' '.join(selected)

