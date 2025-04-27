# app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import mediapipe as mp  # NEW for background removal

# ----- Custom CSS Styling -----
def local_css():
    st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-image: url('https://img.freepik.com/free-photo/arrows-pastel-colors_23-2148488400.jpg?semt=ais_hybrid&w=740');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        min-height: 100vh;
        color: darkred;
    }

    /* Sidebar Background */
    section[data-testid="stSidebar"] {
        background-image: url('https://i.pinimg.com/736x/10/76/df/1076df6744238e75e79047f7c2d2bbec.jpg');
        background-size: cover;
        background-position: center;
    }

    /* Container Styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
        border-radius: 15px;
        padding: 20px;
    }

    /* Button Styling */
    .stButton > button {
        color: white;
        background: linear-gradient(45deg, #ff6a00, #ee0979);
        border: none;
        border-radius: 10px;
        padding: 0.75em 1.5em;
        font-size: 1.1em;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #43cea2, #185a9d);
    }

    /* Profile Links Styling */
    .profile-links img {
        vertical-align: middle;
        margin-right: 8px;
    }
    .profile-links a {
        text-decoration: none;
        color: #333;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

def sidebar_profiles():
    st.sidebar.markdown("### 🎉Author: Maria Nadeem🌟")
    st.sidebar.markdown("### 🔗 Connect With Me")
    st.sidebar.markdown("""
    <hr>
    <div class="profile-links">
        <a href="https://github.com/marianadeem755" target="_blank">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20px"> GitHub
        </a><br><br>
        <a href="https://www.kaggle.com/marianadeem755" target="_blank">
            <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/189_Kaggle_logo_logos-512.png" width="20px"> Kaggle
        </a><br><br>
        <a href="mailto:marianadeem755@gmail.com">
            <img src="https://cdn-icons-png.flaticon.com/512/561/561127.png" width="20px"> Email
        </a><br><br>
        <a href="https://huggingface.co/maria355" target="_blank">
            <img src="https://huggingface.co/front/assets/huggingface_logo-noborder.svg" width="20px"> Hugging Face
        </a>
    </div>
    <hr>
    """, unsafe_allow_html=True)

# ----- Filters Functions -----
def apply_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_blur(img, ksize):
    return cv2.GaussianBlur(img, (ksize, ksize), 0)

def apply_canny(img, threshold1, threshold2):
    return cv2.Canny(img, threshold1, threshold2)

def apply_sepia(img):
    kernel = np.array([[0.272, 0.534, 0.131],
                       [0.349, 0.686, 0.168],
                       [0.393, 0.769, 0.189]])
    sepia_img = cv2.transform(img, kernel)
    sepia_img = np.clip(sepia_img, 0, 255)
    return sepia_img

def apply_pencil_sketch(img):
    if len(img.shape) == 3:
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray_img = img
    inv_img = 255 - gray_img
    blur_img = cv2.GaussianBlur(inv_img, (21, 21), 0)
    sketch = cv2.divide(gray_img, 255 - blur_img, scale=256)
    return sketch

def apply_invert(img):
    return cv2.bitwise_not(img)

def apply_background_removal(img):
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = selfie_segmentation.process(rgb_img)
        mask = results.segmentation_mask
        condition = mask > 0.5
        bg_color = np.ones(img.shape, dtype=np.uint8) * 255
        output_img = np.where(condition[..., None], img, bg_color)
        return output_img

# Convert to PIL
def convert_image(img):
    if len(img.shape) == 2:
        return Image.fromarray(img)
    else:
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Downloadable image
def download_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# ----- Streamlit App Starts Here -----
def main():
    st.set_page_config(page_title="Advanced Image Filter Studio", page_icon="🎨", layout="wide")
    local_css()

    st.title("🎨 Advanced Image Filter Studio")
    st.write("Upload an image, apply **amazing filters**, and download your creation!")

    # Sidebar Profiles
    sidebar_profiles()

    # Sidebar
    st.sidebar.header("1. Upload Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        opencv_image = cv2.imdecode(file_bytes, 1)

        # Filters Section
        st.sidebar.header("2. Choose Filters")
        grayscale = st.sidebar.checkbox("Grayscale")
        blur = st.sidebar.checkbox("Blur")
        canny = st.sidebar.checkbox("Edge Detection")
        sepia = st.sidebar.checkbox("Sepia Effect")
        sketch = st.sidebar.checkbox("Pencil Sketch")
        invert = st.sidebar.checkbox("Invert Colors")
        remove_bg = st.sidebar.checkbox("Remove Background (Simple)")

        st.sidebar.header("3. Filter Parameters")
        blur_strength = st.sidebar.slider("Blur Intensity (odd numbers)", 1, 49, 15, step=2)
        threshold1 = st.sidebar.slider("Canny Threshold1", 50, 300, 100)
        threshold2 = st.sidebar.slider("Canny Threshold2", 50, 300, 150)

        # Process Image
        final_image = opencv_image.copy()

        with st.spinner("🖌️ Applying Filters..."):
            if grayscale:
                final_image = apply_grayscale(final_image)

            if blur:
                if len(final_image.shape) == 2:
                    final_image = cv2.cvtColor(final_image, cv2.COLOR_GRAY2BGR)
                final_image = apply_blur(final_image, blur_strength)

            if canny:
                if len(final_image.shape) != 2:
                    final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)
                final_image = apply_canny(final_image, threshold1, threshold2)

            if sepia:
                if len(final_image.shape) == 2:
                    final_image = cv2.cvtColor(final_image, cv2.COLOR_GRAY2BGR)
                final_image = apply_sepia(final_image)

            if sketch:
                if len(final_image.shape) != 2:
                    final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2GRAY)
                final_image = apply_pencil_sketch(final_image)

            if invert:
                final_image = apply_invert(final_image)

            if remove_bg:
                if len(final_image.shape) != 3 or final_image.shape[2] != 3:
                    final_image = cv2.cvtColor(final_image, cv2.COLOR_GRAY2BGR)
                final_image = apply_background_removal(final_image)

        # Columns to show images
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(uploaded_file, use_column_width=True)

        with col2:
            st.subheader("Processed Image")
            final_pil = convert_image(final_image)
            st.image(final_pil, use_column_width=True)

        # Download button
        st.markdown("---")
        st.download_button(
            label="📥 Download Processed Image",
            data=download_image(final_pil),
            file_name="processed_image.png",
            mime="image/png"
        )
    else:
        st.info("👈 Please upload an image from the sidebar to get started.")

if __name__ == "__main__":
    main()
