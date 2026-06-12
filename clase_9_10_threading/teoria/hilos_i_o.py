import threading
import time
import urllib.request

def descargar(url):
    """Tarea I/O-bound."""
    print(f"Descargando {url}...")
    response = urllib.request.urlopen(url)
    data = response.read()
    print(f"Descargado {url}: {len(data)} bytes")

urls = [
    "https://www.python.org",
    "https://docs.python.org",
    "https://pypi.org",
]

# Secuencial
inicio = time.time()
for url in urls:
    descargar(url)
print(f"Secuencial: {time.time() - inicio:.2f}s\n")

# Con threads (SÍ es más rápido!)
inicio = time.time()
threads = []
for url in urls:
    t = threading.Thread(target=descargar, args=(url,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
print(f"Threads: {time.time() - inicio:.2f}s")