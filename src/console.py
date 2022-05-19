from  engine import SearchEngine

def main():
    engine = SearchEngine()
    while True:
        docID, key = engine.interpreter(input(">>> "))
        if docID is not None:
            engine.display(docID, key)
    pass


if __name__ == '__main__':
    main()