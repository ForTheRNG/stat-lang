from stat_lang import Variable
from matplotlib import pyplot as plt

var = Variable(3, 10) + Variable(4, 4)
plt.plot(*zip(*(var.analyze())))
for _ in range(10):
    print(var[0])
plt.show()