# Test of generators. This is a basic generator.
def fib():
    previous = []    
    while (True):
        if len(previous) == 0 or len(previous) == 1:
            previous.append(1)
            yield 1
        else:
            next_value = previous[-1] + previous[-2]
            previous.append(next_value)
            yield next_value

print("First five fibs:")
gen = fib()

i = 0
while i < 5:
    print(next(gen))
    i += 1

# Create a generator comprehension that returns n^2.
print("Generator comprehension: n^2. Next five:")
gen2 = (n**2 for n in gen)

i = 0
while i < 5:
    i += 1
    print(next(gen2))
