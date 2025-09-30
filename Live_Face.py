# emotion_detector.py

# Required pip installs:
# pip install opencv-python transformers torch Pillow

import cv2
from transformers import pipeline
from PIL import Image
from datetime import datetime

def main():
    """
    Main function to run the live emotion detector with a capture feature.
    """
    # 1. Load the emotion detection model from Hugging Face
    # This uses the image-classification pipeline for ease of use.
    # The model is loaded only once to be efficient.
    print("Loading emotion detection model...")
    try:
        # Using a reliable face emotion detection model for images
        # This model is specifically designed for facial emotion recognition
        classifier = pipeline("image-classification", model="trpakov/vit-face-expression")
        print("Model loaded successfully.")
    except Exception as e:
        print(f"Error loading model: {e}")
        print("Please ensure you have a working internet connection and the required libraries are installed.")
        return

    # 2. Initialize webcam
    # cv2.VideoCapture(0) accesses the default webcam.
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("\nStarting live emotion detection...")
    print("Press 'Spacebar' to capture the current frame and analysis.")
    print("Press 'q' to quit.")

    # 3. Main loop to read frames from the webcam
    while True:
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Convert the OpenCV frame (BGR) to a PIL Image (RGB)
        # The model expects a PIL Image as input.
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Perform emotion prediction on the current frame
        predictions = classifier(pil_image)
        
        # Get the top prediction (highest score)
        top_prediction = predictions[0]
        emotion_label = top_prediction['label']
        emotion_score = top_prediction['score']

        # 4. Overlay the detected emotion and confidence score on the frame
        overlay_text = f"Emotion: {emotion_label} ({emotion_score:.2f})"
        
        # Position the text on the top-left corner of the frame
        cv2.putText(frame, overlay_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

        # Display the resulting frame in a window
        cv2.imshow('Live Emotion Detector', frame)

        # 5. Handle key presses for capture and quit
        key = cv2.waitKey(1) & 0xFF

        # Quit the application if 'q' is pressed
        if key == ord('q'):
            print("Quitting application.")
            break
        
        # Capture feature if 'Spacebar' is pressed
        elif key == ord(' '):
            # --- Capture Logic ---
            
            # a. Generate a unique filename using a timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"capture_{timestamp}.jpg"
            
            # b. Save the current frame as a JPG image
            cv2.imwrite(filename, frame)
            
            # c. Print the detailed emotion analysis to the console
            print(f"📸 CAPTURE: Mood: {emotion_label}, Score: {emotion_score:.2f}")
            print(f"   Image saved as: {filename}\n")

    # 6. Release the webcam and destroy all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
