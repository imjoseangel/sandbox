class A:
    def method(self):
        print("A.method() called")


class B:
    pass


class C(B, A):
    pass


c = C()
c.method()
