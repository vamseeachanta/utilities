import latexify
# Third party imports



# @latexify.function
# def solve(a,b,c):
#     return (-b + math.sqrt(b**2-4*a*c))/(2*a)

# solve

def fib(x):
    if x==0:
        return 1
    elif x==1:
        return 1
    else:
        return fib(x-1)+fib(x-2)

latexify.get_latex(fib)


