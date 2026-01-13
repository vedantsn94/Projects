import streamlit as st
import cv2
import math
import cvzone
import tempfile
import numpy as np
import os
from datetime import datetime
from ultralytics import YOLO

# --------------------- CONFIG ---------------------
# Load YOLO model
model = YOLO("Weights/best.pt")

# Define class names
classNames = ['0', 'c', 'garbage', 'garbage_bag', 'sampah-detection', 'trash']

# Create folder for saving detected images
SAVE_DIR = "Detected_Images"
os.makedirs(SAVE_DIR, exist_ok=True)

# Streamlit page setup
st.set_page_config(page_title="Smart Waste Segregation System", layout="wide")
st.title("♻️ Software-Based Smart Waste Segregation System")

st.sidebar.header("Detection Mode")
mode = st.sidebar.radio("Choose a mode:", ["Upload Image", "Live Camera", "Mobile Camera"])


# --------------------- FUNCTIONS ---------------------
def detect_objects(img):
    """Run YOLO object detection and draw bounding boxes."""
    results = model(img)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            if conf > 0.3:
                cvzone.cornerRect(img, (x1, y1, w, h), t=2)
                cvzone.putTextRect(
                    img,
                    f'{classNames[cls]} {conf}',
                    (x1, y1 - 10),
                    scale=0.8,
                    thickness=1,
                    colorR=(255, 0, 0)
                )
    return img


def save_detected_image(image):
    """Save detected image with timestamp."""
    filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
    filepath = os.path.join(SAVE_DIR, filename)
    cv2.imwrite(filepath, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
    st.success(f"✅ Image saved as {filename} in '{SAVE_DIR}/'")
    return filepath


# --------------------- UPLOAD IMAGE ---------------------
if mode == "Upload Image":
    st.subheader("📸 Upload a waste image for detection")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        img = cv2.imread(tfile.name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        st.image(img, caption="Original Image", use_container_width=True)
        result_img = detect_objects(img.copy())
        st.image(result_img, caption="Detected Image", use_container_width=True)

        if st.button("💾 Save Detected Image"):
            save_detected_image(result_img)


# --------------------- LIVE CAMERA ---------------------
elif mode == "Live Camera":
    st.subheader("🎥 Live Camera Detection")
    run = st.checkbox("Start Camera")
    FRAME_WINDOW = st.image([])

    cap = cv2.VideoCapture(0)
    while run:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ Cannot access webcam.")
            break
        frame = cv2.flip(frame, 1)
        result_frame = detect_objects(frame)
        FRAME_WINDOW.image(result_frame, channels="BGR", use_container_width=True)

        # Save current frame button
        if st.button("💾 Save Current Frame"):
            save_detected_image(cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB))
    else:
        cap.release()
        st.write("🛑 Camera stopped.")


# --------------------- MOBILE CAMERA ---------------------
elif mode == "Mobile Camera":
    st.subheader("📱 Connect Mobile Camera (via IP Webcam App)")
    st.markdown("""
    **Instructions:**
    1. Install **IP Webcam** (Android) or **DroidCam** on your phone.  
    2. Connect your phone and laptop to the **same Wi-Fi network**.  
    3. Open the app → start the server → note the **IP address** shown (e.g. `http://192.168.1.100:8080/video`).  
    4. Enter that IP below.
    """)
    
    ip_link = st.text_input("Enter your IP camera URL:", "http://192.168.1.100:8080/video")
    start = st.checkbox("Start Mobile Camera")
    FRAME_WINDOW = st.image([])

    if start:
        cap = cv2.VideoCapture(ip_link)
        if not cap.isOpened():
            st.error("❌ Cannot connect to the mobile camera. Check IP link.")
        while start:
            ret, frame = cap.read()
            if not ret:
                st.warning("⚠️ Unable to read from the mobile camera.")
                break
            result_frame = detect_objects(frame)
            FRAME_WINDOW.image(result_frame, channels="BGR", use_container_width=True)

            # Save current frame button
            if st.button("💾 Save Current Frame"):
                save_detected_image(cv2.cvtColor(result_frame, cv2.COLOR_BGR2RGB))
        cap.release()
