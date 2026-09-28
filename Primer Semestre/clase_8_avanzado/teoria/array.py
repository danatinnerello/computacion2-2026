from multiprocessing import Process, Array

def modificar(arr, idx):
    arr[idx] = arr[idx] ** 2

if __name__ == "__main__":
    numeros = Array('i', [1, 2, 3, 4, 5])  # array compartido

    procesos = [Process(target=modificar, args=(numeros, i))
                for i in range(5)]

    for p in procesos:
        p.start()
    for p in procesos:
        p.join()

    print(f"Array: {list(numeros)}")  # [1, 4, 9, 16, 25]