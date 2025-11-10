# 🎬 Demonstração - IA Resíduos

Guia passo a passo para demonstrar o projeto IA Resíduos.

---

## 🚀 Preparação (5 minutos)

### 1. Abrir Terminal
```bash
cd "C:\Users\pedro\OneDrive\Área de Trabalho\IA Resíduos"
```

### 2. Ativar Ambiente
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Verificar Instalação
```bash
# Se necessário, instalar dependências
pip install -r requirements.txt
```

### 4. Treinar Modelo (se não existir)
```bash
python train_model.py
```

---

## 📋 Roteiro de Demonstração (10-15 minutos)

### PARTE 1: Introdução (2 minutos)

#### Iniciar Aplicação
```bash
streamlit run app.py
```

#### Apresentar Projeto
1. **Tela inicial** - Explicar título e objetivo
2. **Sobre o Projeto** - Destacar alinhamento com ODS 12/13
3. **Como Funciona** - Mostrar fluxo de processamento
4. **Classes** - Explicar 4 categorias de resíduos
5. **Ética e LGPD** - Enfatizar privacidade e conformidade
6. **Tecnologias** - Mencionar features e ML

---

### PARTE 2: Classificação - Texto (3 minutos)

#### Navegar para Classificar
Clicar em "🔍 Classificar" na barra lateral

#### Demonstração 1: Orgânico 🌱
1. Selecionar "✍️ Somente Texto"
2. Digitar: `casca de banana restos de alface`
3. Clicar "Classificar Resíduo"
4. **Resultado esperado:**
   - Classe: Orgânico 🌱
   - Confiança: ~90%+
   - Dica: Lixeira marrom ou compostagem

**Explicar:**
- Sistema analisa keywords
- Identifica palavras relacionadas a orgânicos
- Fornece orientação de descarte

---

#### Demonstração 2: Reciclável ♻️
1. Limpar campo (F5 para resetar se necessário)
2. Digitar: `garrafa de plástico pet transparente`
3. Classificar
4. **Resultado esperado:**
   - Classe: Reciclável ♻️
   - Confiança: ~92%+
   - Dica: Lixeira azul, limpar antes

**Explicar:**
- Keywords: plástico, pet, garrafa
- Alta confiança devido a termos específicos
- Sistema orienta sobre preparação para reciclagem

---

#### Demonstração 3: Perigoso ⚠️
1. Digitar: `pilha bateria lâmpada fluorescente`
2. Classificar
3. **Resultado esperado:**
   - Classe: Perigoso ⚠️
   - Confiança: ~95%+
   - Dica: NUNCA em lixo comum, ponto especial

**Explicar:**
- Múltiplas keywords de perigo
- Sistema prioriza segurança
- Alerta claro sobre não descartar em lixo comum

---

### PARTE 3: Regra de Segurança (2 minutos)

#### Demonstração 4: Caso Ambíguo
1. Digitar: `celular quebrado plástico metal bateria eletrônico`
2. Classificar
3. **Resultado esperado:**
   - Classe: Perigoso ⚠️ (ajustado)
   - Explicação: "Classificação ajustada para 'Perigoso' por segurança"

**Explicar:**
- Texto menciona múltiplas classes (reciclável + perigoso)
- **Regra de segurança ativada**
- Sistema prioriza "Perigoso" em caso de dúvida
- Threshold: 15% de probabilidade é suficiente

**Mostrar Probabilidades:**
- Ver barras de probabilidade
- Notar que "Perigoso" não era a maior
- Mas regra ajustou por segurança

---

### PARTE 4: Classificação com Imagem (3 minutos)

#### Preparar Imagens de Teste
Opções:
1. Tirar foto com celular de um resíduo real
2. Baixar imagem da internet
3. Usar imagens de teste (se preparadas)

#### Demonstração 5: Upload de Imagem
1. Selecionar "📸 Imagem"
2. Upload de imagem (ex: garrafa plástica)
3. (Opcional) Adicionar descrição: `garrafa plástica`
4. Classificar

**Explicar:**
- Sistema extrai 118 features visuais:
  - Cores (HSV)
  - Texturas (LBP, GLCM)
  - Bordas (Canny)
  - Formas (Hu Moments)
- Combina com features textuais se descrição fornecida
- **Resultado mais preciso** que só texto

---

### PARTE 5: Vídeo (opcional - 2 minutos)

#### Demonstração 6: Upload de Vídeo
1. Selecionar "🎥 Vídeo"
2. Upload de vídeo curto de resíduo
3. Sistema extrai primeiro frame automaticamente
4. Classificar

**Explicar:**
- Processa primeiro frame como imagem
- Útil para captura rápida com câmera
- Mesmas features visuais aplicadas

---

### PARTE 6: Aspectos Técnicos (3 minutos)

#### Voltar para Terminal

#### Mostrar Estrutura do Código
```bash
# Listar arquivos
dir  # Windows
ls   # Linux/Mac

# Mostrar módulos
dir src\  # Windows
ls src/   # Linux/Mac
```

**Explicar:**
- `feature_extraction.py` - Extração de 122 features
- `classifier.py` - Random Forest + regras
- `data_generator.py` - Dados sintéticos

#### Mostrar Treinamento (se tempo permitir)
```bash
python train_model.py
```

**Explicar rapidamente:**
- Gera 600 amostras (150 por classe)
- Treina Random Forest
- Valida performance
- Salva modelo

#### Mostrar Testes
```bash
python test_system.py
```

**Explicar:**
- 5 casos de teste
- Valida cada classe
- Verifica regra de segurança

---

## 🎯 Pontos-Chave a Destacar

### Durante a Demonstração

1. **ODS 12 & 13**
   - Sistema promove descarte responsável
   - Reduz contaminação ambiental
   - Educa usuários

2. **Tecnologia**
   - 118 features visuais (6 técnicas)
   - 4 features textuais
   - Random Forest com 100 árvores
   - 122 features totais

3. **Segurança**
   - Regra especial para resíduos perigosos
   - Prioriza segurança em ambiguidade
   - Evita descarte incorreto

4. **LGPD**
   - Sem coleta de dados pessoais
   - Processamento local
   - Transparência total
   - Anonimização

5. **Usabilidade**
   - Interface intuitiva
   - Múltiplas formas de entrada
   - Orientações claras
   - Design responsivo

---

## 💡 Dicas de Apresentação

### Visual
- ✅ Aumentar zoom do navegador (Ctrl/Cmd +)
- ✅ Modo tela cheia (F11)
- ✅ Esconder barra lateral quando não usar

### Verbal
- ✅ Falar claramente e pausadamente
- ✅ Explicar antes de executar
- ✅ Perguntar se há dúvidas
- ✅ Relacionar com conceitos de IA

### Técnico
- ✅ Ter terminal aberto em outra aba
- ✅ Preparar imagens de teste com antecedência
- ✅ Testar antes da demonstração
- ✅ Ter backup (screenshots) se houver problemas

---

## 🐛 Solução de Problemas Durante Demo

### App não abre
```bash
# Verificar se porta está livre
streamlit run app.py --server.port 8502
```

### Modelo não encontrado
```bash
# Treinar rapidamente
python train_model.py
```

### Erro de dependência
```bash
# Reinstalar
pip install -r requirements.txt
```

### Classificação estranha
- Explicar que modelo usa dados sintéticos
- Em produção, usaria dataset real
- Demonstrar que sistema funciona conforme especificado

---

## 📊 Slides de Apoio (Sugestão)

### Slide 1: Título
- **IA Resíduos**
- Classificação Inteligente de Resíduos Sólidos
- ODS 12 & 13

### Slide 2: Problema
- Descarte incorreto de resíduos
- Contaminação ambiental
- Falta de conhecimento

### Slide 3: Solução
- IA para classificação automática
- 4 categorias de resíduos
- Orientações de descarte

### Slide 4: Tecnologia
- 118 features visuais
- 4 features textuais
- Random Forest
- Regra de segurança

### Slide 5: Demonstração
- (Demo ao vivo)

### Slide 6: Resultados
- Precisão ~92%
- Interface intuitiva
- Conformidade LGPD
- Impacto sustentável

### Slide 7: Conclusão
- Sistema completo e funcional
- Alinhado com ODS
- Escalável e expansível

---

## ⏱️ Cronograma Sugerido

| Tempo | Atividade |
|-------|-----------|
| 0-2min | Introdução teórica e objetivos |
| 2-4min | Navegar página Introdução no app |
| 4-10min | Demonstrações de classificação |
| 10-12min | Mostrar código e arquitetura |
| 12-14min | Destacar diferenciais (LGPD, ODS) |
| 14-15min | Conclusão e perguntas |

---

## ✅ Checklist Pré-Demo

**30 minutos antes:**
- [ ] Iniciar computador
- [ ] Abrir pasta do projeto
- [ ] Ativar ambiente virtual
- [ ] Verificar modelo treinado
- [ ] Testar app rapidamente
- [ ] Preparar imagens de teste
- [ ] Abrir slides (se houver)

**5 minutos antes:**
- [ ] Fechar aplicações desnecessárias
- [ ] Silenciar notificações
- [ ] Aumentar brilho da tela
- [ ] Testar áudio (se houver)
- [ ] Respirar fundo 😊

---

**Boa sorte na demonstração! 🚀**

**Lembre-se:** Você construiu um sistema completo, funcional e alinhado com sustentabilidade. Mostre isso com confiança! 💪

