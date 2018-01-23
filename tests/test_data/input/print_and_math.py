print("Hello, world!")
m = 45
x = 137
b = 18
y = m * x + b
print("Simply, x={}".format(y))
print("1+2={}".format(1 + 2))
# Failed with a previous version of the grammar that interpreted brackets as tuples
# Note also this shouldn't generate with the "var" keyword
y = 17 + (m * x) + b
z = 2 + (3 + 4) * 5
