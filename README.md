# Asistente Virtual en Python

Este proyecto es un asistente virtual en Python con múltiples funcionalidades, incluyendo procesamiento de texto, síntesis de voz, reconocimiento de voz, búsqueda de información y reproducción de música desde YouTube.

## Características Principales

### 1. Importaciones de Librerías
- **groq**: Interfaz para interactuar con modelos de lenguaje.
- **json, os**: Manejo de configuraciones y datos.
- **gTTS, playsound**: Síntesis de texto a voz y reproducción de audio.
- **tempfile**: Manejo de archivos temporales.
- **speech_recognition as sr**: Reconocimiento de voz desde el micrófono.
- **webbrowser, urllib.parse**: Manejo de búsquedas en la web.
- **pyperclip**: Acceso al portapapeles del sistema.
- **nltk**: Procesamiento de texto (tokenización, eliminación de palabras de parada).
- **collections.Counter**: Contar la frecuencia de palabras.
- **sumy**: Resumen de textos utilizando el algoritmo LSA.
- **youtubesearchpython**: Búsqueda de videos en YouTube.

### 2. Funciones Principales
- **analizar_texto_portapapeles**: Extrae texto del portapapeles, identifica palabras clave y genera un resumen.
- **identificar_palabras_clave**: Identifica palabras clave en un texto eliminando palabras comunes.
- **generar_resumen**: Genera un resumen del texto utilizando la librería sumy y el algoritmo LSA.
- **load_history, save_history**: Carga y guarda el historial de mensajes en un archivo JSON.
- **load_config, save_config**: Carga y guarda la configuración del asistente desde/hacia un archivo JSON.
- **text_to_speech**: Convierte texto a voz utilizando gTTS y reproduce el archivo generado.
- **recognize_speech**: Reconoce el habla del usuario desde el micrófono.
- **setup_initial_configuration**: Configura el asistente con datos iniciales proporcionados por el usuario.
- **get_ai_response**: Obtiene una respuesta del modelo de lenguaje.
- **buscar_informacion**: Busca información en la web y genera un resumen.
- **youtube_music**: Reproduce una canción de YouTube.
- **chat_with_bot**: Función principal que inicia el asistente, escucha comandos y responde en consecuencia.
- **es_pregunta**: Determina si el texto es una pregunta.

### 3. Configuración y Uso del Asistente
- **Configuración Inicial**: El asistente se configura al inicio, solicitando al usuario un saludo personalizado, el idioma preferido, la velocidad de habla, una frase de activación, y un nombre para el asistente.
- **Interacciones**: El asistente puede responder a diversas interacciones como análisis de texto, búsqueda de información, y reproducción de música.
- **Comunicación**: La comunicación con el usuario se realiza tanto a través de síntesis de voz como mediante respuestas textuales.

## Instalación y Uso

### Requisitos
- Python 3.x

### Instalación
1. Clona el repositorio:
   ```bash
   git clone https://github.com/tuusuario/nombre-repositorio.git
   cd nombre-repositorio
   pip install groq gtts playsound SpeechRecognition pyperclip nltk sumy youtubesearchpython requests
