"""
Copyright (c) 2025 Unicorn. Всі права захищені.
"""

import math

def main():
    try:
        a = float(input("Input the value for a: "))
        b = float(input("Input the value for b: "))

        r = math.exp(a)
        t = math.log(abs(b + 1))
        
        print("Your values: a =", a, ", b =", b)
        
        if t >= 0:
            y = r + t
            print("Result of calculation: y =", y)
        else:
            print("Absolut value is less than or equal to 0, calculation cannot be processed.")
    
    except ValueError as ve:
        print("Error: the input value is incorrect. Details:", ve)
    except Exception as e:
        print("Unexpected error accure:", e)

if __name__ == "__main__":
    main()