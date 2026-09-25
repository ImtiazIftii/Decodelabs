import cv2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

def load_image(filename: str):
    image_path = BASE_DIR/"data"/filename
    img = cv2.imread(str(image_path))

    if img is None:
        print("No image found on the path")
        return None

    return img





#processing the image before feeding to the OCR
def preprocess_image(img,filename):
    grayImg = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #Turning the 3d image into a 2d black and white image
    gauss = cv2.GaussianBlur(grayImg,(5,5),0) #Remove the dust and smoothen out the image 
    #Otsu's Thresholding that forces any image to pick a side either black or white
    #based on a certain cutoff threshold(88 here)
    cutoff,bin_img = cv2.threshold(gauss,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    #saving the binary image to outputs folder
    save_path = OUTPUT_DIR / f"preprocessed_{filename}"
    cv2.imwrite(str(save_path),bin_img)

    return cutoff,bin_img

if __name__ == "__main__":
    for name in ["invoice1.png","invoice2.png"]:
        img = load_image(name)
        cutoff,bin_img = preprocess_image(img,name)
        
        print(img.shape) #gives height,width and channels(colors)
        print(img.size) #gives the number of data points
        print(img[0,0])

