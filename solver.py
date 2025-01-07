# solver.py

import re
import numpy as np
from PIL import Image
from paddleocr import PaddleOCR
from sympy import sympify

# Initialize PaddleOCR once to improve performance
ocr = PaddleOCR(use_angle_cls=True, lang="en")

def extract_text_from_image(canvas: np.ndarray) -> str:
    """
    Convert a canvas (np.ndarray) to text using PaddleOCR.

    Args:
        canvas (np.ndarray): The drawn canvas containing handwriting.

    Returns:
        str: The extracted text (could be empty if no text is recognized).
    """
    pil_image = Image.fromarray(canvas)
    results = ocr.ocr(np.array(pil_image), cls=True)
    if not results or not results[0]:
        return ""
    return " ".join([line[1][0] for line in results[0]]).strip()

def preprocess_expression(expression: str) -> str:
    """
    Basic preprocessing of the raw recognized text.

    Steps:
    - Convert '^' => '**'
    - Convert '÷' => '/'
    - Remove extra whitespace
    - Replace '3x2' => '3*2'

    Args:
        expression (str): The raw OCR text.

    Returns:
        str: A simpler expression for SymPy evaluation.
    """
    # Replacements
    expression = expression.replace("^", "**").replace("÷", "/")
    # Remove extra whitespace
    expression = re.sub(r'\s+', '', expression)
    # Replace '3x2' or '3X2' => '3*2'
    expression = re.sub(r'(\d)[xX](\d)', r'\1*\2', expression)
    return expression

def evaluate_expression(expression: str) -> str:
    """
    Evaluate the expression with SymPy.

    Args:
        expression (str): Preprocessed Pythonic math expression.

    Returns:
        str: The numeric result (as a string), or an error message if invalid.
    """
    try:
        result = sympify(expression).evalf()
        return str(result)
    except Exception as e:
        # Return a friendly error
        return f"Error: {e}"

def solve_expression_from_canvas(canvas: np.ndarray):
    """
    High-level function to solve the expression from a drawn canvas.

    Steps:
    1. OCR => raw text
    2. Preprocess => Pythonic expression
    3. Evaluate => numeric result or error

    Args:
        canvas (np.ndarray): The drawn canvas image.

    Returns:
        tuple(str, str): (preprocessed_expr, result)
    """
    raw_text = extract_text_from_image(canvas)
    preprocessed_expr = preprocess_expression(raw_text)
    result = evaluate_expression(preprocessed_expr)
    return preprocessed_expr, result
