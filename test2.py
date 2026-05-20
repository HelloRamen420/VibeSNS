import math
def dsin (x):
    h=0.001
    return (math.sin(x+h)-math.sin(x))/h
print(dsin(math.pi))