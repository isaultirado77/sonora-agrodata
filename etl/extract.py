# extract.py

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
from datetime import datetime
from urllib.parse import urlparse, unquote
import logging

from tqdm import tqdm
import requests
from bs4 import BeautifulSoup

from scripts.config import RAW_DIR, setup_logger


# logger
logger = logging.getLogger(__name__)

# paths
agricultura_dir = RAW_DIR / "agricultura"
agricultura_dir.mkdir(exist_ok=True)

hidricos_dir = RAW_DIR / "hidricos"
hidricos_dir.mkdir(exist_ok=True)

# urls
datasets = {
    'agricultura': r"https://datos.sonora.gob.mx/dataset/Agricultura%20Sonora",
    'hidricos': r"https://datos.sonora.gob.mx/dataset/Recursos%20H%C3%ADdricos"
}

def get_download_urls(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    atags = soup.find_all("a", class_="resource-url-analytics")

    return [a.get('href') for a in atags if a]


def download_file(url, dest_dir, chunk_size=5*1024*1024):
    """
    Descarga un archivo desde una URL mostrando una barra de progreso con tqdm.
    """
    if not url.startswith("http"):
        logger.warning(f"URL inválida ignorada: {url}")
        return None

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()

            total_size = int(r.headers.get('content-length', 0))

            parsed = urlparse(url)
            filename = Path(unquote(parsed.path)).name
            file_path = dest_dir / filename
            
            with open(file_path, 'wb') as f, tqdm(
                total=total_size if total_size > 0 else None,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=file_path.name
            ) as bar:
                
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))
        
        return file_path

    except Exception as e:
        logger.exception(f'Error al descargar: {e}')
        raise


def download_files_concurrently(urls, dest_dir, max_workers=5):
    """
    Descarga archivos de una lista de URLs de forma concurrente usando ThreadPoolExecutor.
    """
    downloaded_files = []

    dest_dir.mkdir(parents=True, exist_ok=True)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(download_file, url, dest_dir)
            for url in urls
        ]
        
        for future in futures:
            result = future.result()
            if result:
                downloaded_files.append(result)

    return downloaded_files


def extract_data():
    start = datetime.now()
    logger.info("Iniciando extracción de datos...")
    try:
        paths = {}
        for name, url in datasets.items():
            urls = get_download_urls(url)
            paths[name] = download_files_concurrently(urls, RAW_DIR / name)


        elapsed = (datetime.now() - start).total_seconds()
        logger.info(f'Extracción completada en {elapsed:.2f} s')
        
        return paths

    except Exception:
        logger.exception("Fallo durante la extracción")


if __name__ == '__main__':
    logger = setup_logger()
    extract_data()
