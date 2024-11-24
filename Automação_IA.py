import os  # Para manipular arquivos e diretórios
import PyPDF2  # Para extrair texto de arquivos PDF
import requests  # Para enviar requisições HTTP, incluindo chamadas à API do Google Gemini
from google.oauth2 import service_account  # Para autenticação usando credenciais do Google
import google.auth.transport.requests  # Suporte para transporte de requisições autenticadas
import time  # Para medir tempos de execução e realizar esperas

# Configuração de diretórios e modelo da API
# Substituir pelas pastas de entrada/saída desejadas antes de usar
pasta_entrada = "CAMINHO/DA/PASTA/ENTRADA"  # Insira o caminho dos PDFs a processar
pasta_saida = "CAMINHO/DA/PASTA/SAIDA"  # Insira o caminho para salvar as respostas
pasta_prompts = "CAMINHO/DA/PASTA/PROMPTS"  # Insira o caminho dos arquivos de prompts
modelo_gemini = "gemini-1.5-pro-002"  # Modelo do Google Gemini (ajuste se necessário)

# Configuração de credenciais
# Substituir pelo caminho correto para o arquivo JSON com as credenciais do Google antes de usar
caminho_arquivo_credenciais = "CAMINHO/PARA/ARQUIVO/CREDENCIAIS.JSON"
credenciais = service_account.Credentials.from_service_account_file(
    caminho_arquivo_credenciais,
    scopes=["https://www.googleapis.com/auth/generative-language"]
)

# Função para extrair texto de arquivos (PDF ou texto simples)
def extrair_texto(caminho, tipo):
    """
    Extrai o texto de um arquivo PDF ou texto simples (.txt ou .md).
    - caminho: caminho completo do arquivo.
    - tipo: "pdf" para PDFs, "txt" para arquivos de texto.
    """
    with open(caminho, "rb" if tipo == "pdf" else "r", encoding=None if tipo == "pdf" else "utf-8") as arq:
        if tipo == "pdf":
            return "".join(pagina.extract_text() for pagina in PyPDF2.PdfReader(arq).pages)
        return arq.read()

# Função para chamar a API do Google Gemini e obter a resposta
def consultar_api_gemini(conteudo, tentativas=3, espera=5):
    """
    Envia um texto para a API do Google Gemini e retorna a resposta.
    - conteudo: texto a ser processado pela API.
    - tentativas: número máximo de tentativas em caso de erro.
    - espera: tempo (em segundos) para aguardar entre tentativas.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo_gemini}:generateContent"
    credenciais.refresh(google.auth.transport.requests.Request())  # Atualiza o token de acesso
    headers = {
        "Authorization": f"Bearer {credenciais.token}",  # Token de autenticação
        "Content-Type": "application/json"  # Tipo de conteúdo JSON
    }
    dados = {"contents": [{"parts": [{"text": conteudo}]}]}  # Formato esperado pela API

    for tentativa in range(tentativas):  # Realiza múltiplas tentativas em caso de erro
        resposta = requests.post(url, headers=headers, json=dados)  # Envia a requisição
        if resposta.status_code == 200:  # Se a resposta for bem-sucedida, retorna o texto
            return resposta.json().get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if resposta.status_code == 503:  # Caso de sobrecarga no servidor
            print(f"Tentativa {tentativa + 1} falhou. Tentando novamente em {espera}s...")
            time.sleep(espera)
    print(f"Erro na API: {resposta.status_code} - {resposta.text}")
    return None  # Retorna None em caso de falha

# Função para processar um único PDF
def processar_pdf(nome_arquivo, prompt_completo):
    """
    Processa um único arquivo PDF, envia o conteúdo para a API e salva a resposta.
    - nome_arquivo: nome do arquivo PDF.
    - prompt_completo: prompt combinado com o conteúdo do arquivo.
    """
    caminho_pdf = os.path.join(pasta_entrada, nome_arquivo)  # Caminho completo do PDF
    caminho_saida = os.path.join(pasta_saida, f"{os.path.splitext(nome_arquivo)[0]}_RESPOSTA.txt")  # Caminho do TXT

    print(f"Processando {nome_arquivo}...")
    inicio = time.time()  # Marca o início do processamento

    # Extrai o texto do PDF e combina com o prompt
    texto = extrair_texto(caminho_pdf, "pdf")
    resposta = consultar_api_gemini(f"{prompt_completo}\n\nTexto do Documento:\n{texto}")  # Chama a API
    if resposta:  # Se houver resposta, salva em um arquivo de texto
        with open(caminho_saida, "w", encoding="utf-8") as saida:
            saida.write(resposta + "\n\n")

    # Calcula o tempo gasto no processamento
    print(f"Tempo para {nome_arquivo}: {int((time.time() - inicio) // 60)}m {int((time.time() - inicio) % 60)}s")

# Função principal para processar todos os PDFs
def processar_pdfs():
    """
    Processa todos os arquivos PDF na pasta de entrada, combinando com os prompts.
    """
    if not os.path.exists(pasta_saida):  # Cria a pasta de saída se não existir
        os.makedirs(pasta_saida)

    # Lê e combina o conteúdo de todos os arquivos de prompt
    prompt_completo = "".join(
        extrair_texto(os.path.join(pasta_prompts, arq), "pdf" if arq.endswith(".pdf") else "txt")
        for arq in os.listdir(pasta_prompts)
        if arq.endswith((".pdf", ".md", ".txt"))  # Filtra por tipos de arquivo suportados
    )

    # Marca o início do processamento total
    inicio_total = time.time()
    # Processa cada arquivo PDF encontrado na pasta de entrada
    for arquivo in filter(lambda f: f.endswith(".pdf"), os.listdir(pasta_entrada)):
        processar_pdf(arquivo, prompt_completo)

    # Calcula e exibe o tempo total de processamento
    tempo_total = time.time() - inicio_total
    print(f"Tempo total: {int(tempo_total // 60)}m {int(tempo_total % 60)}s")

# Início da execução
processar_pdfs()
