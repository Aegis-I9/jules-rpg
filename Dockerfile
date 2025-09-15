# 1. Usar uma imagem Python oficial como imagem base
FROM python:3.11-slim

# 2. Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# 3. Copiar o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# 4. Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiar todo o código da aplicação para o diretório de trabalho
# O .dockerignore garantirá que arquivos desnecessários não sejam copiados.
COPY . .

# 6. Expor a porta em que o Flask irá rodar
EXPOSE 5000

# 7. Definir a variável de ambiente PYTHONPATH para que os imports funcionem
ENV PYTHONPATH=.

# 8. Definir o comando para rodar a aplicação quando o contêiner iniciar
CMD ["python3", "app.py"]
