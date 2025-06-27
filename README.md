## Este projeto tem como objetivo demonstrar a automação de processos (RPA) com foco na transcrição de áudios via upload direto.

Inicialmente, a proposta incluía login com logs, histórico de transcrições e banco de dados. Porém, devido às restrições de linguagem e complexidade exigidas pela disciplina, o projeto foi simplificado.

A versão final conta com:

- Landing page única;

- Suporte a múltiplos idiomas;

- Upload de arquivos via drag and drop;

- Transcrição automatizada de áudios.

O foco está na lógica do algoritmo e na aplicação prática da automação, respeitando os limites propostos pelo curso.


# Sistema de Transcrição de Áudio Offline

Uma aplicação web simples em Python para transcrição de arquivos de áudio para texto utilizando reconhecimento de fala offline com PocketSphinx.

## Requisitos

- Python 3.6 ou superior
- Bibliotecas Python:
  - SpeechRecognition
  - PocketSphinx
  - PyAudio
  - pydub

## Instalação das Dependências no Windows

1. Instale as bibliotecas Python necessárias:

```bash
pip install SpeechRecognition pocketsphinx pyaudio pydub
```

2. Se encontrar problemas com o PyAudio, você pode baixar o arquivo .whl pré-compilado:
   - Acesse: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
   - Baixe o arquivo correspondente à sua versão do Python e arquitetura
   - Instale com: `pip install [caminho_do_arquivo_baixado]`

3. Para o pydub funcionar com arquivos MP3, instale o FFmpeg:
   - Baixe o FFmpeg do site oficial: https://ffmpeg.org/download.html
   - Extraia os arquivos e adicione a pasta bin ao PATH do sistema

## Execução

1. Execute o servidor Python:
```
python server.py
```

3. Acesse no navegador:
```
http://localhost:8000
```

## Uso

1. Acesse a página inicial
2. Arraste e solte um arquivo de áudio ou clique para selecionar
3. Escolha o idioma do áudio
4. Clique em "Transcrever"
5. Aguarde o processamento (pode demorar alguns segundos)
6. Visualize o texto transcrito

## Formatos Suportados

- WAV (.wav) - Melhor qualidade para reconhecimento
- MP3 (.mp3) - Requer FFmpeg instalado
- OGG (.ogg) - Requer FFmpeg instalado
- FLAC (.flac) - Requer FFmpeg instalado

## Limitações

- O reconhecimento offline tem precisão limitada comparado a serviços online
- Funciona melhor com áudio de boa qualidade e pouco ruído de fundo
- Arquivos longos podem levar mais tempo para processar
- O idioma padrão é o inglês americano, outros idiomas podem ter precisão reduzida

## Solução de Problemas

### Erro ao instalar PocketSphinx
- Verifique se você tem um compilador C instalado (Visual C++ no Windows)
- Tente instalar uma versão pré-compilada: `pip install --only-binary :all: pocketsphinx`

### Erro ao processar arquivos MP3/OGG/FLAC
- Verifique se o FFmpeg está instalado e no PATH do sistema
- Tente converter o arquivo para WAV antes de fazer o upload

### Baixa qualidade de reconhecimento
- Use arquivos de áudio com boa qualidade e pouco ruído de fundo
- Tente com arquivos WAV em vez de formatos comprimidos
- O reconhecimento offline tem limitações de precisão inerentes

## Vantagens desta Solução
- Funciona completamente offline, sem necessidade de internet
- Não requer chaves de API ou contas em serviços externos
- Privacidade garantida, pois o áudio é processado localmente
- Fácil de instalar e usar
- No mais,é tudo,atenciosamente seus alunos
