from stat_variables import Variable, ValueType
from matplotlib import pyplot as plt

a = Variable(2, 20)
b = Variable(2, 20)
var = a.c_lt(b).ternary(a, b)
for _ in range(10):
    print(var.sample())
print(f"{var.mean(1000)} vs. {var.mean()}")
print(f"{var.std(10000)} vs. {var.std()}")
plt.plot(*zip(*(var.analyze())))
plt.show()