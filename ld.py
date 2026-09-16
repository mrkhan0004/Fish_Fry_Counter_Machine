import cv2
from ultralytics import YOLO

model = YOLO("/media/sahil-khan/New Volume1/linux/Computer/RohitSir_FishProject/runs/detect/train6/weights/best.pt")

# Try different webcam ID
cam_id = 0
cap = cv2.VideoCapture(cam_id)


if not cap.isOpened():
    print("❌ Camera not opened! Trying next...")
    for i in range(1, 4):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ Camera found at index {i}")
            break

print("🚀 Live detection... Press Q to exit")

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("❌ No camera frame!")
        break

    results = model.predict(frame, conf=0.5, imgsz=640, device=0, verbose=False)
    annotated_frame = results[0].plot()

    cv2.imshow("YOLOv8 Live", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
