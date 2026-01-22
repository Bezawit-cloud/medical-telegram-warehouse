import os
import csv
from ultralytics import YOLO

# ==============================
# PATHS (adjust only if needed)
# ==============================
IMAGE_DIR = r"C:\Users\bezis\Downloads\medical-telegram-warehouse\data\raw\images"
OUTPUT_CSV = r"C:\Users\bezis\Downloads\medical-telegram-warehouse\data\processed\yolo_detections.csv"

# ==============================
# SAFETY CHECKS
# ==============================
if not os.path.exists(IMAGE_DIR):
    raise FileNotFoundError(f"Image directory not found: {IMAGE_DIR}")

print("Image directory exists:", os.path.exists(IMAGE_DIR))
print("Top-level folders found:", os.listdir(IMAGE_DIR))

# ==============================
# LOAD YOLO MODEL
# ==============================
model = YOLO("yolov8n.pt")

results_data = []

# ==============================
# LOOP THROUGH ALL SUBFOLDERS RECURSIVELY
# ==============================
for root, dirs, files in os.walk(IMAGE_DIR):
    for image_name in files:
        if not image_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        image_path = os.path.join(root, image_name)
        channel_folder = os.path.basename(root)  # parent folder name
        print("Processing image:", image_path)

        # Run YOLO
        results = model(image_path)

        detected_objects = []
        confidence_scores = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                confidence = float(box.conf[0])

                detected_objects.append(label)
                confidence_scores.append(confidence)

        # ==============================
        # IMAGE CLASSIFICATION LOGIC
        # ==============================
        has_person = "person" in detected_objects
        has_product = any(
            obj in detected_objects
            for obj in ["bottle", "cup", "cell phone", "box", "medicine"]
        )

        if has_person and has_product:
            category = "promotional"
        elif has_product and not has_person:
            category = "product_display"
        elif has_person and not has_product:
            category = "lifestyle"
        else:
            category = "other"

        results_data.append({
            "channel_name": channel_folder,
            "image_name": image_name,
            "detected_objects": ",".join(detected_objects),
            "avg_confidence": round(
                sum(confidence_scores) / len(confidence_scores), 3
            ) if confidence_scores else 0,
            "image_category": category
        })

# ==============================
# SAVE RESULTS TO CSV
# ==============================
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "channel_name",
            "image_name",
            "detected_objects",
            "avg_confidence",
            "image_category"
        ]
    )
    writer.writeheader()
    writer.writerows(results_data)

print("\n✅ YOLO detection completed.")
print(f"✅ Total images processed: {len(results_data)}")
print(f"✅ CSV saved to: {OUTPUT_CSV}")

