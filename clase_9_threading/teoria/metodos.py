import threading

def mostrar_info():
    thread_actual = threading.current_thread()
    print(f"Nombre: {thread_actual.name}")
    print(f"ID: {thread_actual.ident}")
    print(f"Daemon: {thread_actual.daemon}")

# Thread principal
print("=== Main thread ===")
mostrar_info()

# En un thread secundario
print("\n=== Thread secundario ===")
t = threading.Thread(target=mostrar_info, name="MiThread")
t.start()
t.join()

# Listar todos los threads activos
print(f"\nThreads activos: {threading.active_count()}")
for t in threading.enumerate():
    print(f"  - {t.name}")

