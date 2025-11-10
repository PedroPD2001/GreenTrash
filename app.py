"""
Aplicação Streamlit para classificação de resíduos sólidos.
Interface com páginas: Introdução e Classificar.
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier


# Configuração da página
st.set_page_config(
    page_title="GreenTrash - Classificação Inteligente",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E7D32;
        font-weight: bold;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #388E3C;
        font-weight: bold;
        margin-top: 1.5rem;
    }
    .info-box {
        background-color: #E8F5E9;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #FFF3E0;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF9800;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #FFEBEE;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #F44336;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #F5F5F5;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #45A049;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa variáveis de sessão."""
    if 'extractor' not in st.session_state:
        st.session_state.extractor = FeatureExtractor()
    if 'classifier' not in st.session_state:
        st.session_state.classifier = WasteClassifier()
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None


def render_introduction():
    """Renderiza a página de Introdução."""
    st.markdown('<div class="main-header">♻️ GreenTrash - Classificação Inteligente</div>', 
                unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Sobre o projeto
    st.markdown('<div class="sub-header">📖 Sobre o Projeto</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <p>Bem-vindo ao <strong>GreenTrash</strong>! Este sistema utiliza Inteligência Artificial 
    para classificar resíduos sólidos e promover o descarte responsável, alinhado aos 
    <strong>Objetivos de Desenvolvimento Sustentável (ODS) 12 e 13</strong> da ONU:</p>
    <ul>
        <li><strong>ODS 12</strong> - Consumo e Produção Sustentáveis</li>
        <li><strong>ODS 13</strong> - Ação Contra a Mudança Global do Clima</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Como funciona
    st.markdown('<div class="sub-header">🤖 Como Funciona</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Entrada de Dados**
        - 📸 Envie uma foto do resíduo
        - ✍️ Descreva o resíduo em texto
        
        **2. Processamento**
        - Extração de características visuais (cores, texturas, formas)
        - Análise de palavras-chave descritivas
        - Priorização de features visuais sobre textuais
        """)
    
    with col2:
        st.markdown("""
        **3. Classificação**
        - 🌱 **Orgânico** - Restos de alimentos, plantas
        - ♻️ **Reciclável** - Papel, plástico, metal, vidro
        - 🗑️ **Rejeito** - Não reciclável nem compostável
        - ⚠️ **Perigoso** - Pilhas, produtos químicos, eletrônicos
        
        **4. Resultado**
        - Classificação com nível de confiança
        - Orientações de descarte apropriado
        """)
    
    # Classes de resíduos
    st.markdown('<div class="sub-header">🗂️ Classes de Resíduos</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="info-box">
        <h4>🌱 Orgânico</h4>
        <p><small>Restos de alimentos, cascas de frutas, legumes, 
        verduras, folhas, galhos, compostáveis.</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-box">
        <h4>♻️ Reciclável</h4>
        <p><small>Papel, papelão, plástico, vidro, metal, 
        embalagens limpas e secas.</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="warning-box">
        <h4>🗑️ Rejeito</h4>
        <p><small>Papel higiênico, fraldas, absorventes, 
        materiais contaminados.</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="danger-box">
        <h4>⚠️ Perigoso</h4>
        <p><small>Pilhas, baterias, lâmpadas, tintas, 
        produtos químicos, eletrônicos.</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Ética e LGPD
    st.markdown('<div class="sub-header">🔒 Ética e Privacidade (LGPD)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <p><strong>Comprometimento com a privacidade:</strong></p>
    <ul>
        <li>✓ <strong>Dados Mínimos</strong>: Coletamos apenas imagens/descrições de resíduos</li>
        <li>✓ <strong>Anonimização</strong>: Nenhuma informação pessoal é armazenada</li>
        <li>✓ <strong>Processamento Local</strong>: Análise realizada no dispositivo quando possível</li>
        <li>✓ <strong>Sem Armazenamento</strong>: Imagens não são salvas após o processamento</li>
        <li>✓ <strong>Transparência</strong>: Código aberto e auditável</li>
        <li>✓ <strong>Finalidade Específica</strong>: Uso exclusivo para classificação de resíduos</li>
    </ul>
    <p><em>Este sistema está em conformidade com a Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018).</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tecnologias
    st.markdown('<div class="sub-header">🛠️ Tecnologias Utilizadas</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Visão Computacional:**
        - OpenCV - Processamento de imagens
        - Scikit-image - Extração de features
        - Histogramas HSV
        - LBP (Local Binary Patterns)
        - GLCM (Gray Level Co-occurrence Matrix)
        """)
    
    with col2:
        st.markdown("""
        **Machine Learning:**
        - Random Forest (Scikit-learn)
        - Features visuais + textuais
        - Regra de segurança para resíduos perigosos
        - Validação com dados sintéticos
        - Fallback textual quando necessário
        """)
    
    # Instruções de uso
    st.markdown('<div class="sub-header">📝 Como Usar</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <ol>
        <li>Navegue até a página <strong>"Classificar"</strong> no menu lateral</li>
        <li>Escolha o método de entrada: foto ou texto</li>
        <li>Forneça uma descrição opcional para melhorar a precisão</li>
        <li>Clique em <strong>"Classificar Resíduo"</strong></li>
        <li>Visualize o resultado e siga as orientações de descarte</li>
    </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("💡 **Dica**: O sistema prioriza análise visual sobre descrição textual para maior acurácia!")


def render_classifier():
    """Renderiza a página de Classificação."""
    st.markdown('<div class="main-header">🔍 Classificar Resíduo</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Verificar se modelo está disponível
    if st.session_state.classifier.model is None:
        st.markdown("""
        <div class="warning-box">
        <p>⚠️ <strong>Modelo não treinado!</strong></p>
        <p>Execute o script de treinamento com imagens reais:</p>
        <code>python train_model_real.py</code>
        <p><em>O sistema funcionará em modo fallback (apenas texto).</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Seleção do método de entrada
    st.markdown('<div class="sub-header">📥 Método de Entrada</div>', unsafe_allow_html=True)
    
    input_method = st.radio(
        "Escolha como deseja fornecer informações sobre o resíduo:",
        ["📸 Imagem", "✍️ Somente Texto"],
        horizontal=True
    )
    
    image = None
    text = ""
    
    # Interface para imagem
    if input_method == "📸 Imagem":
        col1, col2 = st.columns([1, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Carregue uma imagem do resíduo",
                type=['jpg', 'jpeg', 'png', 'bmp', 'webp'],
                help="Formatos aceitos: JPG, PNG, BMP, WEBP. O sistema prioriza análise visual."
            )
            
            if uploaded_file is not None:
                try:
                    # Ler imagem
                    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                    
                    if image is not None and image.size > 0:
                        # Mostrar preview
                        st.image(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), 
                                caption="Imagem carregada", 
                                use_container_width=True)
                    else:
                        st.error("Erro ao carregar imagem. Tente outro formato.")
                        image = None
                except Exception as e:
                    st.error(f"Erro ao processar imagem: {str(e)}")
                    image = None
        
        with col2:
            text = st.text_area(
                "Descrição adicional (opcional)",
                placeholder="Ex: garrafa de plástico transparente, casca de banana, pilha AA...",
                height=150,
                help="Descrição opcional. O sistema prioriza análise visual da imagem."
            )
    
    # Interface para texto apenas
    else:
        text = st.text_area(
            "Descreva o resíduo",
            placeholder="Ex: casca de banana, garrafa pet, pilha AA, papel higiênico usado...",
            height=150,
            help="Seja específico na descrição para melhor resultado"
        )
        
        if not text:
            st.warning("⚠️ Por favor, forneça uma descrição do resíduo")
    
    st.markdown("---")
    
    # Botão de classificação
    if st.button("🔍 Classificar Resíduo", use_container_width=True):
        # Validar entrada
        if image is None and not text.strip():
            st.error("❌ Por favor, forneça uma imagem ou descrição do resíduo")
            return
        
        # Processar classificação
        with st.spinner("🔄 Analisando resíduo..."):
            try:
                # Extrair features (priorizando visuais quando há imagem)
                if image is not None:
                    # Priorizar features visuais
                    visual_features = st.session_state.extractor.extract_visual_features(image)
                    text_features = st.session_state.extractor.extract_text_features(text)
                    # Combinar: 118 visuais + 4 textuais (96.7% visual, 3.3% textual)
                    features = np.concatenate([visual_features, text_features])
                else:
                    # Apenas texto
                    visual_features = np.zeros(118)  # Features visuais vazias
                    text_features = st.session_state.extractor.extract_text_features(text)
                    features = np.concatenate([visual_features, text_features])
                
                # Classificar
                result = st.session_state.classifier.predict(features)
                
                # Armazenar resultado
                st.session_state.last_result = result
                
            except Exception as e:
                st.error(f"❌ Erro ao classificar: {str(e)}")
                return
    
    # Mostrar resultado
    if st.session_state.last_result is not None:
        result = st.session_state.last_result
        
        st.markdown('<div class="sub-header">📊 Resultado da Classificação</div>', unsafe_allow_html=True)
        
        # Box colorido baseado na classe
        class_colors = {
            'Orgânico': '#4CAF50',
            'Reciclável': '#2196F3',
            'Rejeito': '#9E9E9E',
            'Perigoso': '#F44336'
        }
        
        class_icons = {
            'Orgânico': '🌱',
            'Reciclável': '♻️',
            'Rejeito': '🗑️',
            'Perigoso': '⚠️'
        }
        
        classe = result['classe']
        confianca = result['confianca']
        
        # Resultado principal
        st.markdown(f"""
        <div class="result-box" style="border-left: 6px solid {class_colors.get(classe, '#757575')}">
            <h2 style="color: {class_colors.get(classe, '#757575')}; margin-top: 0;">
                {class_icons.get(classe, '❓')} {classe}
            </h2>
            <p style="font-size: 1.2rem; margin: 0.5rem 0;">
                <strong>Confiança:</strong> {confianca:.1%}
            </p>
            <p style="margin: 0.5rem 0;">{result['explicacao']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Probabilidades
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Probabilidades por Classe:**")
            for class_name, prob in result['probabilidades'].items():
                st.progress(prob, text=f"{class_icons.get(class_name, '❓')} {class_name}: {prob:.1%}")
        
        with col2:
            st.markdown("**Orientação de Descarte:**")
            st.markdown(f"""
            <div class="info-box">
                {result['dica_descarte']}
            </div>
            """, unsafe_allow_html=True)
        
        # Informações adicionais
        with st.expander("ℹ️ Informações Técnicas"):
            st.json(result)


def main():
    """Função principal da aplicação."""
    # Inicializar sessão
    initialize_session_state()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/recycle-sign.png", width=100)
        st.markdown("# GreenTrash")
        st.markdown("---")
        
        page = st.radio(
            "Navegação",
            ["📖 Introdução", "🔍 Classificar"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Sobre")
        st.markdown("""
        Sistema de classificação de resíduos sólidos usando IA.
        
        **ODS 12 & 13**
        - Consumo Sustentável
        - Ação Climática
        
        **Prioriza análise visual**
        """)
        
        st.markdown("---")
        st.markdown("**Versão:** 1.0.0")
        st.markdown("**Tecnologia:** Python + ML")
    
    # Renderizar página selecionada
    if page == "📖 Introdução":
        render_introduction()
    else:
        render_classifier()


if __name__ == "__main__":
    main()

