from multiprocessing import Process, Manager

def worker(d, l, id):
    d[id] = id ** 2
    l.append(id)

if __name__ == "__main__":
    with Manager() as manager:
        d = manager.dict()
        l = manager.list()

        procesos = [Process(target=worker, args=(d, l, i)) for i in range(5)]

        for p in procesos:
            p.start()
        for p in procesos:
            p.join()

        print(f"Dict: {dict(d)}")
        print(f"List: {list(l)}")