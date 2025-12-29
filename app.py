import streamlit as st
import cv2
import numpy as np
from PIL import Image
import os

# --- INITIALIZATION ---
STORAGE_PATH = "my_collection"
if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

st.set_page_config(page_title="Sketch Studio", layout="wide")

# --- CUSTOM CSS FOR BETTER UI ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

def transform_to_coloring_page(img, detail, thickness):
    # Convert to grayscale
    img_array = np.array(img.convert('RGB'))
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    
    # 1. Denoise/Smooth (Detail control)
    # Higher detail = lower blur
    blur_value = detail if detail % 2 != 0 else detail + 1
    smoothed = cv2.medianBlur(gray, blur_value)
    
    # 2. Adaptive Threshold for clean outlines
    edges = cv2.adaptiveThreshold(
        smoothed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 9, thickness
    )
    
    return edges

# --- UI LAYOUT ---
st.title("🖌️ Web Sketch Studio")
st.write("Convert any photo into a custom adult coloring page.")

with st.sidebar:
    st.header("Settings")
    detail_level = st.slider("Detail Level", 1, 9, 3, help="Higher = smoother lines")
    line_thickness = st.slider("Line Strength", 1, 10, 5)
    
    st.divider()
    st.header("Saved Pages")
    files = os.listdir(STORAGE_PATH)
    for f in files:
        if st.button(f"View {f[:10]}...", key=f):
            st.image(os.path.join(STORAGE_PATH, f))

# --- MAIN UPLOADER ---
uploaded_file = st.file_uploader("Drop an image here", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    result = transform_to_coloring_page(image, detail_level, line_thickness)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(image)
    with col2:
        st.subheader("Coloring Draft")
        st.image(result)
        
        # Download and Save Options
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("Save to History"):
                save_name = f"sketch_{len(os.listdir(STORAGE_PATH))}.png"
                cv2.imwrite(os.path.join(STORAGE_PATH, save_name), result)
                st.success("Saved!")
                st.rerun()
