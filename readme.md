# Advanced Image Filter Studio 🎨

## Overview
This **Advanced Image Filter App** is a Streamlit based web application that allows users to upload an image, apply various filters, and download the processed image. The app provides a user friendly interface with customizable filter options and real time image processing.


## Features
- **Upload Images**: Supports `.jpg`, `.jpeg`, and `.png` formats.
- **Apply Filters**:
  - Grayscale
  - Blur (Adjustable intensity)
  - Edge Detection
  - Sepia Effect
  - Pencil Sketch
  - Invert Colors
  - Background Removal (using MediaPipe)
- **Customizable Parameters**:
  - Blur Intensity
  - Canny Edge Detection Thresholds
- **Download Processed Image**: Save the final image in `.png` format.
- **Custom Styling**:
  - Beautiful background and sidebar designs.
  - Stylish buttons and layout.


## Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Dependencies
- **Streamlit**: For building the web app.
- **OpenCV**: For image processing.
- **NumPy**: For numerical operations.
- **Pillow**: For image handling.
- **MediaPipe**: For background removal.


## How to Use
1. **Upload an Image**: Use the sidebar to upload your image.
2. **Choose Filters**: Select one or more filters from the sidebar.
3. **Adjust Parameters**: Customize filter parameters such as blur intensity or edge detection thresholds.
4. **View Results**: See the original and processed images side by side.
5. **Download**: Click the download button to save the processed image.

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/).
