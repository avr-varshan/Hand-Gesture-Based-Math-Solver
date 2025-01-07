# 🖐️ Math with Gestures

A real-time application that combines computer vision, hand gesture recognition, and optical character recognition (OCR) to **recognize handwritten mathematical expressions** and solve them effortlessly. Built using **Python, OpenCV, Mediapipe, PaddleOCR, and Streamlit**, this project offers an interactive way to solve mathematical expressions through gestures.

![Demo](https://via.placeholder.com/800x400?text=Demo+Image+Placeholder)  
<sup>*Replace this with an actual demo screenshot or GIF*</sup>

---

## 🚀 Features

- **Hand Gesture Recognition:**  
  - Draw on the screen by raising your **index finger**.
  - Clear the canvas by raising your **thumb**.
  - Solve drawn expressions by raising **all fingers except the pinky**.
  
- **Real-Time Processing:**  
  Combines live webcam feed with gesture-based drawing and mathematical evaluation.

- **Math Expression Solver:**  
  - Supports handwritten algebraic expressions like `2^3`, `sin(30)`, `5!`, and square roots.
  - Handles subscripts, superscripts, and common OCR challenges.

---

## 🔧️ Tech Stack

- **Languages:** Python  
- **Libraries:** 
  - [OpenCV](https://opencv.org/) - Video capture and image manipulation  
  - [Mediapipe](https://google.github.io/mediapipe/) - Hand gesture detection  
  - [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) - Optical character recognition  
  - [SymPy](https://www.sympy.org/) - Mathematical expression evaluation  
  - [Streamlit](https://streamlit.io/) - Interactive user interface  

---

## 📸 How It Works

1. **Start the application** to access the webcam feed.
2. **Use gestures** to interact with the canvas:
   - Draw mathematical expressions with your finger.
   - Clear the canvas using a thumb gesture.
   - Solve expressions by raising all fingers except the pinky.
3. **Real-time updates** for recognized expressions and results.

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Math-with-Gestures.git
   cd Math-with-Gestures
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   streamlit run main.py
   ```

---

## 📄 Project Structure

```plaintext
Math-with-Gestures/
├── main.py               # Main application logic
├── gesture_utils.py      # Gesture recognition and canvas handling
├── solver.py             # OCR and math expression solving
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
```

---

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or improvements:

1. Fork this repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Submit a pull request with detailed comments.

---

## 🤞🏻‍💻 Author

Your Name  

---

## 📜 License

This project is licensed under the MIT License. See LICENSE for details.

