import cv2
import numpy as np
import mediapipe as mp
import streamlit as st

# Mediapipe Hands setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

tip_ids = [4, 8, 12, 16, 20]

def find_hands(img, draw=True, flip_type=True):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    all_hands = []
    h, w, c = img.shape

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_type, hand_landmarks in zip(
            results.multi_handedness,
            results.multi_hand_landmarks
        ):
            my_hand = {}
            lm_list = []
            x_list, y_list = [], []

            for lm in hand_landmarks.landmark:
                px, py, pz = int(lm.x * w), int(lm.y * h), lm.z * w
                lm_list.append([px, py, pz])
                x_list.append(px)
                y_list.append(py)

            xmin, xmax = min(x_list), max(x_list)
            ymin, ymax = min(y_list), max(y_list)
            bbox = (xmin, ymin, xmax - xmin, ymax - ymin)
            cx, cy = (xmin + xmax) // 2, (ymin + ymax) // 2

            my_hand["lmList"] = lm_list
            my_hand["bbox"] = bbox
            my_hand["center"] = (cx, cy)

            if flip_type and hand_type.classification[0].label == "Right":
                my_hand["type"] = "Left"
            else:
                my_hand["type"] = "Right"

            all_hands.append(my_hand)

            if draw:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    return all_hands, img

def fingers_up(hand):
    lm_list = hand["lmList"]
    hand_type = hand.get("type", "Right")
    fingers = []

    if hand_type == "Right":
        fingers.append(1 if lm_list[tip_ids[0]][0] > lm_list[tip_ids[0] - 1][0] else 0)
    else:
        fingers.append(1 if lm_list[tip_ids[0]][0] < lm_list[tip_ids[0] - 1][0] else 0)

    for id in range(1, 5):
        fingers.append(1 if lm_list[tip_ids[id]][1] < lm_list[tip_ids[id] - 2][1] else 0)

    return fingers

def draw_on_canvas(fingers, lm_list, prev_pos, canvas):
    current_pos = None

    if fingers == [0, 1, 0, 0, 0]:
        current_pos = lm_list[8][0:2]
        if prev_pos is None:
            prev_pos = current_pos
        cv2.line(canvas, tuple(prev_pos), tuple(current_pos), (255, 0, 255), 10)
        prev_pos = current_pos

    elif fingers == [1, 0, 0, 0, 0]:
        canvas = np.zeros_like(canvas)
        prev_pos = None
        st.session_state["recognized_expr"] = ""
        st.session_state["evaluation_result"] = ""

    else:
        prev_pos = None

    return prev_pos, canvas
