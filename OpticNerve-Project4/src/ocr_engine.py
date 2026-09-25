import pytesseract
import cv2
#pointing to pytesseracts installed location so I dont have to restart
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from preprocessor import load_image,preprocess_image,OUTPUT_DIR


def run_ocr_pipeline(filename:str):
    img = load_image(filename)
    cutoff,bin_img = preprocess_image(img,filename)
    #wordmap gets a dictionary for every word in the png with attributes like their confidence score,height,width etc
    """
    for i in range(len(data["text"])):
    word = data["text"][i]      # Word #i
    conf = data["conf"][i]      # Confidence for Word #i
    x    = data["left"][i]      # X position for Word #i
    y    = data["top"][i]       # Y position for Word #i
    w    = data["width"][i]     # Width for Word #i
    h    = data["height"][i]    # Height for Word #i
    
    """
    wordMap = pytesseract.image_to_data(bin_img,config="--psm 11", output_type=pytesseract.Output.DICT)
    boxed_img = img.copy() #copying the img to draw boxes on it for detecting words
    #bucket for confidence score and valid words
    valid_words = []
    valid_confs = [] 
    dropped_count = 0 #to drop words with confidence below 80%

    for i in range(len(wordMap["text"])):
        word = wordMap["text"][i].strip()
        conf = float(wordMap["conf"][i])

        if not word:
            continue 

        if conf >= 80:
            valid_words.append(word)
            valid_confs.append(conf)

            #grabbing the bounding box coordinates

            x = wordMap["left"][i]
            y = wordMap["top"][i]
            w = wordMap["width"][i]
            h = wordMap["height"][i]

            #Drawing a neon green box with thickness 2
            cv2.rectangle(boxed_img,(x,y),(x+w,y+h),(0,255,0),2)
        else:
            dropped_count += 1

    #Saving the boxed image
    save_path = OUTPUT_DIR / f"boxed{filename}"
    cv2.imwrite(str(save_path),boxed_img)

    #Calculating the average confidence score across all accepted words
    avg_conf = sum(valid_confs)/len(valid_confs) if valid_confs else 0.0

    return valid_words,avg_conf,dropped_count



if __name__ == "__main__":
    for name in ["invoice1.png", "invoice2.png"]:
        words, avg_conf, dropped = run_ocr_pipeline(name)
        print(f"\n================ {name} ================")
        print(f"Words Passed (>=80% Gate): {len(words)}")
        print(f"Noisy Words Dropped (<80%): {dropped}")
        print(f"Average Validated Accuracy: {avg_conf:.2f}%")
        print("Extracted Text Sample:", " ".join(words[:25]))