from pdf2image import convert_from_path
import os

# Define the directory where your PDFs are located
pdf_dir = r"C:\Users\Kriti\Downloads\pdf"

# Define the directory where you want to save the output images
output_dir = r'C:\Users\Kriti\Downloads\pdf'
os.makedirs(output_dir, exist_ok=True)

# Path to the bin folder of Poppler
poppler_path = r"F:\poppler-24.08.0\Library\bin"  

# Loop through each file in the PDF directory
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_dir, filename)
        print(f"Converting: {filename}")
        
        # Convert PDF pages to images
        pages = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)  # ✅ use poppler_path here

        for i, page in enumerate(pages):
            img_filename = f"{os.path.splitext(filename)[0]}_page{i+1}.jpg"
            img_path = os.path.join(output_dir, img_filename)
            page.save(img_path, "JPEG")
            print(f"Saved: {img_path}")
