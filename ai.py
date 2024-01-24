# ai code generated

from django.core.cache import cache

def factorial(n):\
    if n in cache:
        return cache[n]
    else:
        cache[n] = n * factorial(n - 1)
        return cache[n]

# fibonacci function with cache
def fibonacci(n):
    if n in cache:
        return cache[n]
    else:
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]
    
