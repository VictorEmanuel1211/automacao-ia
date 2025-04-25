# Projeto: **Automatização de PDFs com Prompts e Google Gemini**

Este projeto automatiza o processamento de arquivos PDF utilizando inteligência artificial com a API do **Google Gemini**. Ele combina documentos PDF com instruções de sistema e prompts personalizados, gerando respostas baseadas em IA e salvando os resultados automaticamente.

## Funcionalidades
- **Envio de PDFs para o modelo Gemini**: Envia arquivos PDF diretamente para a API da Google.
- **Aplicação de múltiplos prompts**: Usa arquivos `.txt` como prompts personalizados.
- **System Instructions configuráveis**: Define instruções de sistema para guiar o comportamento da IA.
- **Processamento em lote**: Lê todos os PDFs da pasta de entrada e salva cada resposta individualmente.
- **Retentativas automáticas com espera exponencial** em caso de falha de conexão com a API.

## Como usar

### 1. **Instalar as dependências**
```bash
pip install google-generativeai
```

### 2. **Preparar os diretórios**
- **PASTA_ENTRADA**: coloque aqui os arquivos PDF que deseja processar.
- **PASTA_PROMPTS**: adicione aqui arquivos `.txt` com os prompts que serão enviados para o modelo.
- **PASTA_SYSTEM_INSTRUCTIONS**: adicione um arquivo `.txt` com instruções gerais para orientar o modelo Gemini.
- **PASTA_SAIDA**: as respostas geradas serão salvas aqui com o mesmo nome do PDF original + `_RESPOSTA.txt`.

### 3. **Configurar o script**
Abra o código e altere as seguintes partes:
- Substitua `"DIGITE_SUA_API_KEY_AQUI"` pela sua chave da API Gemini.
- Substitua `"INSIRA_O_NOME_DO_MODELO_AQUI"` pelo modelo desejado (exemplo: `"gemini-1.5-pro"`).

### 4. **Executar**
```bash
python seu_script.py
```

O script processará todos os arquivos PDF encontrados na pasta de entrada, aplicará os prompts um a um e salvará as respostas.

## Tecnologias usadas
- **Python**: Linguagem principal do projeto.
- **Google Generative AI SDK (`google-generativeai`)**: Para integração com o modelo Gemini.
- **Standard Library (`os`, `time`, `sys`)**: Para manipulação de arquivos, controle de fluxo e tratamento de erros.

## Estrutura recomendada de pastas

```
Automacao_Tribunal/
├── pnf/                     # PDFs de entrada
├── pf/                      # Saídas com respostas geradas
├── prompts/                 # Prompts .txt para o modelo
├── system_instructions/     # Instruções de sistema (.txt)
├── seu_script.py            # Script principal
```

## Contribuição

Contribuições são bem-vindas! Para colaborar:

1. Faça um fork do repositório.
2. Crie uma branch com sua funcionalidade:
   ```bash
   git checkout -b minha-funcionalidade
   ```
3. Envie um pull request com uma descrição clara do que foi alterado.
