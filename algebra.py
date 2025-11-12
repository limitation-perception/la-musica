import numpy as np

# Введення матриці (приклад 3x3)
A = np.array([
    [2, 4, 6],
    [1, 3, 5],
    [0, 2, 8]
])



# Обчислення детермінанта
det = np.linalg.det(A)



print(f"Детермінант матриці: {det:.2f}")
import numpy as np

A = np.array([
    [1, 2, 3, 4],
    [2, 5, 8, 10],
    [3, 7, 11, 0]
])

rank_A = np.linalg.matrix_rank(A)

print(f"Матриця A:\n{A}")
print(f"Ранг матриці A: {rank_A}")