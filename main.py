import os
import cv2
import numpy as np
import streamlit as st
from PIL import Image
from dotenv import load_dotenv

from gesture_utils import find_hands, fingers_up, draw_on_canvas
from solver import solve_expression_from_canvas
from ai_solver import solve_expression_ai

# Load environment variables
load_dotenv()

# Retrieve the Gemini API key from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure .env has GEMINI_API_KEY=your_api_key
if not GEMINI_API_KEY:
    st.error("Gemini API key not found in environment variables. Please set GEMINI_API_KEY in .env.")

# Streamlit page configuration
st.set_page_config(page_title="Hand Gesture Based Math Solver", page_icon="🖐️", layout="wide")
st.title("🖐️ Hand Gesture Solver")

# Sidebar for mode selection
st.sidebar.header("Mode Selection")
mode = st.sidebar.radio("Choose a mode:", ("Normal Mode", "AI Mode"))

# Sidebar instructions
st.sidebar.header("Instructions")
st.sidebar.info("""
**Hand Gestures**:
- **Index finger up**: Draw on the canvas.
- **Thumb up**: Clear the canvas & reset expression/result.
- **All fingers up except pinky**: Solve the expression from the drawn image (according to the selected mode).
""")

# Initialize Streamlit session states
if "recognized_expr" not in st.session_state:
    st.session_state["recognized_expr"] = ""
if "evaluation_result" not in st.session_state:
    st.session_state["evaluation_result"] = ""

# Initialize the webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Frame width
cap.set(4, 720)  # Frame height

# Create a blank black canvas for drawing
canvas = np.zeros((720, 1280, 3), dtype=np.uint8)
prev_pos = None  # Track previous drawing position

# Streamlit layout: two columns
col1, col2 = st.columns([3, 2])

with col1:
    # Initialize the image placeholder with a blank canvas
    FRAME_WINDOW = st.image(canvas, caption="Webcam Feed + Drawing", use_container_width=True)

with col2:
    st.subheader("Recognized Expression")
    expr_placeholder = st.empty()
    st.subheader("Result")
    result_placeholder = st.empty()

# Main loop to read frames from the webcam
while cap.isOpened():
    success, img = cap.read()
    if not success:
        st.warning("Could not read from webcam. Please ensure it's connected.")
        break

    # Flip horizontally (mirror effect)
    img = cv2.flip(img, 1)

    # Detect hands in the current frame
    hands_info, img = find_hands(img, draw=False)

    if hands_info:
        # Take the first detected hand
        hand = hands_info[0]
        finger_list = fingers_up(hand)

        # Draw or clear the canvas
        prev_pos, canvas = draw_on_canvas(finger_list, hand["lmList"], prev_pos, canvas)

        # If all fingers except pinky are up => Solve expression
        if finger_list == [1, 1, 1, 1, 0]:
            if mode == "AI Mode":
                # Solve via Gemini AI
                st.session_state["recognized_expr"], st.session_state["evaluation_result"] = solve_expression_ai(
                    canvas, GEMINI_API_KEY
                )
            else:
                # Normal Mode (OCR + Sympy)
                st.session_state["recognized_expr"], st.session_state["evaluation_result"] = solve_expression_from_canvas(canvas)

    # Blend the webcam feed with the drawing overlay
    combined = cv2.addWeighted(img, 0.7, canvas, 0.3, 0)
    FRAME_WINDOW.image(combined, channels="BGR")

    # Display recognized expression and result in real time
    expr_placeholder.text(st.session_state["recognized_expr"])
    result_placeholder.text(st.session_state["evaluation_result"])

cap.release()
cv2.destroyAllWindows()
