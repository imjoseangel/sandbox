class A:
    def method(self):
        print("A.method() called")


class B:
    def method(self):
        print("B.method() called")


class C(B, A):
    pass


class D(B, C):
    pass


d = D()
d.method()

# If, as in example 4 (shown above):

# The order of inheritance of D is (B, C, object) object ensures that it is a new style class
# The order of inheritance of C is (B, A)
# It would give an error:
# TypeError: Cannot create a consistent method resolution order(MRO) for bases B, C.

# Explanation:
# The MRO that we can deduce from the rules we have seen is : D -> B -> C -> B -> A
# However, B should not come before C as it is a super class of C. So, it becomes:
# D -> C -> B -> A
# But, while declaring the class D, B was declared first in the list of super classes
# so, if a method exists in both B and C, which version should called?
