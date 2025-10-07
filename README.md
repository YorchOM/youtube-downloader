# YouTube MP3 Downloader

Este script descarga videos de YouTube y los convierte a formato MP3 basándose en las URLs contenidas en el archivo `videos.md`.

## 🚀 Ejecución Rápida

**Para ejecutar el script (si ya tienes todo configurado):**

```powershell
# 1. Activar el entorno virtual
.\.venv\Scripts\Activate.ps1

# 2. Ejecutar el script
python .\youtube_mp3_downloader.py
```

## Requisitos

- Python 3.7+
- FFmpeg (para conversión de audio)

## 📦 Instalación Completa

1. **Instalar FFmpeg:**
   
   **En Windows:**
   - Descarga FFmpeg desde: https://ffmpeg.org/download.html
   - Extrae el archivo y agrega la carpeta `bin` al PATH del sistema
   
   **O usando Chocolatey:**
   ```powershell
   choco install ffmpeg
   ```
   
   **O usando winget:**
   ```powershell
   winget install FFmpeg
   ```

2. **Configurar entorno virtual y dependencias:**
   ```powershell
   # Crear entorno virtual (si no existe)
   python -m venv .venv
   
   # Activar entorno virtual
   .\.venv\Scripts\Activate.ps1
   
   # Instalar dependencias
   pip install -r requirements.txt
   ```

## 📖 Uso

1. **Preparar archivo de URLs:**
   - Asegúrate de que el archivo `videos.md` contenga las URLs de YouTube que deseas descargar
   - Solo las líneas que comienzan con `https` serán procesadas
   - Ejemplo:
   ```markdown
   # Mis videos favoritos
   
   https://www.youtube.com/watch?v=VIDEO_ID1
   https://www.youtube.com/watch?v=VIDEO_ID2
   https://youtu.be/VIDEO_ID3
   
   ## Notas
   Esta línea será ignorada porque no comienza con https
   ```

2. **Ejecutar el script:**
   ```powershell
   # Activar entorno virtual
   .\.venv\Scripts\Activate.ps1
   
   # Ejecutar script
   python .\youtube_mp3_downloader.py
   ```

## ✨ Características

- ✅ Extrae automáticamente URLs de YouTube del archivo `videos.md`
- ✅ **Solo procesa líneas que comienzan con `https`** (ignora comentarios y texto)
- ✅ Descarga en calidad de audio de 192 kbps
- ✅ Limpia las URLs de parámetros de playlist
- ✅ Crea automáticamente el directorio `downloads`
- ✅ Muestra progreso de descarga
- ✅ Maneja errores de descarga
- ✅ Evita descargas duplicadas
- ✅ Interfaz gráfica opcional para URLs individuales

## Estructura de archivos

```
youtube-downloader/
├── youtube_mp3_downloader.py  # Script principal
├── videos.md                  # Archivo con URLs de YouTube
├── requirements.txt           # Dependencias de Python
├── downloads/                 # Directorio de archivos MP3 descargados
└── README.md                  # Este archivo
```

## Formato del archivo videos.md

El archivo `videos.md` debe contener URLs de YouTube, una por línea:

```
https://www.youtube.com/watch?v=VIDEO_ID1
https://www.youtube.com/watch?v=VIDEO_ID2
https://youtu.be/VIDEO_ID3
```

El script es inteligente y puede extraer URLs de YouTube de cualquier texto, así que también funcionará si hay otro contenido en el archivo markdown.

## Solución de problemas

**Error: "ffmpeg not found"**
- Asegúrate de que FFmpeg esté instalado y en el PATH del sistema

**Error: "No module named 'yt_dlp'"**
- Ejecuta: `pip install yt-dlp`

**Videos que no se descargan:**
- Verifica que las URLs sean válidas
- Algunos videos pueden tener restricciones de región o edad
- Videos privados o eliminados no se pueden descargar
