class A:
    def method(self):
        print("A.method() called")


class B:
    def method(self):
        print("B.method() called")


class C(A, B):
    pass


class D(C, B):
    pass


d = D()
d.method()

# The MRO for this can be a bit tricky.
# The immediate superclass for D is C, so if the method is not found in D,
# it is searched for in C. However, if it is not found in C,
# then you have to decide if you should check A(declared first in the list of C’s super classes)
# or check B(declared in D’s list of super classes after C).
# In Python 3 onwards, this is resolved as first checking A. So, the MRO becomes:

# D -> C -> A -> B

# Learn about C3 Linearization to see why.
