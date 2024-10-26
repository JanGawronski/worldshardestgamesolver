from math import sin, cos, pi, e

print(e)
multiplier = 1
print([(int((2.718281828459045**(i/400*6.283185307179586 * 1j)*100 * multiplier).real), int((2.718281828459045**(i/400*6.283185307179586 * 1j)*100 * multiplier).imag)) for i in range(100)])