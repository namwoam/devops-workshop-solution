"""
Pytest tests for the linear algebra library.
Only one test is implemented; the rest are left as practice exercises.
"""

import math

import pytest

from lab1.lib import (
    Vector,
    Matrix,
    create_identity_matrix,
    create_zero_matrix,
    create_zero_vector,
)


def test_vector_creation():
    vec = Vector([1.0, 2.0, 3.0])

    assert len(vec) == 3
    assert vec[0] == 1.0
    assert vec[1] == 2.0
    assert vec[2] == 3.0


def test_vector_addition():
    assert Vector([1, 2, 3]) + Vector([4, 5, 6]) == Vector([5, 7, 9])


def test_vector_subtraction():
    assert Vector([4, 5, 6]) - Vector([1, 2, 3]) == Vector([3, 3, 3])


def test_vector_scalar_multiplication():
    vec = Vector([1, -2, 3])

    assert vec * 3 == Vector([3, -6, 9])
    assert 2 * vec == Vector([2, -4, 6])
    with pytest.raises(TypeError):
        vec * "2"


def test_vector_magnitude():
    assert Vector([3, 4]).magnitude() == 5
    assert Vector([1, 2, 2]).magnitude() == 3


def test_vector_dot_product():
    assert Vector([1, 2, 3]).dot(Vector([4, 5, 6])) == 32


def test_vector_normalization():
    normalized = Vector([3, 4]).normalize()

    assert normalized == Vector([0.6, 0.8])
    assert math.isclose(normalized.magnitude(), 1.0)


def test_vector_distance():
    assert Vector([1, 2]).distance(Vector([4, 6])) == 5


def test_vector_dimension_mismatch():
    vec_2d = Vector([1, 2])
    vec_3d = Vector([1, 2, 3])

    with pytest.raises(ValueError):
        vec_2d + vec_3d
    with pytest.raises(ValueError):
        vec_2d - vec_3d
    with pytest.raises(ValueError):
        vec_2d.dot(vec_3d)
    with pytest.raises(ValueError):
        vec_2d.distance(vec_3d)


def test_vector_equality():
    assert Vector([1.0, 2.0]) == Vector([1.0 + 1e-11, 2.0])
    assert Vector([1.0, 2.0]) != Vector([1.0, 2.1])
    assert Vector([1.0, 2.0]) != Vector([1.0, 2.0, 3.0])
    assert Vector([1.0, 2.0]) != [1.0, 2.0]


def test_matrix_creation():
    matrix = Matrix([[1, 2, 3], [4, 5, 6]])

    assert matrix.rows == 2
    assert matrix.cols == 3
    assert matrix[0] == [1, 2, 3]
    assert matrix[1] == [4, 5, 6]

    with pytest.raises(ValueError):
        Matrix([])
    with pytest.raises(ValueError):
        Matrix([[1, 2], [3]])


def test_matrix_addition():
    assert Matrix([[1, 2], [3, 4]]) + Matrix([[5, 6], [7, 8]]) == Matrix(
        [[6, 8], [10, 12]]
    )


def test_matrix_subtraction():
    assert Matrix([[5, 6], [7, 8]]) - Matrix([[1, 2], [3, 4]]) == Matrix(
        [[4, 4], [4, 4]]
    )


def test_matrix_scalar_multiplication():
    matrix = Matrix([[1, -2], [3, 4]])

    assert matrix * 2 == Matrix([[2, -4], [6, 8]])
    assert 3 * matrix == Matrix([[3, -6], [9, 12]])
    with pytest.raises(TypeError):
        matrix * "2"


def test_matrix_multiplication():
    left = Matrix([[1, 2, 3], [4, 5, 6]])
    right = Matrix([[7, 8], [9, 10], [11, 12]])

    assert left @ right == Matrix([[58, 64], [139, 154]])


def test_matrix_vector_multiplication():
    assert Matrix([[1, 2, 3], [4, 5, 6]]) @ Vector([7, 8, 9]) == Vector(
        [50, 122]
    )


def test_matrix_transpose():
    assert Matrix([[1, 2, 3], [4, 5, 6]]).transpose() == Matrix(
        [[1, 4], [2, 5], [3, 6]]
    )


def test_matrix_determinant_2x2():
    assert Matrix([[1, 2], [3, 4]]).determinant() == -2


def test_matrix_determinant_3x3():
    assert Matrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]]).determinant() == -306


def test_matrix_inverse_2x2():
    assert Matrix([[4, 7], [2, 6]]).inverse() == Matrix([[0.6, -0.7], [-0.2, 0.4]])


def test_matrix_inverse_singular():
    with pytest.raises(ValueError):
        Matrix([[1, 2], [2, 4]]).inverse()


def test_matrix_trace():
    assert Matrix([[1, 2], [3, 4]]).trace() == 5
    assert Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]]).trace() == 15


def test_matrix_dimension_mismatch_addition():
    with pytest.raises(ValueError):
        Matrix([[1, 2]]) + Matrix([[1, 2], [3, 4]])


def test_matrix_dimension_mismatch_multiplication():
    with pytest.raises(ValueError):
        Matrix([[1, 2]]) @ Matrix([[1, 2]])

    with pytest.raises(ValueError):
        Matrix([[1, 2]]) @ Vector([1, 2, 3])

    with pytest.raises(TypeError):
        Matrix([[1, 2]]) @ 2


def test_create_identity_matrix():
    assert create_identity_matrix(3) == Matrix(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    )

    with pytest.raises(ValueError):
        create_identity_matrix(0)


def test_create_zero_matrix():
    matrix = create_zero_matrix(2, 3)

    assert matrix == Matrix([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    with pytest.raises(ValueError):
        create_zero_matrix(0, 3)
    with pytest.raises(ValueError):
        create_zero_matrix(2, 0)


def test_create_zero_vector():
    assert create_zero_vector(3) == Vector([0.0, 0.0, 0.0])

    with pytest.raises(ValueError):
        create_zero_vector(0)


def test_empty_vector_creation():
    with pytest.raises(ValueError):
        Vector([])


def test_zero_vector_normalization():
    with pytest.raises(ValueError):
        Vector([0, 0]).normalize()


def test_divide_by_zero():
    with pytest.raises(ValueError):
        Vector([1, 2]) / 0
    with pytest.raises(ValueError):
        Matrix([[1, 2], [3, 4]]) / 0


def test_non_square_matrix_determinant():
    with pytest.raises(ValueError):
        Matrix([[1, 2, 3], [4, 5, 6]]).determinant()


def test_non_square_matrix_inverse():
    with pytest.raises(ValueError):
        Matrix([[1, 2, 3], [4, 5, 6]]).inverse()
