# Projeto: **Automatização de Processamento de PDFs com Google Gemini**

Este projeto automatiza o processamento de arquivos PDF, utilizando inteligência artificial para extrair e interpretar informações através da API do Google Gemini. Ele combina textos extraídos de PDFs com prompts definidos para gerar respostas personalizadas, salvando-as em arquivos de texto.

## Funcionalidades
- **Extração de texto de PDFs**: Lê e processa documentos PDF para extrair seu conteúdo textual.
- **Integração com a API Google Gemini**: Envia conteúdos processados para a API e obtém respostas baseadas em inteligência artificial.
- **Gerenciamento de pastas**: Processa múltiplos arquivos de entrada e organiza as saídas em diretórios específicos.
- **Reutilização de prompts personalizados**: Combina conteúdo de documentos com prompts definidos pelo usuário.

## Como usar
1. **Configuração inicial**:
   - Instale as bibliotecas necessárias:
     ```bash
     pip install PyPDF2 requests google-auth
     ```
   - Configure sua conta Google Cloud:
     - Baixe o arquivo JSON com as credenciais da conta de serviço e insira o caminho no código.
   - Ajuste os diretórios (`pasta_entrada`, `pasta_saida`, `pasta_prompts`) conforme a localização dos seus arquivos.

2. **Preparar os arquivos**:
   - Coloque os PDFs na pasta de entrada.
   - Adicione prompts personalizados (em `.txt`, `.md`, ou `.pdf`) na pasta de prompts.

3. **Executar o script**:
   - Inicie o script:
     ```bash
     python Automação_IA.py
     ```
   - O processamento será executado e as respostas serão salvas na pasta de saída.

## Tecnologias usadas
- **Python**: Linguagem de programação principal do projeto.
- **PyPDF2**: Para leitura e extração de texto de PDFs.
- **Google Cloud API**: Autenticação e envio de requisições à API Google Gemini.
- **Requests**: Para envio de chamadas HTTP.
- **Google Auth**: Gerenciamento de credenciais para autenticação segura.

## Contribuição
Contribuições são bem-vindas! Para colaborar:
1. Faça um fork do repositório.
2. Crie uma branch para suas alterações:
   ```bash
   git checkout -b minha-nova-funcionalidade
