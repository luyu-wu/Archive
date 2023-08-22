'''
I'm litearlly so bored help my soul
this one is for integrating a function s;kull:

'''



def Quadratic(x):
    return (x**2)


def Integrate(function,x_interval,a,b): # a is the lower limit of the integral, b is the upper limit
    sum = 0
    while a <  b:
        sum += function(a)*x_interval
        a+= x_interval
    print(sum)

Integrate(Quadratic,0.005,0,4)
