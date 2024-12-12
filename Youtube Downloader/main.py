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

        # Botón de descarga
        self.boton_descarga = ttk.Button(self.marco, text="Descargar", command=self.iniciar_descarga)
        self.boton_descarga.grid(row=2, column=0, pady=10)

        # Barra de progreso
        self.progreso = ttk.Progressbar(self.marco, length=400, mode='indeterminate')
        self.progreso.grid(row=3, column=0, columnspan=2, pady=10)

        # Área de información
        self.info_texto = tk.Text(self.marco, height=10, width=50)
        self.info_texto.grid(row=4, column=0, columnspan=2, pady=5)

    def iniciar_descarga(self):
        url = self.url_entrada.get()
        if not url:
            messagebox.showerror("Error", "Por favor, ingresa una URL")
            return

        # Deshabilitar botón durante la descarga
        self.boton_descarga.configure(state='disabled')
        self.progreso.start()
        
        # Iniciar descarga en un hilo separado
        thread = threading.Thread(target=self.descargar_video, args=(url,))
        thread.daemon = True
        thread.start()

    def descargar_video(self, url):
        try:
            # Crear objeto YouTube
            yt = YouTube(url)
            
            # Mostrar información
            self.actualizar_info(f"Título: {yt.title}\nVistas: {yt.views}\n")
            
            # Crear carpeta si no existe
            if not os.path.exists('descargas'):
                os.makedirs('descargas')
            
            # Descargar video
            video = yt.streams.get_highest_resolution()
            self.actualizar_info("Descargando...\n")
            video.download('descargas')
            
            self.actualizar_info("¡Descarga completada exitosamente!")
            messagebox.showinfo("Éxito", "Video descargado correctamente")
            
        except Exception as e:
            self.actualizar_info(f"Error: {str(e)}")
            messagebox.showerror("Error", str(e))
        
        finally:
            # Restaurar interfaz
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
