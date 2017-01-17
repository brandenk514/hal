import systemos
import wit

if __name__ == '__main__':
    sys = systemos.SystemOS("Hal")
    wit = wit.Wit("PYEBZJDFJJTY7J6RN4CVFWTO7DLYK5Y6")
    print(wit.listen())
