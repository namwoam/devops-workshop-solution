"""
Linear Algebra Library
A simple library providing basic vector and matrix operations for educational purposes.
"""

import math
from typing import List, Union, Tuple


class Vector:
    """Represents a mathematical vector and provides vector operations."""
    
    def __init__(self, components: List[float]):
        """
        Initialize a vector with given components.
        
        Args:
            components: List of numerical values representing vector components
        """
        if not components:
            raise ValueError("Vector cannot be empty")
        self.components = list(components)
    
    def __str__(self) -> str:
        """Return string representation of vector."""
        return f"Vector({self.components})"
    
    def __repr__(self) -> str:
        """Return detailed string representation of vector."""
        return self.__str__()
    
    def __eq__(self, other: 'Vector') -> bool:
        """Check if two vectors are equal."""
        if not isinstance(other, Vector):
            return False
        if len(self.components) != len(other.components):
            return False
        return all(abs(a - b) < 1e-10 for a, b in zip(self.components, other.components))
    
    def __add__(self, other: 'Vector') -> 'Vector':
        """Add two vectors."""
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for addition")
        return Vector([a + b for a, b in zip(self.components, other.components)])
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        """Subtract one vector from another."""
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for subtraction")
        return Vector([a - b for a, b in zip(self.components, other.components)])
    
    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        """Multiply vector by a scalar."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be a number")
        return Vector([c * scalar for c in self.components])
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        """Right multiplication by scalar."""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: Union[int, float]) -> 'Vector':
        """Divide vector by a scalar."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Vector([c / scalar for c in self.components])
    
    def __len__(self) -> int:
        """Return the dimension of the vector."""
        return len(self.components)
    
    def __getitem__(self, index: int) -> float:
        """Get component at index."""
        return self.components[index]
    
    def dot(self, other: 'Vector') -> float:
        """
        Compute dot product with another vector.
        
        Args:
            other: Another vector
            
        Returns:
            Dot product (scalar)
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension for dot product")
        return sum(a * b for a, b in zip(self.components, other.components))
    
    def magnitude(self) -> float:
        """
        Compute the magnitude (length) of the vector.
        
        Returns:
            Magnitude of the vector
        """
        return math.sqrt(sum(c ** 2 for c in self.components))
    
    def normalize(self) -> 'Vector':
        """
        Return a normalized (unit) vector in the same direction.
        
        Returns:
            Normalized vector
        """
        mag = self.magnitude()
        if mag == 0:
            raise ValueError("Cannot normalize zero vector")
        return self / mag
    
    def distance(self, other: 'Vector') -> float:
        """
        Compute Euclidean distance to another vector.
        
        Args:
            other: Another vector
            
        Returns:
            Distance between vectors
        """
        if len(self.components) != len(other.components):
            raise ValueError("Vectors must have the same dimension")
        return (self - other).magnitude()


class Matrix:
    """Represents a mathematical matrix and provides matrix operations."""
    
    def __init__(self, data: List[List[float]]):
        """
        Initialize a matrix with given data.
        
        Args:
            data: 2D list where each inner list represents a row
        """
        if not data:
            raise ValueError("Matrix cannot be empty")
        
        row_length = len(data[0])
        if not all(len(row) == row_length for row in data):
            raise ValueError("All rows must have the same length")
        
        self.data = [list(row) for row in data]
        self.rows = len(self.data)
        self.cols = row_length
    
    def __str__(self) -> str:
        """Return string representation of matrix."""
        rows_str = "\n  ".join([str(row) for row in self.data])
        return f"Matrix([\n  {rows_str}\n])"
    
    def __repr__(self) -> str:
        """Return detailed string representation of matrix."""
        return self.__str__()
    
    def __eq__(self, other: 'Matrix') -> bool:
        """Check if two matrices are equal."""
        if not isinstance(other, Matrix):
            return False
        if self.rows != other.rows or self.cols != other.cols:
            return False
        return all(abs(a - b) < 1e-10 
                   for row_self, row_other in zip(self.data, other.data)
                   for a, b in zip(row_self, row_other))
    
    def __add__(self, other: 'Matrix') -> 'Matrix':
        """Add two matrices."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for addition")
        return Matrix([
            [a + b for a, b in zip(row_self, row_other)]
            for row_self, row_other in zip(self.data, other.data)
        ])
    
    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """Subtract one matrix from another."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction")
        return Matrix([
            [a - b for a, b in zip(row_self, row_other)]
            for row_self, row_other in zip(self.data, other.data)
        ])
    
    def __mul__(self, scalar: Union[int, float]) -> 'Matrix':
        """Multiply matrix by a scalar."""
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be a number")
        return Matrix([[c * scalar for c in row] for row in self.data])
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Matrix':
        """Right multiplication by scalar."""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: Union[int, float]) -> 'Matrix':
        """Divide matrix by a scalar."""
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return Matrix([[c / scalar for c in row] for row in self.data])
    
    def __getitem__(self, index: int) -> List[float]:
        """Get row at index."""
        return self.data[index]
    
    def __matmul__(self, other: Union['Matrix', 'Vector']) -> Union['Matrix', 'Vector']:
        """
        Matrix multiplication using @ operator.
        
        Args:
            other: Another matrix or vector
            
        Returns:
            Result of matrix multiplication
        """
        if isinstance(other, Vector):
            return self.multiply_vector(other)
        elif isinstance(other, Matrix):
            return self.multiply_matrix(other)
        else:
            raise TypeError("Can only multiply matrix with vector or matrix")
    
    def multiply_matrix(self, other: 'Matrix') -> 'Matrix':
        """
        Multiply two matrices.
        
        Args:
            other: Another matrix
            
        Returns:
            Product matrix
        """
        if self.cols != other.rows:
            raise ValueError(
                f"Cannot multiply matrices: dimensions {self.rows}x{self.cols} "
                f"and {other.rows}x{other.cols} are incompatible"
            )
        
        result = []
        for i in range(self.rows):
            row = []
            for j in range(other.cols):
                val = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                row.append(val)
            result.append(row)
        
        return Matrix(result)
    
    def multiply_vector(self, vec: Vector) -> Vector:
        """
        Multiply matrix by a vector.
        
        Args:
            vec: A vector
            
        Returns:
            Resulting vector
        """
        if self.cols != len(vec):
            raise ValueError(
                f"Cannot multiply matrix of size {self.rows}x{self.cols} "
                f"with vector of dimension {len(vec)}"
            )
        
        result = []
        for i in range(self.rows):
            val = sum(self.data[i][j] * vec.components[j] for j in range(self.cols))
            result.append(val)
        
        return Vector(result)
    
    def transpose(self) -> 'Matrix':
        """
        Compute the transpose of the matrix.
        
        Returns:
            Transposed matrix
        """
        return Matrix([
            [self.data[i][j] for i in range(self.rows)]
            for j in range(self.cols)
        ])
    
    def determinant(self) -> float:
        """
        Compute the determinant of a square matrix.
        
        Returns:
            Determinant value
        """
        if self.rows != self.cols:
            raise ValueError("Determinant is only defined for square matrices")
        
        if self.rows == 1:
            return self.data[0][0]
        
        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        
        # Use cofactor expansion for larger matrices
        det = 0
        for j in range(self.cols):
            det += ((-1) ** j) * self.data[0][j] * self._minor(0, j).determinant()
        
        return det
    
    def _minor(self, row: int, col: int) -> 'Matrix':
        """
        Get the minor matrix by removing specified row and column.
        
        Args:
            row: Row index to remove
            col: Column index to remove
            
        Returns:
            Minor matrix
        """
        new_data = [
            [self.data[i][j] for j in range(self.cols) if j != col]
            for i in range(self.rows) if i != row
        ]
        return Matrix(new_data)
    
    def inverse(self) -> 'Matrix':
        """
        Compute the inverse of a square matrix.
        
        Returns:
            Inverse matrix
        """
        if self.rows != self.cols:
            raise ValueError("Inverse is only defined for square matrices")
        
        det = self.determinant()
        if abs(det) < 1e-10:
            raise ValueError("Matrix is singular and has no inverse")
        
        if self.rows == 1:
            return Matrix([[1 / self.data[0][0]]])
        
        if self.rows == 2:
            a, b = self.data[0]
            c, d = self.data[1]
            return Matrix([
                [d / det, -b / det],
                [-c / det, a / det]
            ])
        
        # For larger matrices, use cofactor method (less efficient but works)
        adj = self._adjugate()
        return adj * (1 / det)
    
    def _adjugate(self) -> 'Matrix':
        """
        Compute the adjugate (adjoint) matrix.
        
        Returns:
            Adjugate matrix
        """
        cofactors = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                minor = self._minor(i, j)
                cofactor = ((-1) ** (i + j)) * minor.determinant()
                row.append(cofactor)
            cofactors.append(row)
        
        return Matrix(cofactors).transpose()
    
    def trace(self) -> float:
        """
        Compute the trace (sum of diagonal elements) of a square matrix.
        
        Returns:
            Trace value
        """
        if self.rows != self.cols:
            raise ValueError("Trace is only defined for square matrices")
        
        return sum(self.data[i][i] for i in range(self.rows))


def create_identity_matrix(n: int) -> Matrix:
    """
    Create an n x n identity matrix.
    
    Args:
        n: Size of the matrix
        
    Returns:
        Identity matrix
    """
    if n <= 0:
        raise ValueError("Matrix size must be positive")
    
    data = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    return Matrix(data)


def create_zero_matrix(rows: int, cols: int) -> Matrix:
    """
    Create a matrix filled with zeros.
    
    Args:
        rows: Number of rows
        cols: Number of columns
        
    Returns:
        Zero matrix
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("Dimensions must be positive")
    
    return Matrix([[0.0 for _ in range(cols)] for _ in range(rows)])


def create_zero_vector(dim: int) -> Vector:
    """
    Create a zero vector of given dimension.
    
    Args:
        dim: Dimension of the vector
        
    Returns:
        Zero vector
    """
    if dim <= 0:
        raise ValueError("Dimension must be positive")
    
    return Vector([0.0] * dim)
