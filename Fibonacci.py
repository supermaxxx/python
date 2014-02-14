def Fibonacci(num):
    res = [0,1]
    i = 0
    while i < num-1:
        res.append(res[i]+res[i+1])
        i+=1
    return res[1:]

def Fibonacci2(num):
    i,a,b = 0,0,1
    res = []
    while i < num:
        res.append(b)
        a,b = b,a+b
        i = i + 1
    return res

print Fibonacci(10)
print Fibonacci2(10)
