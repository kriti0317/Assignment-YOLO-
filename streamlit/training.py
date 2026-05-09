from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("yolov8n.pt")

# Train the model
model.train(
    data="C:/Users/Kriti/OneDrive/Desktop/Assigment of AI/streamlit/data.yaml",
    epochs=30,
    imgsz=640
)

