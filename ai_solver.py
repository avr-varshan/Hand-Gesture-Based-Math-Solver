import google.generativeai as genai
from PIL import Image
import numpy as np

def solve_expression_ai(canvas: np.ndarray, gemini_api_key: str):
    """
    Sends canvas to Gemini AI for solving.

    Args:
        canvas (np.ndarray): The drawn canvas with the expression.
        gemini_api_key (str): Your Gemini API key from .env.

    Returns:
        tuple(str, str): (recognized_expr, result)
    """
    # Create a PIL image from the canvas
    pil_image = Image.fromarray(canvas)

    # Configure Gemini with provided API key
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        # Example usage: We combine a text prompt + the image
        response = model.generate_content(["Solve this math problem", pil_image])
        # If successful, response.text should have the AI's answer
        if response and response.text:
            return "AI recognized expression", response.text.strip()
        else:
            return "No expression recognized", "AI returned empty response"
    except Exception as e:
        return "Error in AI mode", f"AI error: {e}"
