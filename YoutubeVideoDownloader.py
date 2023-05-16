import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import ImageTk, Image
from pytube import YouTube
from pytube.cli import on_progress

def descargar_video():
    url = entry_url.get()
    try:
        yt = YouTube(url, on_progress_callback=progreso_descarga)
        streams = yt.streams.filter(progressive=True)
        quality = combo_calidad.get()
        video = streams.get_by_resolution(quality)
        output_path = filedialog.askdirectory(title="Seleccione una carpeta de destino")
        if output_path:
            video.download(output_path=output_path)
            lbl_status.config(text="Descarga completada")
            lbl_ruta.config(text="Ruta de descarga: " + output_path)
            lbl_calidad.config(text="Calidad: " + video.resolution)
        else:
            lbl_status.config(text="Descarga cancelada")
            lbl_ruta.config(text="")
            lbl_calidad.config(text="")
    except Exception as e:
        lbl_status.config(text="Error en la descarga: " + str(e))

def progreso_descarga(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    lbl_progress.config(text="Progreso: {:.2f}%".format(percentage))

# Crear la ventana principal
window = tk.Tk()
window.title("Descargador de videos de YouTube")

# Obtener el tamaño de la pantalla
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calcular las coordenadas para centrar la ventana
x = (screen_width - 600) // 2
y = (screen_height - 400) // 2

# Establecer la posición de la ventana
window.geometry("600x400+{}+{}".format(x, y))
window.resizable(False, False)

# Agregar el logo de YouTube
logo_path = "logo.png"  # Ruta de la imagen del logo de YouTube
logo_image = Image.open(logo_path)
logo_image = logo_image.resize((100, 100), Image.LANCZOS)  # Utilizar Image.LANCZOS en lugar de Image.ANTIALIAS
logo = ImageTk.PhotoImage(logo_image)
lbl_logo = tk.Label(window, image=logo)
lbl_logo.pack()

# Crear los widgets
lbl_instrucciones = tk.Label(window, text="Ingrese el enlace del video de YouTube:")
lbl_instrucciones.pack()

entry_url = tk.Entry(window, width=50)
entry_url.pack()

lbl_calidad_instrucciones = tk.Label(window, text="Seleccione la calidad de descarga:")
lbl_calidad_instrucciones.pack()

combo_calidad = ttk.Combobox(window, values=["720p", "480p", "360p"], state="readonly")
combo_calidad.current(0)
combo_calidad.pack()

btn_descargar = tk.Button(window, text="Descargar", command=descargar_video)
btn_descargar.pack()

lbl_progress = tk.Label(window, text="Progreso: 0.00%")
lbl_progress.pack()

lbl_ruta = tk.Label(window, text="")
lbl_ruta.pack()

lbl_calidad = tk.Label(window, text="")
lbl_calidad.pack()

lbl_status = tk.Label(window, text="")
lbl_status.pack()

# Agregar el mensaje de copyright
label_copyright = tk.Label(window, text="Murallasoft by Joksan.Dev", fg="gray", font=("Helvetica", 10))
label_copyright.pack(side="bottom")

# Ejecutar la ventana principal
window.mainloop()
