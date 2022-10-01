class A:
    def method(self):
        print("A.method() called")


class B(A):
    def method(self):
        print("B.method() called")


b = B()
b.method()
