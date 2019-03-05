def my_decorator(func):
        def wrapper():
            print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
        return wrapper


def myfunc():
    print("Print myfunc")


my_decorator(myfunc)
