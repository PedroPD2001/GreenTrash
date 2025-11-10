# 🚀 Guia Rápido de Início

Este guia ajudará você a configurar e executar o projeto IA Resíduos em minutos!

---

## ⚡ Instalação Rápida

### 1. Clone e Entre no Diretório
```bash
git clone https://github.com/seu-usuario/ia-residuos.git
cd ia-residuos
```

### 2. Crie Ambiente Virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale Dependências
```bash
pip install -r requirements.txt
```

### 4. Treine o Modelo
```bash
python train_model.py
```

**Saída esperada:**
- Geração de 600 amostras (150 por classe)
- Treinamento do Random Forest
- Relatório de classificação
- Modelo salvo em `models/waste_classifier.pkl`

### 5. Execute a Aplicação
```bash
streamlit run app.py
```

**Acesse:** `http://localhost:8501`

---

## 🎯 Teste Rápido

### Teste 1: Texto Simples
1. Vá para **Classificar**
2. Escolha **Somente Texto**
3. Digite: "casca de banana"
4. Clique em **Classificar**
5. **Resultado esperado**: Orgânico 🌱

### Teste 2: Texto com Reciclável
1. Digite: "garrafa de plástico pet"
2. **Resultado esperado**: Reciclável ♻️

### Teste 3: Texto com Perigoso
1. Digite: "pilha AA velha bateria"
2. **Resultado esperado**: Perigoso ⚠️

---

## 📸 Teste com Imagem

1. Tire uma foto de um resíduo
2. Carregue na opção **Imagem**
3. Adicione descrição (opcional)
4. Classifique!

---

## 🐛 Solução de Problemas

### Erro: "No module named 'cv2'"
```bash
pip install opencv-python
```

### Erro: "No module named 'skimage'"
```bash
pip install scikit-image
```

### Modelo não encontrado
```bash
python train_model.py
```

### Porta 8501 em uso
```bash
streamlit run app.py --server.port 8502
```

---

## 📚 Próximos Passos

- Explore a página **Introdução** para entender o projeto
- Teste com diferentes tipos de resíduos
- Leia o [README completo](README.md)
- Contribua com o projeto!

---

**Pronto! 🎉 Você está usando IA para classificar resíduos!**

