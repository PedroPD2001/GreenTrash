# ⚡ Referência Rápida - IA Resíduos

Comandos e informações essenciais em um único lugar.

---

## 🚀 Instalação e Execução

### Setup Inicial
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente
venv\Scripts\activate              # Windows
source venv/bin/activate           # Linux/Mac

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Treinar modelo
python train_model.py

# 5. Executar aplicação
streamlit run app.py
```

### Comandos Rápidos Windows
```batch
run.bat
```

### Comandos Rápidos Linux/Mac
```bash
bash run.sh
```

---

## 📊 Arquivos Principais

| Arquivo | Propósito | Linhas |
|---------|-----------|--------|
| `app.py` | Interface Streamlit | 450 |
| `src/feature_extraction.py` | Extração de features | 250 |
| `src/classifier.py` | Modelo + Classificação | 200 |
| `src/data_generator.py` | Dados sintéticos | 150 |
| `train_model.py` | Treinamento | 80 |
| `test_system.py` | Testes | 70 |

---

## 🎯 Classes de Resíduos

| Classe | Ícone | Cor | Lixeira | Exemplos |
|--------|-------|-----|---------|----------|
| Orgânico | 🌱 | Verde | Marrom | Cascas, folhas, restos de comida |
| Reciclável | ♻️ | Azul | Azul | Papel, plástico, vidro, metal |
| Rejeito | 🗑️ | Cinza | Preta/Cinza | Papel higiênico, fraldas |
| Perigoso | ⚠️ | Vermelho | Especial | Pilhas, baterias, produtos químicos |

---

## 🔢 Features Extraídas

### Visuais (118 features)
```
Histograma HSV:    90  (30 por canal H, S, V)
Estatísticas HSV:   6  (média + std de H, S, V)
LBP:               10  (histograma uniforme)
GLCM:               4  (contrast, dissimilarity, homogeneity, energy)
Canny:              1  (densidade de bordas)
Hu Moments:         7  (invariantes de forma)
```

### Textuais (4 features)
```
Score por classe:   4  (1 por cada classe)
```

**Total:** 122 features

---

## 🤖 Modelo Random Forest

```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    random_state=42
)
```

---

## ⚠️ Regra de Segurança

```python
if prob_perigoso >= 15% and confianca_geral < 60%:
    classe = "Perigoso"
    explicacao = "Classificação ajustada por segurança"
```

---

## 📝 Exemplos de Teste Rápido

### Via Interface Web
1. `streamlit run app.py`
2. Ir para "Classificar"
3. Testar:
   - Texto: "casca de banana" → Orgânico 🌱
   - Texto: "garrafa pet" → Reciclável ♻️
   - Texto: "pilha bateria" → Perigoso ⚠️
   - Texto: "papel higiênico usado" → Rejeito 🗑️

### Via Python
```python
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier

extractor = FeatureExtractor()
classifier = WasteClassifier()

features = extractor.extract_combined_features(text="casca de banana")
result = classifier.predict(features)

print(result['classe'])      # Orgânico
print(result['confianca'])   # 0.95
```

---

## 📦 Dependências Principais

```
streamlit==1.28.0           # Interface
opencv-python==4.8.1.78     # Visão computacional
scikit-image==0.22.0        # Processamento imagem
scikit-learn==1.3.2         # Machine Learning
numpy==1.24.3               # Computação
```

---

## 🌐 URLs Úteis

| Recurso | URL |
|---------|-----|
| App Local | http://localhost:8501 |
| Porta Alternativa | http://localhost:8502 |

---

## 🔧 Solução de Problemas

### Modelo não encontrado
```bash
python train_model.py
```

### Porta ocupada
```bash
streamlit run app.py --server.port 8502
```

### Erro de dependência
```bash
pip install --upgrade -r requirements.txt
```

### Limpar cache Streamlit
```bash
streamlit cache clear
```

---

## 📂 Estrutura de Diretórios

```
IA Resíduos/
├── src/                    # Código fonte
├── models/                 # Modelos treinados
├── .streamlit/             # Configuração
├── app.py                  # Interface
├── train_model.py          # Treinamento
├── test_system.py          # Testes
└── *.md                    # Documentação
```

---

## 🎨 Cores do Tema

```python
PRIMARY_COLOR = "#4CAF50"      # Verde
BACKGROUND_COLOR = "#FFFFFF"    # Branco
SECONDARY_BG = "#F5F5F5"       # Cinza claro
TEXT_COLOR = "#212121"         # Preto
```

---

## 📊 Métricas de Performance

```
Precisão média:     ~92%
Tempo resposta:     < 1 segundo
Tamanho modelo:     ~1 MB
Amostras treino:    600
```

---

## 🔑 Variáveis Importantes

```python
# Limites de confiança
DANGER_THRESHOLD = 0.15        # 15% para perigoso
CONFIDENCE_THRESHOLD = 0.40    # 40% confiança mínima

# LBP
LBP_RADIUS = 3
LBP_N_POINTS = 24

# Classes
CLASSES = ['Orgânico', 'Reciclável', 'Rejeito', 'Perigoso']
```

---

## 📚 Documentação

| Arquivo | Para quê? |
|---------|-----------|
| **README.md** | Visão geral completa |
| **QUICKSTART.md** | Instalação rápida |
| **USAGE_EXAMPLES.md** | Exemplos práticos |
| **AVALIACAO.md** | Checklist requisitos |
| **DEMO.md** | Roteiro demonstração |
| **PROJECT_INFO.md** | Info técnica |
| **REFERENCIA_RAPIDA.md** | Este arquivo |

---

## 🐛 Debug

### Ver logs do Streamlit
```bash
streamlit run app.py --logger.level=debug
```

### Testar módulo específico
```python
# Testar extração de features
from src.feature_extraction import FeatureExtractor
extractor = FeatureExtractor()
features = extractor.extract_text_features("teste")
print(features)
```

---

## 📋 Checklist Rápido

**Antes de demonstrar:**
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas
- [ ] Modelo treinado
- [ ] App testado localmente
- [ ] Imagens de teste preparadas

**Durante demonstração:**
- [ ] Mostrar página Introdução
- [ ] Classificar texto (orgânico)
- [ ] Classificar texto (reciclável)
- [ ] Classificar texto (perigoso)
- [ ] Mostrar regra de segurança
- [ ] (Opcional) Classificar imagem

---

## 🎯 Pontos-Chave

1. **ODS 12 & 13** - Sustentabilidade
2. **122 features** - 118 visuais + 4 textuais
3. **Random Forest** - 100 árvores
4. **Regra de segurança** - 15% threshold
5. **LGPD compliant** - Privacidade garantida
6. **Multimodal** - Imagem/Vídeo/Texto

---

## ⌨️ Atalhos Streamlit

| Atalho | Ação |
|--------|------|
| `R` | Recarregar app |
| `C` | Limpar cache |
| `F11` | Tela cheia |
| `Ctrl +` | Aumentar zoom |
| `Ctrl -` | Diminuir zoom |

---

## 🚀 Deploy (Futuro)

### Streamlit Cloud
```bash
# Commit e push
git add .
git commit -m "Deploy"
git push

# Streamlit Cloud → Deploy
```

### Docker (Futuro)
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD streamlit run app.py
```

---

## 📞 Suporte Rápido

**Problemas comuns:**
- Modelo não carrega → Executar `train_model.py`
- Porta ocupada → Usar `--server.port 8502`
- Import error → Verificar ambiente virtual ativado
- Feature error → Verificar versão das bibliotecas

**Para mais detalhes:**
- Consultar README.md
- Verificar AVALIACAO.md
- Ler código fonte (bem documentado)

---

**Última atualização:** Novembro 2025  
**Versão:** 1.0.0

