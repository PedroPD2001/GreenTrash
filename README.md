# 🌱 IA Resíduos - Classificação Inteligente de Resíduos Sólidos

Sistema de Inteligência Artificial para classificação de resíduos sólidos, desenvolvido para promover consumo e produção sustentáveis alinhado aos **ODS 12 e 13** da ONU.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [ODS 12 & 13](#ods-12--13)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Arquitetura Técnica](#arquitetura-técnica)
- [Ética e LGPD](#ética-e-lgpd)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuindo](#contribuindo)

---

## 🎯 Sobre o Projeto

O **IA Resíduos** é uma aplicação de Machine Learning que classifica resíduos sólidos em quatro categorias principais:

- 🌱 **Orgânico** - Restos de alimentos, cascas, folhas
- ♻️ **Reciclável** - Papel, plástico, vidro, metal
- 🗑️ **Rejeito** - Materiais não recicláveis
- ⚠️ **Perigoso** - Pilhas, produtos químicos, eletrônicos

O sistema aceita **imagem, vídeo ou descrição textual** e retorna a classificação com orientações de descarte apropriado.

---

## 🌍 ODS 12 & 13

Este projeto está alinhado aos Objetivos de Desenvolvimento Sustentável da ONU:

### ODS 12 - Consumo e Produção Sustentáveis
- Promove descarte responsável de resíduos
- Reduz impactos ambientais através da reciclagem
- Educa sobre práticas sustentáveis

### ODS 13 - Ação Contra a Mudança Global do Clima
- Reduz emissões através do descarte adequado
- Evita contaminação ambiental
- Promove economia circular

---

## ✨ Funcionalidades

### Interface Intuitiva
- **Página Introdução**: Explica funcionamento, ética e LGPD
- **Página Classificar**: Interface para classificação de resíduos

### Múltiplas Entradas
- 📸 **Upload de imagem** (JPG, PNG, BMP)
- 🎥 **Upload de vídeo** (MP4, AVI, MOV, MKV)
- ✍️ **Descrição textual** do resíduo

### Análise Avançada
- Extração de features visuais (HSV, LBP, GLCM, Canny, Hu Moments)
- Análise de palavras-chave textuais
- Combinação de informações visuais e textuais

### Classificação Inteligente
- Modelo Random Forest treinado
- **Regra de segurança**: Prioriza "Perigoso" em casos de incerteza
- Fallback textual quando modelo não disponível
- Probabilidades detalhadas por classe

### Resultados Completos
- Classe identificada com nível de confiança
- Explicação da classificação
- **Orientações de descarte** específicas
- Visualização de probabilidades

---

## 🛠️ Tecnologias

### Visão Computacional
- **OpenCV** - Processamento de imagens
- **Scikit-image** - Extração de features
- Histogramas HSV (cores)
- LBP - Local Binary Patterns (texturas)
- GLCM - Gray Level Co-occurrence Matrix (texturas)
- Canny Edge Detection (bordas)
- Hu Moments (formas)

### Machine Learning
- **Scikit-learn** - Random Forest Classifier
- 122 features combinadas (118 visuais + 4 textuais)
- Balanceamento de classes
- Validação com dados sintéticos

### Interface
- **Streamlit** - Interface web interativa
- Design responsivo e moderno
- Visualizações dinâmicas

---

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/ia-residuos.git
cd ia-residuos
```

2. **Crie um ambiente virtual (recomendado)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Treine o modelo**
```bash
python train_model.py
```

Este comando irá:
- Gerar 600 amostras sintéticas (150 por classe)
- Treinar o modelo Random Forest
- Avaliar performance no conjunto de teste
- Salvar o modelo em `models/waste_classifier.pkl`

5. **Execute a aplicação**
```bash
streamlit run app.py
```

A aplicação estará disponível em: `http://localhost:8501`

---

## 🚀 Como Usar

### 1. Navegue até a página "Classificar"

### 2. Escolha o método de entrada
- **Imagem**: Tire uma foto ou carregue imagem do resíduo
- **Vídeo**: Grave ou carregue vídeo (primeiro frame será usado)
- **Texto**: Descreva o resíduo em palavras

### 3. Adicione descrição (opcional)
Para melhores resultados, combine imagem com descrição textual:
- "garrafa de plástico transparente"
- "casca de banana"
- "pilha AA usada"

### 4. Classifique
Clique em "Classificar Resíduo" e aguarde o resultado.

### 5. Visualize o resultado
- Classe identificada
- Nível de confiança
- Probabilidades por classe
- **Orientações de descarte**

---

## 🏗️ Arquitetura Técnica

### Extração de Features Visuais (118 features)

1. **Histograma HSV** (90 features)
   - 30 bins por canal (H, S, V)
   - Normalizado

2. **Estatísticas HSV** (6 features)
   - Média e desvio padrão de cada canal

3. **LBP - Local Binary Patterns** (10 features)
   - Radius: 3, Points: 24
   - Histograma uniforme

4. **GLCM** (4 features)
   - Contrast, Dissimilarity, Homogeneity, Energy
   - Gray Level Co-occurrence Matrix

5. **Canny Edge Detection** (1 feature)
   - Densidade de bordas

6. **Hu Moments** (7 features)
   - Momentos invariantes de forma
   - Transformação logarítmica

### Extração de Features Textuais (4 features)

- Score de correspondência com keywords de cada classe
- Dicionário com 20-25 termos por classe
- Normalização por frequência

### Modelo Random Forest

- **Estimadores**: 100 árvores
- **Max Depth**: 20
- **Class Weight**: Balanced
- **Features**: 122 (visuais + textuais)
- **Classes**: 4 (Orgânico, Reciclável, Rejeito, Perigoso)

### Regra de Segurança

```python
# Prioriza "Perigoso" se:
# 1. Prob(Perigoso) >= 15%
# 2. Confiança geral < 60%
# 3. Classe prevista != Perigoso
```

Esta regra garante que resíduos potencialmente perigosos não sejam descartados incorretamente.

### Fallback Textual

Quando modelo não está disponível:
- Utiliza apenas features textuais
- Classificação baseada em keywords
- Menor precisão, mas funcional

---

## 🔒 Ética e LGPD

O sistema está em conformidade com a **Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018)**.

### Princípios Implementados

✅ **Dados Mínimos**: Coleta apenas imagens/descrições de resíduos

✅ **Anonimização**: Nenhuma informação pessoal identificável

✅ **Processamento Local**: Análise no dispositivo quando possível

✅ **Sem Armazenamento**: Imagens não são salvas após processamento

✅ **Transparência**: Código aberto e auditável

✅ **Finalidade Específica**: Uso exclusivo para classificação de resíduos

✅ **Segurança**: Regra especial para resíduos perigosos

### Privacidade

- Nenhum dado biométrico é coletado
- Nenhuma geolocalização é armazenada
- Nenhum dado é compartilhado com terceiros
- Processamento em memória (sem persistência)

---

## 📁 Estrutura do Projeto

```
ia-residuos/
│
├── app.py                      # Aplicação Streamlit (interface)
├── train_model.py              # Script de treinamento
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
│
├── src/                        # Módulos principais
│   ├── __init__.py
│   ├── feature_extraction.py  # Extração de features
│   ├── classifier.py          # Modelo de classificação
│   └── data_generator.py      # Geração de dados sintéticos
│
└── models/                     # Modelos treinados (criado automaticamente)
    └── waste_classifier.pkl   # Modelo Random Forest
```

---

## 📊 Performance do Modelo

Após treinamento com dados sintéticos:

| Classe      | Precision | Recall | F1-Score |
|-------------|-----------|--------|----------|
| Orgânico    | ~0.95     | ~0.93  | ~0.94    |
| Reciclável  | ~0.92     | ~0.94  | ~0.93    |
| Rejeito     | ~0.91     | ~0.90  | ~0.91    |
| Perigoso    | ~0.93     | ~0.95  | ~0.94    |

**Nota**: Performance com dados reais pode variar. Para produção, recomenda-se treinar com dataset real.

---

## 🔮 Melhorias Futuras

- [ ] Coleta de dataset real com imagens anotadas
- [ ] Transfer learning com ResNet/MobileNet
- [ ] API REST para integração
- [ ] Aplicativo móvel nativo
- [ ] Suporte multilíngue
- [ ] Histórico de classificações (com opt-in)
- [ ] Integração com mapas de pontos de coleta
- [ ] Gamificação para engajamento

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 👨‍💻 Autor

**Projeto de Avaliação - IA Resíduos**

Desenvolvido como projeto acadêmico focado em sustentabilidade e tecnologia.

---

## 🙏 Agradecimentos

- ONU - Objetivos de Desenvolvimento Sustentável
- Comunidade Open Source Python
- Scikit-learn e OpenCV teams
- Streamlit por facilitar desenvolvimento de interfaces

---

## 📞 Suporte

Para questões, sugestões ou problemas:
- Abra uma [Issue](https://github.com/seu-usuario/ia-residuos/issues)
- Consulte a [Documentação](https://github.com/seu-usuario/ia-residuos/wiki)

---

## 🌟 Star o Projeto

Se este projeto foi útil, considere dar uma ⭐ no repositório!

---

**Juntos por um futuro mais sustentável! 🌍♻️**

