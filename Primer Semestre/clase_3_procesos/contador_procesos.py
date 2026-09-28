#!/usr/bin/env python3
import os

def main():
    procesos = [d for d in os.listdir("/proc") if d.isdigit()]
    print(f"Procesos en ejecución: {len(procesos)}")

if __name__ == "__main__":
    main()