class A:
    def __init__(self):
        self.name = 'name'

    def method(self):
        print 'method'

    def method2(self):
        print 'method2'



a = A()
getattr(a, 'method', 'method2')()
setattr(a, 'python', 'test')
s = getattr(a, 'python', 'not found')
print s
print a.__dict__
# print getattr(a, 'name12', 'not found')()
