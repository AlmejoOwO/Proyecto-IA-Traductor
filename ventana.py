from tkinter import *  
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
from langdetect import detect
from googletrans import Translator
from tkinter import PhotoImage
# Idiomas soportados por Google Translate
idiomas_soportados = {
    'español': 'es', 'inglés': 'en', 'francés': 'fr', 'alemán': 'de', 'italiano': 'it',
    'portugués': 'pt', 'japonés': 'ja', 'chino': 'zh-cn', 'ruso': 'ru', 'árabe': 'ar',
    'holandés': 'nl', 'polaco': 'pl', 'coreano': 'ko', 'turco': 'tr', 'sueco': 'sv'
}

#Funcion de inico de proceso
def iniciar_proceso():
  
    r = sr.Recognizer()
    
    try:
        # Escuchar el primer mensaje
        label_estado.config(text="Di algo...")
        ventana.update()
        with sr.Microphone() as source:
            audio = r.listen(source)
        
        # Transcribir el audio
        texto = r.recognize_google(audio)
        label_estado.config(text=f"Transcripción: {texto}")
        ventana.update()

        # Detectar idioma
        idioma = detect(texto)
        label_resultado.config(text=f"Idioma detectado: {idioma}")
        ventana.update()

        # Pedir idioma de destino
        label_estado.config(text="Di el nombre del idioma al que deseas traducir:")
        ventana.update()
        with sr.Microphone() as source:
            audio_idioma = r.listen(source)
            idioma_seleccionado = r.recognize_google(audio_idioma).lower()

        idioma_destino = idiomas_soportados.get(idioma_seleccionado)  
        label_resultado.config(text=f"Idioma destino seleccionado: {idioma_seleccionado.capitalize()}")
        ventana.update()

        # Traductor del texto
        traductor = Translator()
        traduccion = traductor.translate(texto, src=idioma, dest=idioma_destino)
        texto_traduccion = f"Texto original: {texto}\nTraducción al {idioma_seleccionado.capitalize()}: {traduccion.text}"
        label_resultado.config(text=texto_traduccion)
    
    except sr.UnknownValueError:
        label_resultado.config(text="No pude entender lo que dijiste.")
    except sr.RequestError as e:
        label_resultado.config(text=f"Error: {e}")

# Ventana principal
ventana = tk.Tk()
ventana.title("Traducción y Reconocimiento")
ventana.geometry("500x400")

# Cargar la imagen de fondo
try:
    img_fondo = PhotoImage(file="sonido-de-onda.png")  
except Exception as e:
    print(f"Error al cargar la imagen de fondo: {e}")
    img_fondo = None  

if img_fondo:
    # Configurar imagen de fondo
    fondo_label = tk.Label(ventana, image=img_fondo)
    fondo_label.place(relwidth=1, relheight=1)  

# Crear un marco para los widgets (encima de la imagen de fondo)
frame_widgets = tk.Frame(ventana, bg="white", bd=0, highlightthickness=0)
frame_widgets.place(relx=0.5, rely=0.5, anchor="center")  

# Etiqueta de estado
label_estado = tk.Label(frame_widgets, text="Haz clic en 'Iniciar' para comenzar.", font=("Arial", 14), wraplength=450, justify="center", bg="white")
label_estado.pack(pady=20)

# Etiqueta para los resultados
label_resultado = tk.Label(frame_widgets, text="", font=("Arial", 12), wraplength=450, justify="left", bg="white")
label_resultado.pack(pady=20)

# Botón para iniciar el proceso
try:
    imagen_boton = PhotoImage(file="IA.png") 
    boton_iniciar = tk.Button(frame_widgets, image=imagen_boton, command=iniciar_proceso, borderwidth=0)
except Exception as e:
    print(f"Error al cargar la imagen del botón: {e}")
    boton_iniciar = tk.Button(frame_widgets, text="Iniciar", font=("Arial", 12), command=iniciar_proceso)
boton_iniciar.pack(pady=20)

# Mostrar la ventana
ventana.mainloop()
