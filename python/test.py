from stat_lang import Variable, ValueType
from matplotlib import pyplot as plt

var = (Variable(ValueType.Num, 3) @ Variable(1, 101) - Variable(ValueType.Num, 3)) # / Variable(ValueType.Num, 3)
for _ in range(10):
    print(var.sample())
print(f"{var.mean(1000)} vs. {var.mean()}")
print(f"{var.std(10000)} vs. {var.std()}")
plt.plot(*zip(*(var.analyze())))
plt.show()