from ultralytics import YOLO
import json
import os

directory = "data/seaside_17"

files = os.listdir(directory)

l = []
last_hour = 0
last_minute = 0
for file in files:
    if file.endswith(".ts"):

        file_name = file.split(".")[0]
        time = file_name.split("_")[1]
        hour = int(time[:2])
        minute = int(time[2:4])
        if hour != last_hour:
            last_minute = minute
            last_hour = hour
            l.append(file_name)
        elif minute - last_minute >= 5:
            last_minute = minute
            l.append(file_name)


model = YOLO('yolov8x.pt')

if not os.path.exists("processed"):
    os.mkdir("processed")

for filename in l:
    if not os.path.exists("processed/" + filename + ".json"):
        print("Processing " + filename)
        # Create a yolo model

        # Track with a yolo model on a video
        results = model.track(source="data/seaside_17/" + filename + ".ts",
                              device='0',
                              save=True)

        output = {}

        for count, result in enumerate(results):
            boxes = result.boxes.xyxy.tolist()
            classes = result.boxes.cls.tolist()
            names = result.names
            confidences = result.boxes.conf.tolist()
            output[count] = []
            for box, cls, conf in zip(boxes, classes, confidences):
                x1, y1, x2, y2 = box
                center = ((x1 + x2) / 2, (y1 + y2) / 2T:
                confidence = conf
                detected_class = cls
                name = names[int(cls)]
                output[count].append(
                    {"center": center, "confidence": confidence, "detected_class": detected_class, "name": name})

        json.dump(output, open("processed/" + filename + ".json", "w"), indent=4)

        print("Processed " + filename)
