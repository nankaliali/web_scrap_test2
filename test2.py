class Integer :
    def __init__(self, value):
        if isinstance(value, int):
            self.value = value
        else:
            raise TypeError('Value must be an instance of int class.')

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __lt__(self, other):
        if isinstance(other, Integer):
            value = other.value
        elif isinstance(other, int):
            value = other
        if self.value < value :
            return True
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, Integer):
            value = other.value
        elif isinstance(other, int):
            value = other
        if self.value > value :
            return True
        else:
            return False

    def __le__(self, other):
        if isinstance(other, Integer):
            value = other.value
        elif isinstance(other, int):
            value = other
        if self.value <= value :
            return True
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, Integer):
            value = other.value
        elif isinstance(other, int):
            value = other
        if self.value >= value :
            return True
        else:
            return False
    
    def __eq__(self, other):
        if isinstance(other, Integer):
            value = other.value
        elif isinstance(other, int):
            value = other
        elif isinstance(other, Complex):
            if other.i != 0 :
                return False
            value = other.r
        else:
            return NotImplemented
        # Check equivalent
        if self.value == value :
            return True
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Matrix):
            return NotImplemented
        elif isinstance(other, Integer):
            return Integer(self.value + other.value)
        elif isinstance(other, Complex):
            return NotImplemented
        else:
            raise TypeError('Integer cant add to this type.')

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return NotImplemented
        elif isinstance(other, Integer):
            return Integer(self.value * other.value)
        elif isinstance(other, Complex):
            return NotImplemented
        else:
            raise TypeError('Integer cant mult by this type.')

    def __sub__(self, other):
        return self + other*Integer(-1)

    def __rsub__(self, other):
        return self + other*Integer(-1)

    @staticmethod
    def make_integer_from_string(string):
        return Integer(int(string))

class Complex :
    def __init__(self, real, imaginary):
        if True: # validation
            self.i = imaginary
            self.r = real
        else:
            raise ValueError()

    def __eq__(self, other):
        if isinstance(other, Complex):
            if (self.i == other.i) and (self.r == other.r):
                return True
            else :
                return False
        else : 
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Matrix):
            return NotImplemented
        elif isinstance(other, Integer):
            return Complex(self.r + other.value, self.i)
        elif isinstance(other, Complex):
            return Complex(self.r + other.r, self.i + other.i)
        else:
            raise TypeError('Complex number cant add to this type.')
    
    def __radd__(self, other):
        if isinstance(other, Integer):
            return Complex(self.r + other.value, self.i)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return NotImplemented
        elif isinstance(other, Integer):
            return Complex(self.r * other.value, self.i * other.value)
        elif isinstance(other, Complex):
            return Complex(self.r*other.r - self.i*other.i, self.i * other.r + self.r* other.i)
        else:
            raise TypeError('Complex number cant multiply by this type.')
    
    def __rmul__(self, other):
        if isinstance(other, Integer):
            return Complex(self.r * other.value, self.i * other.value)
    
    def __sub__(self, other):
        return self + other*Integer(-1)

    def __rsub__(self, other):
        return self + other*Integer(-1)

    def __str__(self):
        return str(self.r)+ ('' if self.i < 0 else '+') + str(self.i) + 'i'

    def __repr__(self):
        return str(self.r)+ ('' if self.i < 0 else '+') + str(self.i) + 'i'

    @staticmethod
    def make_complex_from_string(string):
        i, r = string.split('i')
        return Complex(int(r), int(i))

class Matrix :
    def __init__(self, row, col, matrix):
        self.row = row
        self.col = col
        if all((isinstance(it, Integer) or isinstance(it, Complex)) for it in matrix) :
            self.matrix = []
            # create the matrix
            for r in range(row) :
                self.matrix.append(matrix[r*col:(r+1)*col])
        else:
            raise TypeError('Values must be an instance of Integer or Complex class.')
        
    @staticmethod
    def make_unit_matrix(n):
        return Matrix(n, n, [Integer(1) if i % (n+1) == 0 else Integer(0) for i in range(n*n)])

    @staticmethod
    def get_ith_row(matrix, i):
        return matrix.matrix[i]

    @staticmethod
    def get_ith_col(matrix, j):
        return [it[j] for it in matrix.matrix]

    @staticmethod
    def is_zero_matrix(matrix):
        for i in matrix.matrix:
            for j in i:
                if j != 0 :
                    return False
        return True

    @staticmethod
    def is_unit_matrix(matrix):
        if matrix.row != matrix.col :
            return False
        return matrix == Matrix.make_unit_matrix(matrix.row)

    @staticmethod
    def is_bottom_triangular_matrix(matrix):
        if matrix.row != matrix.col :
            return False
        for i in range(matrix.row):
            for j in range(i+1, matrix.col):
                if matrix.matrix[i][j] != 0:
                    return False
        return True

    @staticmethod
    def is_top_triangular_matrix(matrix):
        if matrix.row != matrix.col :
            return False
        for i in range(matrix.row):
            for j in range(i):
                if matrix.matrix[i][j] != 0:
                    return False
        return True

    @classmethod
    def make_matrix_from_string(cls, elements):
        matrix = []
        rows = elements.split(',')
        for row in rows:
            for item in row.split(' '):
                if 'i' in item:
                    matrix.append(Complex.make_complex_from_string(item))
                else:
                    matrix.append(Integer.make_integer_from_string(item))
        return cls(len(rows), len(matrix)//len(rows), matrix)

    def __str__(self):
        result = ''
        for it in self.matrix:
            result += str(it)
            result += '\n'
        return result[:-1]
    
    def __eq__(self, other):
        if isinstance(other, Matrix):
            return True if self.matrix == other.matrix else False
        else:
            return NotImplemented

    def __add__(self, other):
        if isinstance(other, Matrix):
            if (self.row == other.row) and (self.col == other.col):
                result = []
                for i in range(self.row) :
                    for j in range(self.col):
                        result.append(self.matrix[i][j] + other.matrix[i][j])
                return Matrix(self.row, self.col, result)
            else:
                raise ValueError('the shape of matrixes are diff!')
        elif isinstance(other, Integer) or isinstance(other, Complex):
            result = []
            for i in range(self.row) :
                for j in range(self.col):
                    result.append(self.matrix[i][j] + other)
            return Matrix(self.row, self.col, result)
        else:
            raise TypeError('Matrix cant add to this type.')
    
    def __radd__(self, other):
        if isinstance(other, Integer) or isinstance(other, Complex):
            result = []
            for i in range(self.row) :
                for j in range(self.col):
                    result.append(self.matrix[i][j] + other)
            return Matrix(self.row, self.col, result)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.col == other.row :
                result = []
                for i in range(self.row):
                    row = Matrix.get_ith_row(self, i)
                    for j in range(other.col):
                        col = Matrix.get_ith_col(other, j)
                        new_element = Integer(0)
                        for i in range(len(row)):
                            new_element += row[i]*col[i]
                        result.append(new_element)
                return Matrix(self.row, other.col, result)
            else:
                raise ValueError('the shape of matrixes are not correct!')
        elif isinstance(other, Integer) or isinstance(other, Complex):
            result = []
            for i in range(self.row) :
                for j in range(self.col):
                    result.append(self.matrix[i][j] * other)
            return Matrix(self.row, self.col, result)
        else:
            raise TypeError('Matrix cant multipy by this type.')
    
    def __rmul__(self, other):
        if isinstance(other, Integer) or isinstance(other, Complex):
            result = []
            for i in range(self.row) :
                for j in range(self.col):
                    result.append(self.matrix[i][j] * other)
            return Matrix(self.row, self.col, result)

    def __sub__(self, other):
        return self + other*Integer(-1)

    def __rsub__(self, other):
        return self + other*Integer(-1)

def multiply(a, b):
    return a*b
    
################ Unit Testing ################
import unittest
def run_tests(test_class):
    '''running the tests'''
    suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
    runner = unittest.TextTestRunner(verbosity=3)
    runner.run(suite)

class matrix_tests(unittest.TestCase):
    def test_creat_matrix(self):
        matrix = Matrix(3, 2, [Integer(12), Complex(1, 4), Integer(122), Complex(10, 2), Integer(4), Complex(2, -5)])
        self.assertEqual(matrix.matrix, [[Integer(12), Complex(1, 4)], [Integer(122), Complex(10, 2)], [Integer(4), Complex(2, -5)]])

    def test_make_unit_matrix(self):
        matrixi = Matrix.make_unit_matrix(5)
        self.assertEqual(str(matrixi), "[1, 0, 0, 0, 0]\n[0, 1, 0, 0, 0]\n[0, 0, 1, 0, 0]\n[0, 0, 0, 1, 0]\n[0, 0, 0, 0, 1]")

    def test_get_ith_row(self):
        matrix = Matrix(3, 2, [Integer(12), Complex(1, 4), Integer(122), Complex(10, 2), Integer(4), Complex(2, -5)])
        self.assertEqual(Matrix.get_ith_row(matrix, 1), [Integer(122), Complex(10, 2)])

    def test_get_ith_col(self):
        matrix = Matrix(3, 2, [Integer(12), Complex(1, 4), Integer(122), Complex(10, 2), Integer(4), Complex(2, -5)])
        self.assertEqual(Matrix.get_ith_col(matrix, 1), [Complex(1, 4), Complex(10, 2), Complex(2, -5)])

    def test_is_zero_matrix(self):
        matrixi = Matrix.make_unit_matrix(5)
        self.assertEqual(Matrix.is_zero_matrix(matrixi), False)
        self.assertEqual(Matrix.is_zero_matrix(Matrix(2, 2, [Integer(0),Integer(0),Integer(0),Integer(0)])), True)

    def test_integer_comparison(self):
        self.assertEqual(10 >= Integer(11), False)
        self.assertEqual(10 < Integer(11), True)
        self.assertEqual(Integer(12) == Integer(11), False)
        self.assertEqual(Integer(23) > 34, False)
        self.assertEqual([Integer(1)]==[Complex(1, 0)], True)
        self.assertEqual([Integer(1), Complex(3, 0)]==[Complex(1, 0), Integer(3)], True)
        self.assertEqual([Integer(1), Complex(3, 32)]==[Complex(1, 0), Integer(3)], False)

    def test_matrix_equivalent(self):
        matrix = Matrix(3, 2, [Integer(12), Complex(1, 4), Integer(122), Complex(10, 2), Integer(4), Complex(2, -5)])
        matrixi = Matrix.make_unit_matrix(5)
        matrixi2 = Matrix.make_unit_matrix(5)
        self.assertEqual(matrixi == matrixi2, True)
        self.assertEqual(matrixi == matrix, False)

    def test_is_unit_matrix(self):
        matrix = Matrix(3, 2, [Integer(1), Complex(1, 4), Integer(12), Complex(10, 2), Integer(34), Complex(2, -5)])
        self.assertEqual(Matrix.is_unit_matrix(matrix), False)
        self.assertEqual(Matrix.is_unit_matrix(Matrix.make_unit_matrix(5)), True)

    def test_is_bottom_triangular_matrix(self):
        matrix = Matrix(3, 3, [Integer(2),Integer(0),Integer(0),Integer(5),Integer(7),Integer(0),Integer(2),Integer(2),Integer(2)])
        self.assertEqual(Matrix.is_bottom_triangular_matrix(matrix), True)
        matrix = Matrix(3, 3, [Integer(2),Integer(1),Integer(0),Integer(5),Integer(7),Integer(0),Integer(2),Integer(2),Integer(2)])
        self.assertEqual(Matrix.is_bottom_triangular_matrix(matrix), False)

    def test_is_top_triangular_matrix(self):
        matrix = Matrix(3, 3, [Integer(2),Integer(10),Integer(3240),Integer(0),Integer(7),Integer(35),Integer(0),Integer(0),Integer(0)])
        self.assertEqual(Matrix.is_top_triangular_matrix(matrix), True)
        matrix = Matrix(3, 3, [Integer(2),Integer(1),Integer(0),Integer(5),Integer(7),Integer(0),Integer(2),Integer(2),Integer(2)])
        self.assertEqual(Matrix.is_top_triangular_matrix(matrix), False)

    def test_make_matrix_from_string(self):
        matrix = Matrix(3, 2, [Integer(12), Complex(1, 4), Integer(122), Complex(10, 2), Integer(4), Complex(2, -5)])
        matrix2 = Matrix.make_matrix_from_string('12 4i+1,122 2i+10,4 -5i+2')
        self.assertEqual(matrix,matrix2)

    def test_add_integer_and_complex(self):
        num = Integer(34)
        com = Complex(6, -2)
        self.assertEqual(com + num, Complex(40, -2))
        self.assertEqual(num + com, Complex(40, -2))
        self.assertEqual(num + num, Integer(68))
        self.assertEqual(com + com, Complex(12, -4))

    def test_add_matrix(self):
        num = Integer(34)
        com = Complex(6, -2)
        matrix = Matrix.make_unit_matrix(3)
        matrix2 = Matrix(3,3, [Integer(5), Integer(7), Complex(2, 4), Integer(7), Integer(2), Integer(8), Complex(1, 4), Integer(4), Complex(9, 4)])
        self.assertEqual(matrix + matrix2, Matrix(3,3,[Integer(6), Integer(7), Complex(2, 4), Integer(7), Integer(3), Integer(8), Complex(1, 4), Integer(4), Complex(10, 4)]))
        self.assertEqual(matrix + Integer(1), Matrix(3, 3, [Integer(2),Integer(1),Integer(1),Integer(1),Integer(2),Integer(1),Integer(1),Integer(1),Integer(2)]))
        self.assertEqual(matrix + Complex(1, 2), Matrix(3, 3,[Complex(2, 2),Complex(1, 2),Complex(1, 2),Complex(1, 2),Complex(2, 2),Complex(1, 2),Complex(1, 2),Complex(1, 2),Complex(2, 2)]))
        self.assertEqual(Integer(1) + matrix, Matrix(3, 3, [Integer(2),Integer(1),Integer(1),Integer(1),Integer(2),Integer(1),Integer(1),Integer(1),Integer(2)]))
        self.assertEqual(Complex(1, 2) + matrix, Matrix(3, 3,[Complex(2, 2),Complex(1, 2),Complex(1, 2),Complex(1, 2),Complex(2, 2),Complex(1, 2),Complex(1, 2),Complex(1, 2),Complex(2, 2)]))
    
    def test_mul_integer_and_complex(self):
        num = Integer(3)
        com = Complex(6, -2)
        self.assertEqual(com * num, Complex(18, -6))
        self.assertEqual(num * com, Complex(18, -6))
        self.assertEqual(num * num, Integer(9))
        self.assertEqual(com * com, Complex(32, -24))

    def test_mul_matrix(self):
        com = Complex(6, -2)
        matrix = Matrix.make_unit_matrix(2)
        matrix2 = Matrix(2,2, [Integer(5), Integer(7), Complex(2, 4), Integer(7)])
        self.assertEqual(matrix * matrix2, matrix2)
        self.assertEqual(matrix *Integer(2), Matrix(2, 2, [Integer(2),Integer(0),Integer(0),Integer(2)]))
        self.assertEqual(Integer(2)*matrix, Matrix(2, 2, [Integer(2),Integer(0),Integer(0),Integer(2)]))
        self.assertEqual(matrix *Complex(2, 3), Matrix(2, 2, [Complex(2, 3),Integer(0),Integer(0),Complex(2, 3)]))
        self.assertEqual(Complex(2, 3) * matrix, Matrix(2, 2, [Complex(2, 3),Integer(0),Integer(0),Complex(2, 3)]))

# running the tests
run_tests(matrix_tests)