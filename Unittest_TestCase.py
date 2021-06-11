import unittest


def fib(n):
    """
    Вычислает число Фибонаачи номер n.
    Выбрасывает исключение TypeError, если вызвано не для целочисленного типа.
    Выбрасывает исключение ValueError, если число отрицательное или больше
    допустимого по контракту.
    :param n: целое число от 0 до 9999
    :return: целое число от 0 до ....
    """
    if not isinstance(n, int):
        raise TypeError("Fibonacci function can work only with <class 'int'> type.")
    if n < 0:
        raise ValueError("Fibonacci can't work with negative numbers.")
    if n >= 10000:
        raise ValueError("Fibonacci can't work with numbers larger than 9999.")
    if n == 0:
        return 0
    f_2 = 0
    f_1 = 1
    for i in range(2, n + 1):
        f_1, f_2 = (f_1 + f_2), f_1
    return f_1


class TestFibonacci(unittest.TestCase):

    def test_simple(self):
        for param, result in [(0, 0), (1, 1), (2, 1), (3, 2), (10, 55)]:
            self.assertEqual(fib(param), result)

    def test_stress(self):
        with self.assertRaises(ValueError):
            fib(10000)

    def test_negative(self):
        with self.assertRaises(ValueError):
            fib(-1)
        with self.assertRaises(ValueError):
            fib(-100)

    def test_wrong_param_type(self):
        with self.assertRaises(TypeError):
            fib(2.5)
        with self.assertRaises(TypeError):
            fib('Hello')


if __name__ == '__main__':
    unittest.main()
