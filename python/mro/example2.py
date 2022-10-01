class A:
    def method(self):
        print("A.method() called")


class B:
    pass


class C(B, A):
    pass


c = C()
c.method()

# The MRO for this case is :
# C -> B -> A
# The method only existed in A, where it was searched for last.
