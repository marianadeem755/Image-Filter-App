# app.py

import streamlit as st
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import requests
import os
from dotenv import load_dotenv
import base64

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
REMOVE_BG_API_KEY = os.getenv("REMOVE_BG_API_KEY")

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

# ----- Background Removal using API -----
def remove_background_api(image_data, bg_color=None):
    """
    Remove background from image using Remove.bg API
    
    Args:
        image_data: Image as bytes
        bg_color: Background color in hex format without # (e.g. "FFFFFF" for white)
                  If None, transparent background will be used
    
    Returns:
        Image with background removed as bytes
    """
    try:
        url = "https://api.remove.bg/v1.0/removebg"
        
        # Set up the headers with API key
        headers = {
            'X-Api-Key': REMOVE_BG_API_KEY,
        }
        
        # Set up the data payload
        data = {
            'size': 'auto',
            'format': 'auto',
        }
        
        # Add background color if specified
        if bg_color:
            data['bg_color'] = bg_color
        
        # Set up the files payload
        files = {
            'image_file': image_data,
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, data=data, files=files)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error: {response.status_code}, {response.text}")
            return None
    
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

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

# Convert PIL Image to bytes
def pil_to_bytes(pil_img, format="PNG"):
    buf = BytesIO()
    pil_img.save(buf, format=format)
    return buf.getvalue()

# Convert bytes to PIL Image
def bytes_to_pil(img_bytes):
    return Image.open(BytesIO(img_bytes))

# Convert to PIL
def convert_image(img):
    if len(img.shape) == 2:
        return Image.fromarray(img)
    else:
        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

# Downloadable image
def download_image(img):
    if isinstance(img, bytes):
        return img
    else:
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

    # API Key Status Check
    if not REMOVE_BG_API_KEY:
        st.sidebar.warning("⚠️ No Remove.bg API key found in .env file. Background removal will not work.")
    else:
        st.sidebar.success("✅ Remove.bg API key detected")

    # Sidebar
    st.sidebar.header("1. Upload Image")
    uploaded_file = st.sidebar.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Read the uploaded file
        file_bytes = uploaded_file.getvalue()
        opencv_image = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), 1)
        pil_image = Image.open(uploaded_file)

        # Store original image for display
        original_image = opencv_image.copy()

        # Filters Section
        st.sidebar.header("2. Choose Filters")
        grayscale = st.sidebar.checkbox("Grayscale")
        blur = st.sidebar.checkbox("Blur")
        canny = st.sidebar.checkbox("Edge Detection")
        sepia = st.sidebar.checkbox("Sepia Effect")
        sketch = st.sidebar.checkbox("Pencil Sketch")
        invert = st.sidebar.checkbox("Invert Colors")
        remove_bg = st.sidebar.checkbox("Remove Background (API)")

        st.sidebar.header("3. Filter Parameters")
        blur_strength = st.sidebar.slider("Blur Intensity (odd numbers)", 1, 49, 15, step=2)
        threshold1 = st.sidebar.slider("Canny Threshold1", 50, 300, 100)
        threshold2 = st.sidebar.slider("Canny Threshold2", 50, 300, 150)
        
        # Background Removal Parameters (only show if remove_bg is selected)
        bg_removed_image = None
        if remove_bg:
            if REMOVE_BG_API_KEY:
                st.sidebar.subheader("Background Removal Settings")
                bg_type = st.sidebar.radio("Background Type", ["Transparent", "Solid Color"])
                
                if bg_type == "Solid Color":
                    bg_color = st.sidebar.color_picker("Background Color", "#FFFFFF")
                    # Remove # from hex color
                    bg_color = bg_color[1:]
                else:
                    bg_color = None
            else:
                st.sidebar.error("API key is required for background removal")

        # Process Image
        final_image = opencv_image.copy()
        processing_complete = True

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

        # Convert the processed image to PIL
        final_pil = convert_image(final_image)

        # Handle background removal separately (API call)
        if remove_bg and REMOVE_BG_API_KEY:
            with st.spinner("🔄 Removing background using API - this may take a moment..."):
                # Convert the processed image back to bytes for API call
                processed_bytes = pil_to_bytes(final_pil)
                
                # Call the API to remove background
                bg_removed_bytes = remove_background_api(processed_bytes, bg_color)
                
                if bg_removed_bytes:
                    # Convert the response bytes back to PIL image
                    bg_removed_image = bytes_to_pil(bg_removed_bytes)
                    final_pil = bg_removed_image
                else:
                    st.error("Failed to remove background. Please try again later.")
                    processing_complete = False

        # Columns to show images
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Original Image")
            st.image(uploaded_file)

        with col2:
            st.subheader("Processed Image")
            if processing_complete:
                st.image(final_pil)

        # Download button
        if processing_complete:
            st.markdown("---")
            download_data = bg_removed_bytes if remove_bg and bg_removed_image else download_image(final_pil)
            st.download_button(
                label="📥 Download Processed Image",
                data=download_data,
                file_name="processed_image.png",
                mime="image/png"
            )
    else:
        st.info("👈 Please upload an image from the sidebar to get started.")

if __name__ == "__main__":
    main()
