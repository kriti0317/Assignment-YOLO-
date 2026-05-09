import os
from pathlib import Path
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np

# ---- Paths ----
model_path = r"C:\Users\Kriti\OneDrive\Desktop\Assigment of AI\best.pt"
pdf_to_image_folder = r"C:\Users\Kriti\Downloads\pdf"
cropped_output_folder = r"C:\Users\Kriti\Downloads\cropped-outputs"
# local_pdf_folder = r"C:\Users\Kriti\Downloads\pdf

# Create folders if they don't exist
os.makedirs(pdf_to_image_folder, exist_ok=True)
os.makedirs(cropped_output_folder, exist_ok=True)
# os.makedirs(local_pdf_folder, exist_ok=True)

# ---- Load Model ----
model = YOLO(model_path)

st.title("📄 Document or Image Dectection Using YOLO")

# ---- File Uploader ----
uploaded_files = st.file_uploader("Upload PDFs or Images", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

# ---- Helper: Convert PIL to OpenCV ----
def pil_to_cv2(pil_img):
    return cv2.cvtColor(np.array(pil_img.convert("RGB")), cv2.COLOR_RGB2BGR)

# ---- Save and Show Crops ----
def save_and_show_crops(image_cv2, results, base_name):
    label_counts = {}
    crops = []
    captions = []

    for i, box in enumerate(results[0].boxes):
        cls_id = int(box.cls[0])
        label = results[0].names[cls_id]
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        label_counts[label] = label_counts.get(label, 0) + 1
        crop_name = f"{base_name}_{label}_{label_counts[label]}.png"
        crop_path = os.path.join(cropped_output_folder, crop_name)

        crop = image_cv2[y1:y2, x1:x2]
        cv2.imwrite(crop_path, crop)

        crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
        crops.append(crop_rgb)
        captions.append(crop_name)

    # Show all cropped images in one row
    cols = st.columns(len(crops))
    for col, img, cap in zip(cols, crops, captions):
        col.image(img, caption=cap, use_container_width=True)


# ---- Process PIL Image with YOLO ----
def process_image(pil_img, base_name):
    image_cv2 = pil_to_cv2(pil_img)
    results = model(image_cv2)
    save_and_show_crops(image_cv2, results, base_name)

# ---- Handle One or More Images ----
def handle_images(images, base_name):
    for i, img in enumerate(images):
        name = f"{base_name}_page_{i+1}" if len(images) > 1 else base_name
        process_image(img, name)

# ---- Handle Uploaded Files ----
if uploaded_files:
    st.subheader("📤 Uploaded Files")
    for file in uploaded_files:
        file_name = Path(file.name).stem
        if file.type == "application/pdf":
            images = convert_from_bytes(file.read())
            handle_images(images, file_name)
        elif "image" in file.type:
            img = Image.open(file)
            handle_images([img], file_name)

# ---- Handle Local PDFs ----
# if os.path.exists(local_pdf_folder):
#     st.subheader("📂 Local PDFs")
#     for filename in os.listdir(local_pdf_folder):
#         if filename.lower().endswith(".pdf"):
#             pdf_path = os.path.join(local_pdf_folder, filename)
#             pdf_name = Path(filename).stem
#             images = convert_from_path(pdf_path)
#             handle_images(images, pdf_name)
