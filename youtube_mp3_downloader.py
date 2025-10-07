#!/usr/bin/env python3
"""
Script para descargar videos de YouTube en formato MP3 desde un archivo videos.md
Utiliza yt-dlp para la descarga y conversión
"""

import os
import re
import sys
from pathlib import Path
import yt_dlp

# Importar tkinter para la ventana de prompt
try:
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False
    print("Advertencia: tkinter no está disponible. Se usará entrada por consola.")


def extract_youtube_urls(file_path):
    """
    Extrae las URLs de YouTube del archivo especificado
    Solo procesa líneas que comienzan con https
    """
    youtube_urls = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Filtrar solo líneas que comienzan con https y unirlas
        filtered_lines = [line for line in lines if line.strip().startswith('https')]
        content = ''.join(filtered_lines)
            
        # Expresión regular para encontrar URLs de YouTube
        youtube_pattern = r'https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+'
        urls = re.findall(youtube_pattern, content)
        
        # Limpiar URLs quitando parámetros adicionales de lista
        for url in urls:
            # Extraer solo la parte básica del video
            if 'youtube.com/watch?v=' in url:
                video_id = re.search(r'v=([^&]+)', url)
                if video_id:
                    clean_url = f"https://www.youtube.com/watch?v={video_id.group(1)}"
                    youtube_urls.append(clean_url)
            else:
                youtube_urls.append(url)
                
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo {file_path}")
        return []
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return []
    
    return list(set(youtube_urls))  # Eliminar duplicados


def download_mp3(url, output_dir="downloads"):
    """
    Descarga un video de YouTube y lo convierte a MP3
    """
    # Crear directorio de salida si no existe
    Path(output_dir).mkdir(exist_ok=True)
    
    # Configuración para yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'postprocessor_args': [
            '-ar', '44100'
        ],
        'prefer_ffmpeg': True,
        'keepvideo': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Obtener información del video
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Título desconocido')
            duration = info.get('duration', 0)
            
            print(f"Descargando: {title}")
            print(f"Duración: {duration // 60}:{duration % 60:02d}")
            
            # Descargar el video
            ydl.download([url])
            print(f"✓ Descarga completada: {title}")
            
    except Exception as e:
        print(f"✗ Error al descargar {url}: {e}")


def get_url_from_prompt():
    """
    Muestra una ventana de prompt para pedir la URL de YouTube
    """
    if HAS_TKINTER:
        # Crear ventana raíz oculta
        root = tk.Tk()
        root.withdraw()
        
        # Mostrar ventana de entrada
        url = simpledialog.askstring(
            "YouTube MP3 Downloader",
            "Introduce la URL de YouTube (deja vacío para usar videos.md):",
            parent=root
        )
        
        root.destroy()
        return url
    else:
        # Fallback a consola si tkinter no está disponible
        print("\n🎵 YouTube MP3 Downloader")
        print("=" * 40)
        url = input("Introduce la URL de YouTube (presiona Enter para usar videos.md): ").strip()
        return url if url else None


def main():
    """
    Función principal
    """
    print("🎵 YouTube MP3 Downloader")
    print("=" * 40)
    
    # Pedir URL al usuario
    url_input = get_url_from_prompt()
    
    urls = []
    
    if url_input and url_input.strip():
        # Usar la URL proporcionada
        urls = [url_input.strip()]
        print(f"Usando URL proporcionada: {url_input}")
    else:
        # Usar el archivo videos.txt
        videos_file = "videos.txt"
        
        # Verificar si el archivo existe
        if not os.path.exists(videos_file):
            print(f"Error: No se encontró el archivo {videos_file}")
            if HAS_TKINTER and HAS_TKINTER:
                messagebox.showerror("Error", f"No se encontró el archivo {videos_file}")
            sys.exit(1)
        
        # Extraer URLs del archivo
        print(f"Usando URLs desde {videos_file}...")
        urls = extract_youtube_urls(videos_file)
        
        if not urls:
            print("No se encontraron URLs de YouTube válidas en el archivo.")
            if HAS_TKINTER:
                messagebox.showwarning("Advertencia", "No se encontraron URLs válidas en videos.md")
            sys.exit(1)
        
        print(f"Se encontraron {len(urls)} URLs de YouTube:")
        for i, url in enumerate(urls, 1):
            print(f"  {i}. {url}")
    
    print("\nIniciando descargas...")
    print("-" * 40)
    
    # Crear directorio de descargas
    download_dir = "downloads"
    Path(download_dir).mkdir(exist_ok=True)
    
    # Descargar cada video
    successful_downloads = 0
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Procesando...")
        try:
            download_mp3(url, download_dir)
            successful_downloads += 1
        except KeyboardInterrupt:
            print("\n\nDescarga interrumpida por el usuario.")
            break
        except Exception as e:
            print(f"Error inesperado: {e}")
    
    print("\n" + "=" * 40)
    print(f"Proceso completado!")
    print(f"Descargas exitosas: {successful_downloads}/{len(urls)}")
    print(f"Archivos guardados en: {os.path.abspath(download_dir)}")
    
    if HAS_TKINTER and successful_downloads > 0:
        messagebox.showinfo("Completado", f"Descarga completada!\nArchivos guardados en: {download_dir}")


if __name__ == "__main__":
    main()
