from  engine import SearchEngine

def main():
    engine = SearchEngine()
    engine.info()
    while True:
        result = engine.interpreter(input(">>> "))
        engine.display(result)
    pass


if __name__ == '__main__':
    main()