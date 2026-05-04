"""
Pytest tests for the linear algebra library.
Only one test is implemented; the rest are left as practice exercises.
"""

import math

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
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_subtraction():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_scalar_multiplication():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_magnitude():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_dot_product():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_normalization():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_distance():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_dimension_mismatch():
    raise NotImplementedError("This test is not implemented yet.")


def test_vector_equality():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_creation():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_addition():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_subtraction():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_scalar_multiplication():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_multiplication():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_vector_multiplication():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_transpose():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_determinant_2x2():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_determinant_3x3():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_inverse_2x2():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_inverse_singular():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_trace():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_dimension_mismatch_addition():
    raise NotImplementedError("This test is not implemented yet.")


def test_matrix_dimension_mismatch_multiplication():
    raise NotImplementedError("This test is not implemented yet.")


def test_create_identity_matrix():
    raise NotImplementedError("This test is not implemented yet.")


def test_create_zero_matrix():
    raise NotImplementedError("This test is not implemented yet.")


def test_create_zero_vector():
    raise NotImplementedError("This test is not implemented yet.")


def test_empty_vector_creation():
    raise NotImplementedError("This test is not implemented yet.")


def test_zero_vector_normalization():
    raise NotImplementedError("This test is not implemented yet.")


def test_divide_by_zero():
    raise NotImplementedError("This test is not implemented yet.")


def test_non_square_matrix_determinant():
    raise NotImplementedError("This test is not implemented yet.")


def test_non_square_matrix_inverse():
    raise NotImplementedError("This test is not implemented yet.")
