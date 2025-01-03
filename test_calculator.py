# test_calculator.py

import subprocess

def run_calculator(*args):
    """Helper function to run the calculator script and return the output."""
    result = subprocess.run(
        ['python', 'calculator.py'] + list(args),
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def test_addition():
    result = run_calculator('add', '2', '3')
    assert result == "Result: 5.0"

def test_subtraction():
    result = run_calculator('subtract', '5', '3')
    assert result == "Result: 2.0"

def test_multiplication():
    result = run_calculator('multiply', '2', '3')
    assert result == "Result: 6.0"

def test_division():
    result = run_calculator('divide', '6', '3')
    assert result == "Result: 2.0"

def test_division_by_zero():
    result = run_calculator('divide', '6', '0')
    assert result == "Result: Error: Division by zero is not allowed."
