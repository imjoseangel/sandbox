class A:
    def method(self):
        print("A.method() called")


class B(A):
    def method(self):
        print("B.method() called")


b = B()
b.method()

# This is a simple case with single inheritance.
# In this case, when b.method() is called, it first searches for the method in class B.
# In this case, class B had defined the method; hence, it is the one that was executed.
# In the case where it is not present in B,
# then the method from its immediate super class (A) would be called.
# So, the MRO for this case is: B -> A
