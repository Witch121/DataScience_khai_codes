def is_even(number: int) -> bool:
    """
    Check if a number is even.

    Parameters:
        number (int): The number to check.

    Returns:
        bool: True if the number is even, False otherwise.
    """
    return number % 2 == 0

# Example usage
num = 10
if is_even(num):
    print(f"{num} is even.")
else:
    print(f"{num} is odd.")