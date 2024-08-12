import groq
import json
import os
from gtts import gTTS
from playsound import playsound
import tempfile
import speech_recognition as sr
import webbrowser
import urllib.parse
import pyperclip
import nltk
from fuzzywuzzy import process
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
from GoogleNews import GoogleNews
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from youtubesearchpython import VideosSearch


CONFIG_FILE_PATH = 'config.json'

# Descarga de recursos necesarios para nltk
nltk.download('punkt')
nltk.download('stopwords')

# Inicializar GoogleNews
googlenews = GoogleNews()

IDIOMA_CODIGOS = {
    'español': 'es',
    'inglés': 'en',
    'francés': 'fr',
    'alemán': 'de',
    'italiano': 'it',
    'portugués': 'pt',
    'japonés': 'ja',
    'chino': 'zh',
    'ruso': 'ru',
    'árabe': 'ar'
}

# Define las acciones y sus posibles frases clave
acciones = {
    'buscar_informacion': ['busca', 'buscar', 'encuentra', 'investiga'],
    'analizar_texto': ['analiza este texto', 'revisa el texto', 'analiza texto'],
    'reproducir_musica': ['reproduce', 'escucha', 'pon', 'reproduce música'],
    'obtener_noticias': ['muéstrame noticias sobre', 'dame noticias sobre', 'noticias sobre'],
    'conversemos': ['hablemos sobre', 'platicame sobre','oye', 'qué opinas','ayudame']
}


def analizar_texto_portapapeles():
    """Analiza el texto actualmente en el portapapeles, identificando temas y resumiendo."""
    try:
        texto = pyperclip.paste()
        if texto:
            # Identificar palabras clave
            palabras_clave = identificar_palabras_clave(texto)
            palabras_clave_str = ", ".join(palabras_clave)
            
            # Generar resumen
            resumen = generar_resumen(texto)
            
            # Resultado del análisis
            resultado = f"Palabras clave: {palabras_clave_str}\nResumen: {resumen}"
            print(resultado)
            return resultado
        else:
            print("El portapapeles está vacío.")
            return "No hay texto en el portapapeles para analizar."
    except Exception as e:
        print(f"Error al acceder al portapapeles: {e}")
        return "Hubo un error al acceder al portapapeles."

def identificar_palabras_clave(texto):
    """Identifica palabras clave en el texto."""
    stop_words = set(stopwords.words('spanish'))
    word_tokens = word_tokenize(texto.lower())
    filtered_words = [word for word in word_tokens if word.isalnum() and word not in stop_words]
    frecuencia = Counter(filtered_words)
    palabras_clave = [palabra for palabra, count in frecuencia.most_common(10)]
    return palabras_clave

def generar_resumen(texto):
    parser = PlaintextParser.from_string(texto, Tokenizer("spanish"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Número de oraciones en el resumen
    return " ".join([str(sentence) for sentence in summary])

def load_history(file_path):
    """Carga el historial de mensajes desde un archivo JSON."""
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return []

def save_history(file_path, history):
    """Guarda el historial de mensajes en un archivo JSON."""
    with open(file_path, 'w') as file:
        json.dump(history, file, indent=4)

def load_config():
    """Carga la configuración desde un archivo JSON."""
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r') as file:
            return json.load(file)
    return None

def save_config(config):
    """Guarda la configuración en un archivo JSON."""
    with open(CONFIG_FILE_PATH, 'w') as file:
        json.dump(config, file, indent=4)

def text_to_speech(text, lang='es', slow=False):
    """Convierte el texto a habla y reproduce el sonido."""
    tts = gTTS(text=text, lang=lang, slow=slow)
    with tempfile.NamedTemporaryFile(delete=True) as temp_file:
        temp_file_path = temp_file.name + '.mp3'
        tts.save(temp_file_path)
        playsound(temp_file_path)

def recognize_speech():
    """Reconoce el texto del audio del micrófono."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Ajustando ruido...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Escuchando...")
        audio = recognizer.listen(source)

        try:
            # Usar el servicio de Google para el reconocimiento de voz
            text = recognizer.recognize_google(audio, language='es-ES')
            print("Texto reconocido:", text)
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio.")
            return None
        except sr.RequestError as e:
            print(f"Error con el servicio de Google Speech Recognition: {e}")
            return None

def setup_initial_configuration():
    """Configura el asistente por primera vez mediante comandos de voz."""
    config = {}

    while True:
        text_to_speech("Bienvenido. Vamos a configurar el asistente. Dime tu saludo personalizado.")
        print("Dime tu saludo personalizado:")
        personal_greeting = recognize_speech()
        if personal_greeting:
            config['personal_greeting'] = personal_greeting
            break
        else:
            text_to_speech("No entendí el saludo. Por favor, repite tu saludo personalizado.")
    
    while True:
        text_to_speech("¿En qué idioma prefieres que te hable? Dime el nombre del idioma, como español o inglés.")
        print("Dime el nombre del idioma que prefieres (español, inglés, etc.):")
        lang_name = recognize_speech()
        if lang_name:
            lang_name = lang_name.lower()
            if lang_name in IDIOMA_CODIGOS:
                config['language'] = IDIOMA_CODIGOS[lang_name]
                break
            else:
                text_to_speech(f"Idioma {lang_name} no soportado. Por favor, elige otro idioma.")
        else:
            text_to_speech("No entendí el idioma. Por favor, repite el nombre del idioma.")
    
    while True:
        text_to_speech("¿Prefieres una velocidad de habla lenta? Responde sí o no.")
        print("¿Prefieres una velocidad de habla lenta? (sí/no):")
        slow_speech_response = recognize_speech()
        if slow_speech_response:
            slow_speech_response = slow_speech_response.lower()
            if slow_speech_response in ['sí', 'si', 'no', 'yes', 'y', 'no']:
                config['slow_speech'] = slow_speech_response in ['sí', 'si', 'yes', 'y']
                break
            else:
                text_to_speech("Respuesta no reconocida. Por favor, responde sí o no.")
        else:
            text_to_speech("No entendí tu respuesta. Por favor, responde sí o no.")
    
    while True:
        text_to_speech("Por favor, dime la frase de activación para iniciar una conversación conmigo.")
        print("Dime la frase de activación:")
        activation_phrase = recognize_speech()
        if activation_phrase:
            config['activation_phrase'] = activation_phrase.lower()
            break
        else:
            text_to_speech("No entendí la frase de activación. Por favor, repítela.")
    
    while True:
        text_to_speech("Por último, dime el nombre que quieres darme.")
        print("Dime el nombre del asistente:")
        assistant_name = recognize_speech()
        if assistant_name:
            config['assistant_name'] = assistant_name.lower()
            break
        else:
            text_to_speech("No entendí el nombre. Por favor, repítelo.")

    save_config(config)
    return config

def get_ai_response(client, messages):
    """Obtiene la respuesta del modelo AI utilizando Groq."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages,
            temperature=0.7,
            stream=True,
        )
        response = "".join(chunk.choices[0].delta.content or "" for chunk in completion)
        return response
    except Exception as e:
        print(f"Error al obtener la respuesta de AI: {e}")
        return "Hubo un error al obtener la respuesta."

def buscar_informacion(tema, client, lang='es'):
    """Busca información sobre un tema, abre pestañas del navegador y genera un resumen."""
    # Buscar en el navegador
    base_url = "https://www.google.com/search?q="
    query = urllib.parse.quote(tema)
    search_urls = [f"{base_url}{query}&start={i * 10}" for i in range(5)]
    for url in search_urls:
        webbrowser.open_new_tab(url)

    # Generar resumen utilizando la API de Groq
    summary_prompt = f"Resumen breve en {lang} sobre: {tema}"
    messages = [{'role': 'user', 'content': summary_prompt}]
    resumen = get_ai_response(client, messages)
    return resumen

def youtube_music(cancion):
    # Realizar búsqueda en YouTube y obtener el primer resultado
    videos_search = VideosSearch(cancion, limit=1)
    results = videos_search.result()
    
    # Obtener la URL del primer video
    video_url = results['result'][0]['link']
      
    # Abrir el video en el navegador predeterminado
    webbrowser.open(video_url)
    
    return text_to_speech("Disfruta la reproducción")

def obtener_ultimas_noticias(tema):
    # Buscar noticias sobre el tema
    googlenews.search(tema)
    
    # Obtener resultados de búsqueda
    resultados = googlenews.results(sort=True)
    
    cadena_total = ""
    
    # Mostrar noticias (limitado a 7 resultados)
    for i, noticia in enumerate(resultados[:7]):  # Limitar a los primeros 7 resultados
        # Crear la cadena para esta iteración y acumularla en cadena_total
        cadena = f"{i}. {noticia.get('title', 'No disponible')}\n{noticia.get('media', 'No disponible')}\n{noticia.get('desc', 'No disponible')}\n\n"
        cadena_total += cadena
    
    print(cadena_total)
    
    for noticia in resultados[:7]:  # Limitar a los primeros 7 resultados
        webbrowser.open(noticia.get('link'))
        
    return cadena_total

def determinar_accion(entrada):
    """Determina la acción más probable basada en la entrada del usuario."""
    entrada = entrada.lower()
    mejor_puntuacion = 0
    accion_elegida = None

    for accion, frases in acciones.items():
        for frase in frases:
            puntuacion = process.extractOne(entrada, [frase])[1]
            if puntuacion > mejor_puntuacion:
                mejor_puntuacion = puntuacion
                accion_elegida = accion

    return accion_elegida


def chat_with_bot():
    file_path = 'chat_history.json'
    api_key = "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"

    client = groq.Groq(api_key=api_key)
    messages = load_history(file_path)
    config = load_config()
    if config is None:
        config = setup_initial_configuration()

    personal_greeting = config.get('personal_greeting', 'Hola')
    lang = config.get('language', 'es')
    slow_speech = config.get('slow_speech', False)
    activation_phrase = config.get('activation_phrase', 'hey asistente')
    assistant_name = config.get('assistant_name', 'asistente')

    text_to_speech(personal_greeting, lang=lang, slow=slow_speech)
    print(personal_greeting)
    
    en_modo_respuesta = False

    while True:
        try:
            if en_modo_respuesta:
                print("Esperando respuesta...")
            else:
                print(f"Esperando la frase de activación '{activation_phrase}' o el nombre '{assistant_name}'...")
            
            user_input = recognize_speech()
            
            if user_input is None:
                continue

            if en_modo_respuesta or (activation_phrase in user_input.lower() or assistant_name in user_input.lower()):
                user_input = user_input.lower().replace(activation_phrase, "").replace(assistant_name, "").strip()

                if user_input.lower() in ['salir', 'exit', 'adios', 'adiós']:
                    text_to_speech("Hasta luego", lang=lang, slow=slow_speech)
                    print("¡Hasta luego!")
                    save_history(file_path, messages)
                    break
                
                accion = determinar_accion(user_input)
                
                if accion == 'buscar_informacion':
                    tema = user_input.split('sobre')[-1].strip()
                    text_to_speech(f"Buscando información sobre {tema}", lang=lang, slow=slow_speech)
                    buscar_informacion(tema, client, lang)
                    resumen = buscar_informacion(tema, client, lang)
                    print(f"Resumen sobre {tema}: {resumen}")
                    text_to_speech(resumen, lang=lang, slow=slow_speech)
                    en_modo_respuesta = False
                    continue

                if accion == 'analizar_texto':
                    texto_analizado = analizar_texto_portapapeles()
                    text_to_speech(f"Texto analizado: {texto_analizado}", lang=lang, slow=slow_speech)
                    print(f"Texto analizado: {texto_analizado}")
                    en_modo_respuesta = False
                    continue
                
                if accion == 'reproducir_musica':
                    cancion = user_input.split('música')[-1].strip()
                    youtube_music(cancion)
                    continue
                
                if accion == 'obtener_noticias':
                    topic = user_input.split('sobre')[-1].strip()
                    noticias = obtener_ultimas_noticias(topic)
                    text_to_speech(noticias, lang=lang, slow=slow_speech)
                    continue
                
                if accion == 'conversemos':
                    messages.append({'role': 'user', 'content': user_input})
                    bot_message = get_ai_response(client, messages)
                    print(f"{assistant_name.capitalize()}:", bot_message)
                    text_to_speech(bot_message, lang=lang, slow=slow_speech)
                    messages.append({'role': 'assistant', 'content': bot_message})
                    en_modo_respuesta = es_pregunta(bot_message)
            else:
                print(f"No se detectó la frase de activación '{activation_phrase}' o el nombre '{assistant_name}'.")
                en_modo_respuesta = False

        except Exception as e:
            print(f"Ocurrió un error: {e}")
            text_to_speech("Ocurrió un error. Por favor, inténtalo de nuevo.", lang=lang, slow=slow_speech)

def es_pregunta(texto):
    """Determina si el texto es una pregunta."""
    return texto.strip().endswith('?')

if __name__ == "__main__":
    chat_with_bot()