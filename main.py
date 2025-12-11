import cv2
import time 
from src.detector import HandDetector
from src.game import Fruit

def main():
    # Configure webcam
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    WIDTH, HEIGHT = 1280, 720
    cap.set(3, WIDTH) #Width
    cap.set(4, HEIGHT)  #Height

    # Detector
    detector = HandDetector(max_hands=1, detection_con=0.3, track_con=0.5)

    # VARIABLES OF THE GAME
    fruits = []
    last_spawn_time = time.time()
    spawn_interval = 1.0

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
        frame = detector.find_hands(frame, draw=False)
        lm_list = detector.find_position(frame)

        index_x, index_y = None, None

        if len(lm_list) != 0:
            index_x, index_y = lm_list[8][1], lm_list[8][2]
            cv2.circle(frame, (index_x, index_y), 20, (0, 255, 0), cv2.FILLED)

        # Manage fruit spawning
        current_time = time.time()
        if current_time - last_spawn_time > spawn_interval:
            fruits.append(Fruit(screen_width=WIDTH, screen_height=HEIGHT))
            last_spawn_time = current_time

        # Colision logic and fruit updates
        for fruit in fruits[:]: 
            fruit.draw(frame)
            active = fruit.update()
            
            if index_x is not None and index_y is not None:
                if fruit.check_collision(index_x, index_y):

                    print("¡Cut Fruit!") 
                    fruits.remove(fruit) # Erase fruit on collision
                    continue 

            if not active:
                fruits.remove(fruit)
        

        cv2.putText(frame, f'Activate Fruits: {len(fruits)}', (20,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)

        cv2.imshow('AI Fruit Ninja - Dev Mode', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()