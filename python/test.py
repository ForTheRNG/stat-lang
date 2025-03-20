from stat_variables import Variable, ValueType
from matplotlib import pyplot as plt
import z3

var = Variable(5, 10) / (Variable(1, 2) + Variable(ValueType.Num, 1))
i = 0
for x in var:
    if i == 10:
        break
    i += 1
    print(x)
print(f"{var.mean(1000)} vs. {var.mean()}")
print(f"{var.std(1000)} vs. {var.std()}")
plt.plot(*zip(*(var.analyze())))
plt.show()
"""
# 9x9 matrix of integer variables
X = [ [ z3.Int("x_%s_%s" % (i+1, j+1)) for j in range(9) ]
      for i in range(9) ]

# each cell contains a value in {1, ..., 9}
cells_c  = [ z3.And(1 <= X[i][j], X[i][j] <= 9)
             for i in range(9) for j in range(9) ]

# each row contains a digit at most once
rows_c   = [ z3.Distinct(X[i]) for i in range(9) ]

# each column contains a digit at most once
cols_c   = [ z3.Distinct([ X[i][j] for i in range(9) ])
             for j in range(9) ]

# each 3x3 square contains a digit at most once
sq_c     = [ z3.Distinct([ X[3*i0 + i][3*j0 + j]
                        for i in range(3) for j in range(3) ])
             for i0 in range(3) for j0 in range(3) ]

sudoku_c = cells_c + rows_c + cols_c + sq_c

# sudoku instance, we use '0' for empty cells
instance = ((0,0,0,0,9,4,0,3,0),
            (0,0,0,5,1,0,0,0,7),
            (0,8,9,0,0,0,0,4,0),
            (0,0,0,0,0,0,2,0,8),
            (0,6,0,2,0,1,0,5,0),
            (1,0,2,0,0,0,0,0,0),
            (0,7,0,0,0,0,5,2,0),
            (9,0,0,0,6,5,0,0,0),
            (0,4,0,9,7,0,0,0,0))

instance_c = [ z3.If(instance[i][j] == 0,
                  True,
                  X[i][j] == instance[i][j])
               for i in range(9) for j in range(9) ]

s = z3.Solver()
s.add(sudoku_c + instance_c)
if s.check() == z3.sat:
    m = s.model()
    r = [ [ m.evaluate(X[i][j]) for j in range(9) ]
          for i in range(9) ]
    z3.print_matrix(r)
else:
    print ("failed to solve")
"""