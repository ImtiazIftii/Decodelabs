import cv2
import numpy as numpy
from pathlib import Path
from preprocessor import load_image,OUTPUT_DIR,BASE_DIR

PROTOTXT_PATH = BASE_DIR/"models"/"MobileNetSSD_deploy.prototxt"
MODEL_PATH = BASE_DIR/"models"/"MobileNetSSD_deploy.caffemodel"

#MobileNet-SSD was trained on this dataset ; and can detect these 20 everyday objects and background
#we define them

CLASSES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"
]

def load_mobilenet_model():
    net = cv2.dnn.readNetFromCaffe(str(PROTOTXT_PATH),str(MODEL_PATH))
    return net


def detect_objects(filename,net):
    img = load_image(filename)
    annotated_img = img.copy()
    #We need this to scale the image and keep it between (-1.0-1.0 range) 
    H,W = img.shape[:2] 
    #Reshape, scale, and center the photo into the 4D tensor(creating blob)
    blob = cv2.dnn.blobFromImage(cv2.resize(img,(300,300)),0.007843,(300,300),127.5) #127.5 is the avg of 0-255(color pxl)
    blobOp = net.setInput(blob)
    detections = net.forward()
    dropped_count = 0
    valid_confs = []
    detected_objects = []
    #Deriving the confidence score
    for i in range(detections.shape[2]):
        conf = float(detections[0,0,i,2])
        if(conf >= .80):
            class_id = int(detections[0,0,i,1]) #which class the obj belongs to
            label_name = CLASSES[class_id]
            detected_objects.append(label_name)
            valid_confs.append(conf)
            #Scaling the coordinates
            startX = int(detections[0,0,i,3]*W)
            startY = int(detections[0,0,i,4]*H)
            endX = int(detections[0,0,i,5]*W)
            endY = int(detections[0,0,i,6]*H)

            #Drawing neon box over the object
            box = cv2.rectangle(annotated_img,(startX,startY),(endX,endY),
            (0,255,0),2)

            label_text = f"{label_name}: {conf*100:.1f}%"
            #Stamping the label text above the box
            cv2.putText(annotated_img,label_text,(startX, startY - 10), cv2.FONT_HERSHEY_COMPLEX,0.5,
            (0,255,0),2)
        else:
            dropped_count +=1    

        # Save the Visual Confirmation image (Gatekeeper #4)

    avg_conf = (sum(valid_confs)/len(valid_confs)) * 100  if len(valid_confs) > 0  else 0.0   
    save_path = OUTPUT_DIR / f"detected_{filename}"
    cv2.imwrite(str(save_path), annotated_img)
    return detected_objects, avg_conf, dropped_count


if __name__ == "__main__":
    net = load_mobilenet_model()
    objects, avg_conf, dropped = detect_objects("dog.jpg", net)

    print("\n================ OBJECT DETECTION REPORT ================")
    print(f"Objects Detected (>= 80% Gate): {len(objects)} -> {objects}")
    print(f"Low-Confidence Guesses Dropped: {dropped}")
    print(f"Average Validated Confidence:   {avg_conf:.2f}%\n")