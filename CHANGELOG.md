# 📝 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

---

## [1.0.0] - 2025-11-03

### 🎉 Lançamento Inicial

#### Adicionado
- Sistema completo de classificação de resíduos com IA
- Interface Streamlit com páginas Introdução e Classificar
- Suporte para entrada via imagem, vídeo ou texto
- Extração de 122 features (118 visuais + 4 textuais)
- Modelo Random Forest com 100 estimadores
- Regra de segurança priorizando resíduos perigosos
- Sistema de fallback baseado em texto
- 4 classes: Orgânico, Reciclável, Rejeito, Perigoso

#### Features Visuais
- Histograma HSV (90 features)
- Estatísticas HSV - média e std (6 features)
- LBP - Local Binary Patterns (10 features)
- GLCM - Gray Level Co-occurrence Matrix (4 features)
- Canny Edge Detection (1 feature)
- Hu Moments (7 features)

#### Features Textuais
- Dicionário com 80+ keywords
- Score de correspondência por classe (4 features)
- Normalização por frequência

#### Documentação
- README.md completo
- QUICKSTART.md para início rápido
- USAGE_EXAMPLES.md com exemplos práticos
- CONTRIBUINDO.md com guia de contribuição
- Docstrings em todos os módulos

#### Scripts
- `train_model.py` - Treinamento automático
- `test_system.py` - Testes de validação
- `run.bat` - Script de execução Windows
- `run.sh` - Script de execução Linux/Mac

#### Conformidade
- LGPD - Lei Geral de Proteção de Dados
- Ética em IA - Transparência e responsabilidade
- ODS 12 - Consumo e Produção Sustentáveis
- ODS 13 - Ação Contra a Mudança do Clima

---

## [Futuro] - Roadmap

### Planejado para v1.1.0
- [ ] Coleta de dataset real
- [ ] Testes unitários
- [ ] API REST
- [ ] Melhorias de performance

### Planejado para v1.2.0
- [ ] Transfer learning com ResNet
- [ ] Suporte multilíngue (EN, ES)
- [ ] Aplicativo móvel
- [ ] Histórico de classificações

### Planejado para v2.0.0
- [ ] Detecção de múltiplos objetos
- [ ] Integração com mapas de coleta
- [ ] Gamificação
- [ ] Modo colaborativo

---

## Tipos de Mudanças

- **Adicionado** - Para novas funcionalidades
- **Modificado** - Para mudanças em funcionalidades existentes
- **Depreciado** - Para funcionalidades que serão removidas
- **Removido** - Para funcionalidades removidas
- **Corrigido** - Para correções de bugs
- **Segurança** - Para vulnerabilidades

---

**Formato de Versão:** MAJOR.MINOR.PATCH
- **MAJOR** - Mudanças incompatíveis na API
- **MINOR** - Novas funcionalidades compatíveis
- **PATCH** - Correções de bugs compatíveis

