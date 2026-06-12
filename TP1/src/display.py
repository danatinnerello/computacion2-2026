def mostrar_memoria(procesos):

    print("\n=== MEMORIA ===\n")

    print(
        f"{'PID':<8}"
        f"{'RSS':<15}"
        f"{'SIZE':<15}"
        f"{'SWAP':<15}"
        f"{'CMD'}"
    )

    for p in procesos[:10]:

        print(
            f"{p['pid']:<8}"
            f"{p['VmRSS']:<15}"
            f"{p['VmSize']:<15}"
            f"{p['VmSwap']:<15}"
            f"{p['comando']}"
        )

def mostrar_threads(procesos):

    print("\n=== THREADS ===\n")

    print(
        f"{'PID':<8}"
        f"{'THREADS':<12}"
        f"{'CMD'}"
    )

    for p in procesos[:10]:

        print(
            f"{p['pid']:<8}"
            f"{p['threads']:<12}"
            f"{p['comando']}"
        )

def mostrar_fds(procesos):

    print("\n=== FILE DESCRIPTORS ===\n")

    print(
        f"{'PID':<8}"
        f"{'FDS':<8}"
        f"{'CMD'}"
    )

    for p in procesos[:10]:

        print(
            f"{p['pid']:<8}"
            f"{p['fds']:<8}"
            f"{p['comando']}"
        )

def mostrar_senales(procesos):

    print("\n=== SEÑALES ===\n")

    print(
        f"{'PID':<8}"
        f"{'PEND':<18}"
        f"{'IGN':<18}"
        f"{'CGT':<18}"
        f"{'CMD'}"
    )

    for p in procesos[:10]:

        print(
            f"{p['pid']:<8}"
            f"{p['SigPnd'][:16]:<18}"
            f"{p['SigIgn'][:16]:<18}"
            f"{p['SigCgt'][:16]:<18}"
            f"{p['comando']}"
        )

def mostrar_scheduling(procesos):

    print("\n=== SCHEDULING ===\n")

    print(
        f"{'PID':<8}"
        f"{'CPU':<12}"
        f"{'VOL':<12}"
        f"{'NONVOL':<12}"
        f"{'CMD'}"
    )

    for p in procesos[:10]:

        print(
            f"{p['pid']:<8}"
            f"{p['cpus']:<12}"
            f"{p['voluntary']:<12}"
            f"{p['nonvoluntary']:<12}"
            f"{p['comando']}"
        )