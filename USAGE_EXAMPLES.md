# 📖 Exemplos de Uso

Este documento fornece exemplos práticos de uso do sistema IA Resíduos.

---

## 🌱 Classificação de Orgânicos

### Exemplo 1: Casca de Fruta
**Entrada (Texto):**
```
casca de banana
```

**Resultado Esperado:**
- Classe: Orgânico 🌱
- Confiança: ~95%
- Dica: "Descarte em lixeira marrom ou faça compostagem"

### Exemplo 2: Restos de Comida
**Entrada (Texto):**
```
restos de alface, tomate e cenoura
```

**Resultado Esperado:**
- Classe: Orgânico 🌱
- Confiança: ~90%

---

## ♻️ Classificação de Recicláveis

### Exemplo 3: Garrafa PET
**Entrada (Texto):**
```
garrafa de plástico pet transparente
```

**Resultado Esperado:**
- Classe: Reciclável ♻️
- Confiança: ~92%
- Dica: "Descarte em lixeira azul ou ponto de coleta seletiva"

### Exemplo 4: Papel
**Entrada (Texto):**
```
folhas de papel sulfite jornal revista
```

**Resultado Esperado:**
- Classe: Reciclável ♻️
- Confiança: ~88%

### Exemplo 5: Lata de Alumínio
**Entrada (Texto):**
```
lata de refrigerante alumínio
```

**Resultado Esperado:**
- Classe: Reciclável ♻️
- Confiança: ~94%

---

## 🗑️ Classificação de Rejeito

### Exemplo 6: Papel Higiênico
**Entrada (Texto):**
```
papel higiênico usado
```

**Resultado Esperado:**
- Classe: Rejeito 🗑️
- Confiança: ~85%
- Dica: "Descarte em lixeira cinza ou preta (lixo comum)"

### Exemplo 7: Fralda
**Entrada (Texto):**
```
fralda descartável suja
```

**Resultado Esperado:**
- Classe: Rejeito 🗑️
- Confiança: ~90%

---

## ⚠️ Classificação de Perigoso

### Exemplo 8: Pilha
**Entrada (Texto):**
```
pilha AA bateria
```

**Resultado Esperado:**
- Classe: Perigoso ⚠️
- Confiança: ~96%
- Dica: "NÃO descarte em lixo comum! Leve a ponto de coleta especial"

### Exemplo 9: Lâmpada Fluorescente
**Entrada (Texto):**
```
lâmpada fluorescente queimada mercúrio
```

**Resultado Esperado:**
- Classe: Perigoso ⚠️
- Confiança: ~94%

### Exemplo 10: Produto Químico
**Entrada (Texto):**
```
tinta óleo solvente químico
```

**Resultado Esperado:**
- Classe: Perigoso ⚠️
- Confiança: ~92%

---

## 🔀 Casos Ambíguos (Regra de Segurança)

### Exemplo 11: Descrição Incerta
**Entrada (Texto):**
```
bateria celular eletrônico plástico
```

**Comportamento:**
- Múltiplas classes detectadas (Perigoso + Reciclável)
- **Regra de segurança ativada**
- Resultado: Perigoso ⚠️ (por precaução)
- Explicação: "Classificação ajustada para 'Perigoso' por segurança"

---

## 📸 Uso com Imagem

### Exemplo 12: Imagem + Texto
**Entrada:**
- Imagem: Foto de garrafa plástica
- Texto: "garrafa de água pet"

**Vantagem:**
- Features visuais (cor, forma, textura)
- Features textuais (keywords)
- **Maior precisão** (~95%+)

---

## 🎥 Uso com Vídeo

### Exemplo 13: Vídeo Curto
**Entrada:**
- Vídeo: Filmagem de resíduo orgânico
- Sistema extrai primeiro frame
- Processa como imagem

---

## 💡 Dicas para Melhores Resultados

1. **Seja específico na descrição**
   - ✅ Bom: "garrafa de plástico pet transparente"
   - ❌ Ruim: "garrafa"

2. **Combine imagem e texto**
   - Melhora precisão em 10-20%

3. **Inclua características distintivas**
   - Material (plástico, metal, vidro)
   - Cor (transparente, verde, marrom)
   - Estado (limpo, sujo, quebrado)

4. **Use palavras-chave relevantes**
   - Orgânico: compostagem, biodegradável, alimento
   - Reciclável: reciclagem, limpo, embalagem
   - Rejeito: sujo, contaminado, não reciclável
   - Perigoso: tóxico, químico, bateria, eletrônico

---

## ⚡ Testes Rápidos (CLI)

Se preferir testar via código Python:

```python
from src.feature_extraction import FeatureExtractor
from src.classifier import WasteClassifier

# Inicializar
extractor = FeatureExtractor()
classifier = WasteClassifier()

# Classificar por texto
text = "casca de banana"
features = extractor.extract_combined_features(text=text)
result = classifier.predict(features)

print(f"Classe: {result['classe']}")
print(f"Confiança: {result['confianca']:.1%}")
print(f"Dica: {result['dica_descarte']}")
```

---

**Explore diferentes combinações e contribua com mais exemplos!** 🚀

