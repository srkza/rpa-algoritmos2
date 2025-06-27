import http.server
import socketserver
import json
import os
import uuid
import time
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Configurações
PORT = 8000
UPLOAD_DIR = "uploads"

# Garantir que a pasta de uploads existe
os.makedirs(UPLOAD_DIR, exist_ok=True)

class TranscriptionHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            # Servir arquivos estáticos
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/upload':
            # Obter o tamanho do conteúdo
            content_length = int(self.headers['Content-Length'])
            
            # Obter o tipo de conteúdo e o boundary
            content_type = self.headers['Content-Type']
            
            if 'multipart/form-data' in content_type:
                # Ler os dados do corpo da requisição
                post_data = self.rfile.read(content_length)
                
                # Encontrar o boundary
                boundary = content_type.split('=')[1].encode()
                
                # Processar os dados multipart
                parts = post_data.split(boundary)
                
                # Variáveis para armazenar os dados do formulário
                audio_file_data = None
                audio_file_name = None
                language = "pt-BR"  # Valor padrão
                
                # Processar cada parte
                for part in parts:
                    if b'name="audio_file"' in part and b'filename="' in part:
                        # Extrair o nome do arquivo
                        filename_start = part.find(b'filename="') + 10
                        filename_end = part.find(b'"', filename_start)
                        audio_file_name = part[filename_start:filename_end].decode()
                        
                        # Encontrar o início do conteúdo do arquivo
                        content_start = part.find(b'\r\n\r\n') + 4
                        content_end = part.rfind(b'\r\n')
                        
                        # Extrair o conteúdo do arquivo
                        audio_file_data = part[content_start:content_end]
                    
                    elif b'name="language"' in part:
                        # Extrair o valor do idioma
                        content_start = part.find(b'\r\n\r\n') + 4
                        content_end = part.rfind(b'\r\n')
                        language = part[content_start:content_end].decode()
                
                # Verificar se o arquivo foi enviado
                if not audio_file_data or not audio_file_name:
                    self.send_error_response('Nenhum arquivo enviado')
                    return
                
                # Verificar extensão do arquivo
                file_ext = os.path.splitext(audio_file_name)[1].lower()
                if file_ext not in ['.wav', '.mp3', '.ogg', '.flac']:
                    self.send_error_response('Formato de arquivo não suportado. Use WAV, MP3, OGG ou FLAC.')
                    return
                
                # Salvar o arquivo
                filename = f"{uuid.uuid4()}{file_ext}"
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, 'wb') as f:
                    f.write(audio_file_data)
                
                try:
                    # Transcrever o áudio usando reconhecimento offline
                    transcription = self.transcribe_audio_offline(filepath, language)
                    
                    # Enviar resposta
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    
                    response = {
                        'success': True,
                        'transcription': transcription
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                except Exception as e:
                    self.send_error_response(f'Erro ao processar arquivo: {str(e)}')
                
                # Limpar o arquivo após o processamento
                try:
                    os.remove(filepath)
                except:
                    pass
            else:
                self.send_error_response('Tipo de conteúdo não suportado')
    
    def transcribe_audio_offline(self, filepath, language):
        """
        Transcreve o áudio usando reconhecimento offline com Sphinx
        """
        # Inicializar o reconhecedor
        recognizer = sr.Recognizer()
        
        # Converter para WAV se necessário
        if not filepath.endswith('.wav'):
            sound = AudioSegment.from_file(filepath)
            wav_filepath = filepath.rsplit('.', 1)[0] + '.wav'
            sound.export(wav_filepath, format="wav")
            filepath = wav_filepath
        
        # Carregar o arquivo de áudio
        with sr.AudioFile(filepath) as source:
            # Ajustar para ruído ambiente
            recognizer.adjust_for_ambient_noise(source)
            # Capturar o áudio
            audio = recognizer.record(source)
        
        try:
            # Usar Sphinx para reconhecimento offline
            text = recognizer.recognize_sphinx(audio, language=language)
            return text
        except sr.UnknownValueError:
            return "Não foi possível entender o áudio"
        except sr.RequestError as e:
            return f"Erro no serviço de reconhecimento: {e}"
    
    def send_error_response(self, message):
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            'success': False,
            'error': message
        }
        self.wfile.write(json.dumps(response).encode())

print(f"Iniciando RPA  na porta {PORT}...")
print(f"Acesse http://localhost:{PORT} no navegador")
with socketserver.TCPServer(("", PORT), TranscriptionHandler) as httpd:
    httpd.serve_forever()
