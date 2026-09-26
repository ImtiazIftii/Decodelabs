import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from src.ocr_engine import run_ocr_pipeline
from src.object_detector import load_mobilenet_model,detect_objects


def display_menu():
    print("\n" + "=" * 70)
    print("     THE MACHINE'S OPTIC NERVE")
    print("     Dual-Mode Computer Vision & Perception Engine")
    print("=" * 70)
    print(" Select an execution path:")
    print("   [1] Path 1: Optical Character Recognition (OCR Document Scanner)")
    print("   [2] Path 2: Deep Learning Object Detection (MobileNet-SSD)")
    print("   [q] Exit")
    print("-" * 70)



def main():
    print("Initializing Deep Learning Optic Nerve...")
    net = load_mobilenet_model()
    print("Model weights loaded and ready!\n")

    while True:
        display_menu()
        choice = input("Enter your choice [1 / 2 / q]").strip().lower()

        if choice in ["q","quit","quit"]:
            print("\n👋 Shutting down Optic Nerve.\n")
            break

        #OCR Pipeline    
        elif choice == "1":
            filename = input("\nEnter invoice/document image name (e.g. invoice1.png): ").strip()
            print(f"\nRunning Pre-Processing (Grayscale -> Blur -> Otsu) & Tesseract OCR...")
            try:
                words, avg_conf, dropped = run_ocr_pipeline(filename)
                print("\n" + "=" * 60)
                print(f" 📄 OCR RESULTS FOR: {filename}")
                print("=" * 60)
                print(f" Words Validated (>= 80% Gate): {len(words)}")
                print(f" Low-Confidence Noise Dropped:  {dropped}")
                print(f" Average Validated Accuracy:    {avg_conf:.2f}%")
                print(f" Visual Confirmation Saved:     outputs/boxed{filename}")
                print("-" * 60)
                print(" Extracted Text Sample:")
                print(" " + " ".join(words[:30]) + ("..." if len(words) > 30 else ""))
                print("=" * 60)
            except Exception as e:
                print(f"❌ Error processing OCR: {e}")

        #Object Detection Pipeline
        elif choice == "2":
            filename = input("\nEnter scene photo name (e.g. scene.jpg): ").strip()
            print(f"\n🔄 Building 4D Blob & Running MobileNet-SSD Forward Pass...")
            try:
                objects, avg_conf, dropped = detect_objects(filename, net)
                print("\n" + "=" * 60)
                print(f" 🎯 OBJECT DETECTION RESULTS FOR: {filename}")
                print("=" * 60)
                print(f" Entities Detected (>= 80% Gate): {len(objects)} -> {objects}")
                print(f" Hallucinations / Noise Dropped:  {dropped}")
                print(f" Average Validated Confidence:    {avg_conf:.2f}%")
                print(f" Visual Confirmation Saved:       outputs/detected_{filename}")
                print("=" * 60)
            except Exception as e:
                print(f"❌ Error processing Object Detection: {e}")
        else:
            print("⚠️ Invalid choice. Please enter 1, 2, or q.")
if __name__ == "__main__":
    main()

