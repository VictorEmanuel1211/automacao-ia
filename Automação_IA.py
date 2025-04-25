import os
import time
import sys
import google.generativeai as genai
from pathlib import Path

# Diretórios principais do sistema
PASTA_ENTRADA = "C:\\..."  # Coloque aqui os arquivos PDF que deseja processar
PASTA_SAIDA = "C:\\..."  # As respostas geradas serão salvas aqui
PASTA_PROMPTS = "C:\\..."  # Coloque aqui os arquivos .txt com os prompts
PASTA_SYSTEM_INSTRUCTIONS = "C:\\..."  # Coloque aqui o arquivo .txt com as instruções do sistema

# API Key do Google Gemini
API_KEY = "DIGITE_SUA_API_KEY_AQUI"  # Substitua por sua chave de API

# Configuração dos parâmetros de geração do modelo
GENERATION_CONFIG = {
    "temperature": 0.5,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
}

def carregar_system_instructions():
    try:
        arquivos_txt = [f for f in os.listdir(PASTA_SYSTEM_INSTRUCTIONS) if f.endswith('.txt')]
        if not arquivos_txt:
            print("Nenhum arquivo de system instructions encontrado!")
            return None
        arquivo_instructions = arquivos_txt[0]
        caminho_completo = os.path.join(PASTA_SYSTEM_INSTRUCTIONS, arquivo_instructions)
        with open(caminho_completo, 'r', encoding='utf-8') as f:
            system_instructions = f.read()
            print(f"System instructions carregadas com sucesso de: {arquivo_instructions}")
            return system_instructions
    except Exception as e:
        print(f"Erro ao carregar system instructions: {e}")
        return None

def configurar_modelo():
    try:
        genai.configure(api_key=API_KEY)
        system_instructions = carregar_system_instructions()
        if system_instructions is None:
            raise Exception("Não foi possível carregar as system instructions")
        return genai.GenerativeModel(
            model_name="INSIRA_O_NOME_DO_MODELO_AQUI",  # Exemplo: "gemini-1.5-pro"
            generation_config=GENERATION_CONFIG,
            system_instruction=system_instructions
        )
    except Exception as e:
        print(f"Erro ao configurar o modelo: {e}")
        sys.exit(1)

def processar_pdf_com_gemini(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
        return {
            "mime_type": "application/pdf",
            "data": pdf_content
        }
    except Exception as e:
        print(f"Erro ao processar PDF: {e}")
        return None

def carregar_prompts():
    prompts = []
    arquivos_txt = sorted([
        arquivo for arquivo in os.listdir(PASTA_PROMPTS)
        if arquivo.endswith('.txt')
    ])
    for arquivo in arquivos_txt:
        caminho_completo = os.path.join(PASTA_PROMPTS, arquivo)
        try:
            with open(caminho_completo, 'r', encoding='utf-8') as f:
                prompts.append({
                    'nome': arquivo,
                    'conteudo': f.read()
                })
        except Exception as e:
            print(f"Erro ao ler o arquivo {arquivo}: {e}")
    return prompts

def chamar_api_gemini(chat_session, conteudo, documento, tentativas=3, espera=5):
    for tentativa in range(tentativas):
        try:
            response = chat_session.send_message([conteudo, documento])
            if response.text:
                return response.text
        except Exception as e:
            print(f"\nErro na tentativa {tentativa + 1}: {e}. Esperando {espera}s...")
            time.sleep(espera * (2 ** tentativa))
    print(f"\nErro na API após {tentativas} tentativas.")
    return None

def processar_pdf(nome_arquivo, prompts, model):
    caminho_pdf = os.path.join(PASTA_ENTRADA, nome_arquivo)
    nome_base = os.path.splitext(nome_arquivo)[0]
    caminho_saida = os.path.join(PASTA_SAIDA, f"{nome_base}_RESPOSTA.txt")
    if os.path.exists(caminho_saida):
        print(f"{nome_arquivo} já processado. Pulando...")
        return
    print(f"\nProcessando {nome_arquivo}...")
    inicio = time.time()
    documento = processar_pdf_com_gemini(caminho_pdf)
    if not documento:
        print(f"Falha ao processar o documento {nome_arquivo}")
        return
    chat_session = model.start_chat(history=[])
    todas_respostas = []
    for i, prompt in enumerate(prompts, 1):
        print(f"Aplicando prompt {i} de {len(prompts)}...")
        resposta = chamar_api_gemini(chat_session, prompt['conteudo'], documento)
        if resposta:
            todas_respostas.append(resposta + "\n\n\n\n")
    if todas_respostas:
        with open(caminho_saida, "w", encoding="utf-8") as saida:
            saida.write("".join(todas_respostas))
        print(f"Todas as respostas salvas em: {caminho_saida}")
    print(f"Tempo total para {nome_arquivo}: {int((time.time() - inicio) // 60)}m {int((time.time() - inicio) % 60)}s")

def processar_todos_pdfs():
    prompts = carregar_prompts()
    if not prompts:
        print("Nenhum prompt encontrado na pasta de prompts!")
        return
    inicio_total = time.time()
    arquivos = [f for f in os.listdir(PASTA_ENTRADA) if f.endswith(".pdf")]
    total_arquivos = len(arquivos)
    print(f"Encontrados {len(prompts)} prompts para processar.")
    model = configurar_modelo()
    for i, arquivo in enumerate(arquivos, 1):
        print(f"\nProcessando arquivo {i} de {total_arquivos}")
        processar_pdf(arquivo, prompts, model)
    tempo_total = time.time() - inicio_total
    print(f"\nTempo total: {int(tempo_total // 60)}m {int(tempo_total % 60)}s")
    print("Todos os processos foram finalizados com sucesso!")

if __name__ == "__main__":
    processar_todos_pdfs()
