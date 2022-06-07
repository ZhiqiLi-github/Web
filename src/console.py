from  engine import SearchEngine
import timeit
def main():
    print("Reading/Creating Inverted Index ... ")
    start = timeit.default_timer()
    engine = SearchEngine()
    end = timeit.default_timer()

    print("Done, cost time: %.4f"%(end-start))
    engine.info()
    while True:
        result = engine.interpreter(input(">>> "))
        engine.display(result)
    pass


if __name__ == '__main__':
    main()
