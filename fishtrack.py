# import cv2
# import numpy as np
# import time
# import torch
# from ultralytics import YOLO
# from ultralytics.trackers import BYTETracker
# from ultralytics.utils import IterableSimpleNamespace
# from ultralytics.engine.results import Boxes

# # ==========================================
# # 1. CONFIGURATION
# # ==========================================
# MODEL_PATH = "/media/sahil-khan/New Volume/linux/Computer/RohitSir_FishProject/runs/detect/train6/weights/best.pt" 
# SOURCE = "/media/sahil-khan/New Volume/linux/Computer/RohitSir_FishProject/video/Hailuo_Video_An ultra-realistic top-down ov_464144277927747590.mp4" 

# SKIP_FRAMES = 2
# IMG_SIZE = 416       
# CONF_THRESHOLD = 0.4 

# LINE_START = (0, 400)
# LINE_END   = (1280, 400)

# # ==========================================
# # 2. TRACKER ARGS (COMPLETE SET)
# # ==========================================
# # Maine yahan wo saare variables add kar diye hain jinse AttributeError aata hai
# args_dict = {
#     'track_high_thresh': 0.5,
#     'track_low_thresh': 0.1,
#     'new_track_thresh': 0.6,
#     'track_buffer': 30,
#     'match_thresh': 0.8,
#     'fuse_score': True,    # <--- YEH WALA MISSING THA (Error solve karega)
#     'mot20': False
# }
# args = IterableSimpleNamespace(**args_dict)

# # ==========================================
# # 3. INITIALIZATION
# # ==========================================
# print("🔄 Loading Model...")
# model = YOLO(MODEL_PATH)
# tracker = BYTETracker(args, frame_rate=30)
# print("✅ Ready!")

# cap = cv2.VideoCapture(SOURCE)
# if not cap.isOpened():
#     print("❌ Error: Video file not found.")
#     exit()

# # Metadata for empty boxes
# orig_shape = (int(cap.get(4)), int(cap.get(3)))

# fish_count = 0
# crossed_ids = set() 
# previous_positions = {} 
# frame_count = 0
# start_time = time.time()
# fps = 0

# # ==========================================
# # 4. MAIN LOOP
# # ==========================================
# print("🚀 Running... Press 'q' to stop.")

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
        
#     frame_count += 1
#     if frame_count % 10 == 0:
#         fps = 10 / (time.time() - start_time)
#         start_time = time.time()
    
#     # Empty boxes setup to avoid 'NoneType' errors
#     tracker_input = Boxes(torch.empty((0, 6)), orig_shape) 

#     if frame_count % SKIP_FRAMES == 0:
#         results = model(frame, imgsz=IMG_SIZE, verbose=False, conf=CONF_THRESHOLD)
#         if results and len(results[0].boxes) > 0:
#             tracker_input = results[0].boxes
    
#     # TRACKING
#     online_targets = tracker.update(tracker_input, frame)
    
#     # LOGIC & DRAWING
#     for track in online_targets:
#         if not hasattr(track, 'track_id'): continue
        
#         track_id = track.track_id
#         x1, y1, x2, y2 = map(int, track.xyxy[0])
#         cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
#         if track_id in previous_positions:
#             prev_x, prev_y = previous_positions[track_id]
#             line_y = LINE_START[1]
            
#             # Line crossing logic
#             if (prev_y < line_y and cy >= line_y) or (prev_y > line_y and cy <= line_y):
#                 if track_id not in crossed_ids:
#                     fish_count += 1
#                     crossed_ids.add(track_id)

#         previous_positions[track_id] = (cx, cy)
        
#         # Visuals
#         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
#         cv2.putText(frame, f'Fish #{track_id}', (x1, y1 - 10), 
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#     # UI
#     cv2.line(frame, LINE_START, LINE_END, (0, 0, 255), 2)
#     cv2.rectangle(frame, (20, 20), (280, 100), (0,0,0), -1)
#     cv2.putText(frame, f'COUNT: {fish_count}', (40, 60), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
#     cv2.putText(frame, f'FPS: {fps:.1f}', (40, 90), 
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)

#     cv2.imshow('Fish Counting System', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()
# print("✅ Finished.")
# # ==========================================







#-----------------------------------------------------------------------------------------------------------------------------


import cv2
from ultralytics import YOLO

# ==========================================
# 1. CONFIGURATION
# ==========================================
MODEL_PATH = "/media/sahil-khan/New Volume/linux/Computer/RohitSir_FishProject/runs/detect/train6/weights/best.pt" 
SOURCE = "/media/sahil-khan/New Volume/linux/Computer/RohitSir_FishProject/video/Hailuo_Video_An ultra-realistic top-down ov_464144277927747590.mp4" 

# Model load karo
model = YOLO(MODEL_PATH)

# Unique fish count store karne ke liye set
counted_ids = set()

cap = cv2.VideoCapture(SOURCE)

print("🚀 Running Extreme Accuracy Mode for Crowded Fish...")

# ==========================================
# 2. MAIN LOOP
# ==========================================
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # --- CROWD CONTROL SETTINGS ---
    # 1. conf=0.15: Thoda low confidence taaki chhoti/dhundli fish bhi pakdi jayein.
    # 2. iou=0.3: Yeh sabse important hai. Isse overlapping boxes ko merge hone se roka jayega.
    # 3. imgsz=640: Standard resolution for detection.
    results = model.track(
        frame, 
        persist=True, 
        tracker="bytetrack.yaml", 
        conf=0.15, 
        iou=0.3,    # Low IOU helps in crowded scenes
        imgsz=640, 
        verbose=False
    )

    # Agar results mein boxes hain aur IDs assign hui hain
    if results[0].boxes is not None and results[0].boxes.id is not None:
        ids = results[0].boxes.id.cpu().numpy().astype(int)
        boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)

        for box, track_id in zip(boxes, ids):
            # Unique counting logic
            if track_id not in counted_ids:
                counted_ids.add(track_id)

            # --- DRAWING (Thin lines for clear visibility) ---
            x1, y1, x2, y2 = box
            # Green box draw karo (thin line = 1)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
            # Chhota text taaki bheed mein ek dusre ke upar na chadh jaye
            cv2.putText(frame, f"ID:{track_id}", (x1, y1 - 5), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)

    # --- UI DISPLAY ---
    # Transparent black background for count
    overlay = frame.copy()
    cv2.rectangle(overlay, (10, 10), (350, 70), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    
    cv2.putText(frame, f"TOTAL FISH DETECTED: {len(counted_ids)}", (20, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Extreme Fish Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

print(f"✅ Final Count: {len(counted_ids)}")


