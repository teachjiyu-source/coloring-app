import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

st.set_page_config(page_title="My Coloring Book", layout="wide")
st.title("🎨 Adult Coloring Page Creator")

def process_image(image, thickness):
    img = np.array(image.convert('RGB'))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Use thickness variable from slider
    edges = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 11, thickness
    )
    return edges

uploaded_file = st.file_uploader("Upload a photo", type=["jpg", "png", "jpeg"])

if uploaded_file:
    # Sidebar slider for customization
    line_thickness = st.sidebar.slider("Line Boldness", 1, 15, 5)
    
    image = Image.open(uploaded_file)
    processed_img = process_image(image, line_thickness)
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(image, caption="Original")
    with col2:
        st.image(processed_img, caption="Your Coloring Page")
        
        # --- NEW: DOWNLOAD BUTTON LOGIC ---
        # Convert the processed image back to a format you can download
        is_success, buffer = cv2.imencode(".png", processed_img)
        io_buf = io.BytesIO(buffer)
        
        st.download_button(
            label="📥 Download Coloring Page for Printing",
            data=io_buf,
            file_name="my_coloring_page.png",
            mime="image/png"
        )
