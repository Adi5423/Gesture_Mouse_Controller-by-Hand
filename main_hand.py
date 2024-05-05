import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize the webcam capture
cap = cv2.VideoCapture(0)

# Create a hand detector using MediaPipe
hand_detector = mp.solutions.hands.Hands()

# Create a drawing utility for drawing hand landmarks
drawing_utils = mp.solutions.drawing_utils

# Get the screen width and height using pyautogui
screen_width, screen_height = pyautogui.size()

# Initialize the index finger y-coordinate
index_y = 0

# Initialize the previous time for click detection
prev_time = time.time()

while True:
    # Read a frame from the webcam
    _, frame = cap.read()
    
    # Flip the frame horizontally (since the webcam is mirrored)
    frame = cv2.flip(frame, 1)
    
    # Convert the frame from BGR to RGB (required by MediaPipe)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame using the hand detector
    output = hand_detector.process(rgb_frame)
    
    # Get the detected hand landmarks
    hands = output.multi_hand_landmarks
    
    # Get the frame height and width
    frame_height, frame_width, _ = frame.shape
    
    # If hands are detected
    if hands:
        # Iterate through each hand
        for hand in hands:
            # Draw the hand landmarks on the frame
            drawing_utils.draw_landmarks(frame, hand)
            
            # Get the individual landmarks for the hand
            landmarks = hand.landmark
            
            # Iterate through each landmark
            for id, landmark in enumerate(landmarks):
                # Get the x and y coordinates of the landmark
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                
                # If the landmark is the index finger tip (id=8)
                if id == 8:
                    # Draw a circle on the frame at the index finger tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Calculate the screen coordinates of the index finger tip
                    index_x = screen_width / float(frame_width) * x
                    index_y = screen_height / float(frame_height) * y
                    
                    # Move the mouse cursor to the calculated screen coordinates
                    pyautogui.moveTo(int(index_x), int(index_y))
                
                # If the landmark is the thumb tip (id=4)
                if id == 4:
                    # Draw a circle on the frame at the thumb tip
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    
                    # Calculate the screen coordinates of the thumb tip
                    thumb_x = screen_width / float(frame_width) * x
                    thumb_y = screen_height / float(frame_height) * y
                    
                    # Calculate the distance between the index finger and thumb tips
                    print("outside", abs(index_y - thumb_y))
                    
                    # Get the current time
                    current_time = time.time()
                    
                    # If the distance between the index finger and thumb tips is less than 25 pixels
                    if abs(index_y - thumb_y) < 33:
                        # Perform a mouse click
                        pyautogui.click()
                        pyautogui.sleep(1)
                        
                        # Commented out code for implementing a long press
                        # diff = current_time - prev_time
                        # if diff > 1.5:
                        #     # Holds the mouse button
                        #     pyautogui.click(button='left')
                        #     prev_time = current_time
                        # else:
                        #     # Normal click
                        #     pyautogui.click(button='left')
                        #     pyautogui.sleep(1)
                        #     prev_time = current_time
    
    # Display the frame
    cv2.imshow('Frame', frame)
    
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break