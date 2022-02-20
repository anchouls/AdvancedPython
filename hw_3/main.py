import numpy as np
from matrix import Matrix
from numpy_matrix import NumpyMatrix


def easy():
    m1 = Matrix(np.random.randint(0, 10, (10, 10)))
    m2 = Matrix(np.random.randint(0, 10, (10, 10)))
    (m1 + m2).write_to_file("artifacts/easy/matrix+.txt")
    (m1 * m2).write_to_file("artifacts/easy/matrix*.txt")
    (m1 @ m2).write_to_file("artifacts/easy/matrix@.txt")


def medium():
    m1 = NumpyMatrix(np.random.randint(0, 10, (10, 10)))
    m2 = NumpyMatrix(np.random.randint(0, 10, (10, 10)))
    (m1 + m2).write_to_file("artifacts/medium/matrix+.txt")
    (m1 * m2).write_to_file("artifacts/medium/matrix*.txt")
    (m1 @ m2).write_to_file("artifacts/medium/matrix@.txt")


def hard():
    with open("artifacts/hard/A.txt", 'r') as f:
        A = Matrix([[int(j) for j in i.split()] for i in f.readlines()])
    with open("artifacts/hard/B.txt", 'r') as f:
        B = Matrix([[int(j) for j in i.split()] for i in f.readlines()])
    with open("artifacts/hard/C.txt", 'r') as f:
        C = Matrix([[int(j) for j in i.split()] for i in f.readlines()])
    with open("artifacts/hard/D.txt", 'r') as f:
        D = Matrix([[int(j) for j in i.split()] for i in f.readlines()])

    if (hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D):
        print("Collision")

    (A @ B).write_to_file("artifacts/hard/AB.txt")
    (C @ D).write_to_file("artifacts/hard/CD.txt")
    with open("artifacts/hard/hash.txt", 'w') as f:
        print(hash(A), file=f)


def main():
    np.random.seed(0)
    easy()
    medium()
    hard()


if __name__ == "__main__":
    main()
