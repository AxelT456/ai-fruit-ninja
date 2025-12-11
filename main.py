import cv2
from src.detector import HandDetector

def main():
    # Configure webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) #Width
    cap.set(4, 720)  #Height

    # Detector
    detector = HandDetector(max_hands=1)

    if not cap.isOpened():
        print("Error: Could not open video.")
        return
    
    print("Game Init. Press 'q' to quit.")

    while True:
        ret,frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)

        # Detect hands and get landmark positions
        frame = detector.find_hands(frame)
        lm_list = detector.find_position(frame)

        if len(lm_list) != 0:
            x_index, y_index = lm_list[8][1], lm_list[8][2]  # Tip of the index finger
            cv2.circle(frame, (x_index, y_index), 15, (255, 0, 255), cv2.FILLED)

        cv2.imshow('AI Fruit Ninja - Dev Mode', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()