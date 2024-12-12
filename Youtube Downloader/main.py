import tkinter as tk
from tkinter import ttk, messagebox
from pytube import YouTube
import os
import threading

class DescargadorYoutube:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de YouTube")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")

        # Marco principal
        self.marco = ttk.Frame(root, padding="10")
        self.marco.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # URL entrada
        ttk.Label(self.marco, text="URL del video:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entrada = ttk.Entry(self.marco, width=50)
        self.url_entrada.grid(row=1, column=0, columnspan=2, pady=5)

        # Selector de formato
        ttk.Label(self.marco, text="Formato:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.formato = tk.StringVar()
        self.formato_opciones = ttk.Combobox(self.marco, textvariable=self.formato, width=20)
        self.formato_opciones['values'] = ['Video MP4 (Alta Calidad)', 
                                         'Video MP4 (720p)',
                                         'Video MP4 (480p)',
                                         'Solo Audio (MP3)',
                                         'Solo Audio (MP4)']
        self.formato_opciones.current(0)
        self.formato_opciones.grid(row=2, column=1, pady=5)

        # Botón de descarga
        self.boton_descarga = ttk.Button(self.marco, text="Descargar", command=self.iniciar_descarga)
        self.boton_descarga.grid(row=3, column=0, pady=10)

        # Barra de progreso
        self.progreso = ttk.Progressbar(self.marco, length=400, mode='indeterminate')
        self.progreso.grid(row=4, column=0, columnspan=2, pady=10)

        # Área de información
        self.info_texto = tk.Text(self.marco, height=10, width=50)
        self.info_texto.grid(row=5, column=0, columnspan=2, pady=5)

    def iniciar_descarga(self):
        url = self.url_entrada.get()
        if not url:
            messagebox.showerror("Error", "Por favor, ingresa una URL")
            return

        self.boton_descarga.configure(state='disabled')
        self.progreso.start()
        
        thread = threading.Thread(target=self.descargar_video, args=(url,))
        thread.daemon = True
        thread.start()

    def descargar_video(self, url):
        try:
            yt = YouTube(url)
            self.actualizar_info(f"Título: {yt.title}\nVistas: {yt.views}\n")
            
            if not os.path.exists('descargas'):
                os.makedirs('descargas')

            formato_seleccionado = self.formato.get()
            
            if formato_seleccionado == 'Video MP4 (Alta Calidad)':
                stream = yt.streams.get_highest_resolution()
            elif formato_seleccionado == 'Video MP4 (720p)':
                stream = yt.streams.filter(res='720p', file_extension='mp4').first()
            elif formato_seleccionado == 'Video MP4 (480p)':
                stream = yt.streams.filter(res='480p', file_extension='mp4').first()
            elif formato_seleccionado == 'Solo Audio (MP3)':
                stream = yt.streams.filter(only_audio=True).first()
                # Descargar como MP4 y convertir a MP3
                archivo_mp4 = stream.download('descargas')
                base, ext = os.path.splitext(archivo_mp4)
                archivo_mp3 = base + '.mp3'
                os.rename(archivo_mp4, archivo_mp3)
                self.actualizar_info("¡Descarga completada exitosamente!")
                messagebox.showinfo("Éxito", "Audio descargado correctamente")
                return
            elif formato_seleccionado == 'Solo Audio (MP4)':
                stream = yt.streams.filter(only_audio=True).first()
            
            self.actualizar_info("Descargando...\n")
            stream.download('descargas')
            
            self.actualizar_info("¡Descarga completada exitosamente!")
            messagebox.showinfo("Éxito", "Archivo descargado correctamente")
            
        except Exception as e:
            self.actualizar_info(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            self.root.after(0, self.restaurar_interfaz)

    def actualizar_info(self, texto):
        self.root.after(0, lambda: self.info_texto.insert(tk.END, texto + "\n"))

    def restaurar_interfaz(self):
        self.boton_descarga.configure(state='normal')
        self.progreso.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = DescargadorYoutube(root)
    root.mainloop()
