
import os
import stat
import pwd
import grp
import sys
from datetime import datetime


def tipo_archivo(modo):
    if stat.S_ISREG(modo):
        return "archivo regular"
    elif stat.S_ISDIR(modo):
        return "directorio"
    elif stat.S_ISLNK(modo):
        return "enlace simbólico"
    elif stat.S_ISCHR(modo):
        return "dispositivo de caracteres"
    elif stat.S_ISBLK(modo):
        return "dispositivo de bloques"
    else:
        return "otro"


def permisos_legibles(modo):
    return stat.filemode(modo)


def permisos_octal(modo):
    return oct(modo & 0o777)[2:]


def formato_tiempo(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def main():
    if len(sys.argv) != 2:
        print("Uso: python inspector.py <ruta>")
        sys.exit(1)

    ruta = sys.argv[1]

    try:
        # Para no seguir symlinks automáticamente
        info = os.lstat(ruta)
    except FileNotFoundError:
        print("El archivo no existe")
        sys.exit(1)

    print(f"Archivo: {ruta}")

    # Tipo
    tipo = tipo_archivo(info.st_mode)

    if tipo == "enlace simbólico":
        destino = os.readlink(ruta)
        print(f"Tipo: {tipo} -> {destino}")
    else:
        print(f"Tipo: {tipo}")

    # Tamaño
    tamaño = info.st_size
    print(f"Tamaño: {tamaño} bytes")

    # Permisos
    legible = permisos_legibles(info.st_mode)
    octal = permisos_octal(info.st_mode)
    print(f"Permisos: {legible} ({octal})")

    # Usuario y grupo
    usuario = pwd.getpwuid(info.st_uid).pw_name
    grupo = grp.getgrgid(info.st_gid).gr_name

    print(f"Propietario: {usuario} (uid: {info.st_uid})")
    print(f"Grupo: {grupo} (gid: {info.st_gid})")

    # Inodo y enlaces
    print(f"Inodo: {info.st_ino}")
    print(f"Enlaces duros: {info.st_nlink}")

    # Fechas
    print(f"Creación: {formato_tiempo(info.st_ctime)}")
    print(f"Última modificación: {formato_tiempo(info.st_mtime)}")
    print(f"Último acceso: {formato_tiempo(info.st_atime)}")

    # Extra para directorios
    if stat.S_ISDIR(info.st_mode):
        try:
            contenido = os.listdir(ruta)
            print(f"Contenido: {len(contenido)} elementos")
        except PermissionError:
            print("Contenido: permiso denegado")


if __name__ == "__main__":
    main()