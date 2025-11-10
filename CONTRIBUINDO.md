# 🤝 Guia de Contribuição

Obrigado por considerar contribuir para o projeto **IA Resíduos**! 

Este documento fornece diretrizes para contribuir com o projeto.

---

## 📋 Código de Conduta

- Seja respeitoso e inclusivo
- Aceite críticas construtivas
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros

---

## 🚀 Como Contribuir

### 1. Reportar Bugs

**Antes de reportar:**
- Verifique se o bug já foi reportado nas [Issues](https://github.com/seu-usuario/ia-residuos/issues)
- Teste com a versão mais recente

**Ao reportar:**
- Use título claro e descritivo
- Descreva passos para reproduzir
- Inclua comportamento esperado vs. real
- Adicione screenshots se relevante
- Informe versão do Python e SO

### 2. Sugerir Melhorias

**Boas sugestões incluem:**
- Novas funcionalidades
- Melhorias de performance
- Melhorias de UX/UI
- Documentação

**Ao sugerir:**
- Use título claro
- Explique o problema atual
- Descreva solução proposta
- Liste benefícios

### 3. Contribuir com Código

#### Setup do Ambiente

```bash
# Fork e clone
git clone https://github.com/seu-usuario/ia-residuos.git
cd ia-residuos

# Crie branch
git checkout -b feature/minha-feature

# Ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Dependências
pip install -r requirements.txt

# Teste
python test_system.py
```

#### Padrões de Código

**Python:**
- Siga PEP 8
- Use docstrings (Google style)
- Adicione type hints quando possível
- Comente código complexo

**Exemplo:**
```python
def classify_waste(image: np.ndarray, text: str = "") -> dict:
    """
    Classifica resíduo a partir de imagem e/ou texto.
    
    Args:
        image: Imagem numpy array em formato BGR
        text: Descrição textual opcional
        
    Returns:
        Dicionário com classe, confiança e dicas
    """
    pass
```

**Commits:**
- Use mensagens claras e descritivas
- Prefixos recomendados:
  - `feat:` - Nova funcionalidade
  - `fix:` - Correção de bug
  - `docs:` - Documentação
  - `style:` - Formatação
  - `refactor:` - Refatoração
  - `test:` - Testes
  - `chore:` - Manutenção

**Exemplo:**
```
feat: adicionar suporte para PDF na classificação
fix: corrigir erro de divisão por zero em HSV stats
docs: atualizar README com exemplos de vídeo
```

#### Pull Request

**Antes de submeter:**
1. Teste localmente
2. Atualize documentação
3. Adicione testes se aplicável
4. Certifique-se que código segue padrões

**Ao submeter:**
1. Use título descritivo
2. Descreva mudanças detalhadamente
3. Referencie issues relacionadas
4. Adicione screenshots se relevante

**Template:**
```markdown
## Descrição
Breve descrição das mudanças.

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Como Testar
Passos para testar as mudanças.

## Checklist
- [ ] Código segue padrões do projeto
- [ ] Documentação atualizada
- [ ] Testes passando
- [ ] Sem warnings
```

---

## 🎯 Áreas para Contribuir

### Prioridade Alta
- [ ] Coleta de dataset real com imagens anotadas
- [ ] Testes unitários e de integração
- [ ] Melhorias na precisão do modelo
- [ ] Documentação de API

### Prioridade Média
- [ ] Transfer learning com CNNs
- [ ] Suporte multilíngue (EN, ES)
- [ ] API REST
- [ ] Mobile app

### Prioridade Baixa
- [ ] Gamificação
- [ ] Integração com mapas
- [ ] Modo offline
- [ ] Temas customizáveis

---

## 🧪 Testes

### Executar Testes
```bash
# Teste simples
python test_system.py

# Treinar modelo
python train_model.py

# Executar app
streamlit run app.py
```

### Adicionar Testes
```python
# Criar arquivo tests/test_nome.py
import unittest
from src.classifier import WasteClassifier

class TestClassifier(unittest.TestCase):
    def test_organic_classification(self):
        # Seu teste aqui
        pass
```

---

## 📚 Documentação

### Atualizar Documentação
- README.md - Visão geral
- QUICKSTART.md - Início rápido
- USAGE_EXAMPLES.md - Exemplos
- Docstrings - Código

### Adicionar Exemplos
```python
# USAGE_EXAMPLES.md
## Novo Exemplo
**Entrada:**
```
texto de exemplo
```

**Resultado:**
- Classe: X
- Confiança: Y%
```

---

## 🏆 Reconhecimento

Contribuidores serão listados em:
- README.md (seção Contribuidores)
- Releases notes
- Changelog

---

## 📞 Contato

Dúvidas sobre contribuição?
- Abra uma [Discussion](https://github.com/seu-usuario/ia-residuos/discussions)
- Comente em uma Issue existente
- Entre em contato com mantenedores

---

## 📝 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a MIT License.

---

**Obrigado por contribuir! 🌟**

