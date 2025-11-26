# GreenTrash — Executando no Windows (sem INICIAR.bat)

Este guia mostra como instalar e rodar a aplicação no Windows sem usar o arquivo `INICIAR.bat`, e sem criar ambiente virtual (venv).

## Pré-requisitos
- Python 64-bit instalado (recomendado 3.10 ou 3.11).
- Acesso ao terminal PowerShell ou Prompt de Comando.

Verifique se seu Python é 64-bit:
```powershell
py -c "import platform,struct;print(platform.python_version(), struct.calcsize('P')*8, 'bits')"
```
Se o resultado mostrar `32 bits`, instale o Python 64-bit do site oficial antes de continuar.

## Instalação (sem venv)
No diretório do projeto (pasta com `app.py`):
```powershell
cd CAMINHO\para\GreenTrash
py -m pip install --upgrade pip
py -m pip install --user -r requirements.txt
```
Dicas:
- `--user` instala os pacotes no perfil do usuário (sem admin e sem venv).
- Se ocorrer erro ao instalar `scikit-image`, veja a seção “Solução de problemas”.

## Executando a aplicação
Use o launcher do Python para chamar o Streamlit (evita problemas de PATH):
```powershell
py -m streamlit run app.py
```
A aplicação fica disponível em: http://localhost:8501

## Treinamento (opcional)
Para treinar o modelo com dados reais (se aplicável):
```powershell
py train_model_real.py
```

## Modo "lite" (sem scikit-image)
Se preferir rodar imediatamente sem `scikit-image` (recursos visuais reduzidos), instale somente os pacotes essenciais e execute:
```powershell
cd CAMINHO\para\GreenTrash
py -m pip install --user streamlit==1.28.0 opencv-python==4.8.1.78 scikit-learn==1.3.2 numpy==1.24.3 pandas==2.1.3 Pillow==10.1.0 matplotlib==3.8.2 joblib==1.3.2
py -m streamlit run app.py
```
Observação: neste modo, certas features visuais (LBP/GLCM) são desativadas, mas a aplicação roda e a classificação baseada em texto continua funcionando.

## Solução de problemas
- Erro ao compilar `scikit-image` (Mensagens envolvendo Meson/MinGW/GCC):
  - Causa: ausência de wheel compatível; o `pip` tenta compilar nativamente e falha.
  - Solução recomendada: usar Python 64-bit e forçar instalação via wheel.
  - Comandos:
    ```powershell
    py -m pip install --upgrade pip
    py -m pip install --user --only-binary :all: scikit-image==0.22.0
    py -m pip install --user -r requirements.txt
    ```
  - Se não houver wheel para sua versão, instale Python 64-bit suportado (3.10/3.11) e repita.

- `cv2` (OpenCV) falhou ao iniciar:
  - Instale o “Microsoft Visual C++ Redistributable 2015–2022”.

- Comandos não reconhecidos (`streamlit`, `pip`):
  - Use sempre o formato `py -m <modulo>`, por exemplo: `py -m streamlit run app.py` e `py -m pip install ...`.

- Desinstalar dependências (opcional):
  ```powershell
  py -m pip uninstall -r requirements.txt -y
  ```

## Observações
- Este guia evita o uso de ambiente virtual por simplicidade. Para ambientes isolados, você pode usar `venv` ou `conda`.
- Caso prefira usar o script, o arquivo `INICIAR.bat` automatiza a instalação e execução com fallback quando `scikit-image` não está disponível.
