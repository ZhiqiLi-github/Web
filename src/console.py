from  engine import SearchEngine

def main():
    engine = SearchEngine()
    while True:
        docIDs, keys = engine.interpreter(input(">>> "))
        if keys is not None:
            for i in range(len(docIDs)):
                engine.display(docIDs[i], keys[i])
    pass


if __name__ == '__main__':
    main()