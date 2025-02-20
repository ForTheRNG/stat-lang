from stat_lang import Variable
from matplotlib import pyplot as plt

plt.plot(*zip(*(Variable(3,10).analyze())))
plt.show()