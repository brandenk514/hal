import systemos
import wit

# This is the main class to run HAL

if __name__ == '__main__':
    sys = systemos.SystemOS("Hal")
    wit = wit.Wit("PYEBZJDFJJTY7J6RN4CVFWTO7DLYK5Y6")
    sys.sayHello()
    sys.open_app("Google Chrome")
    print(wit.listen())
