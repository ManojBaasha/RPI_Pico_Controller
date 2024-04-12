from picamera2 import Picamera2
import cv2
import time
import numpy as np

# Initialize Picamera2
picam2 = Picamera2()
picam2.start()
time.sleep(1)

# Define the delay between each frame capture
frame_delay = 0.5  # Adjust this value to change the frame rate

def filter_colors(frame):
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for white color in HSV
    lower_white = np.array([0, 0, 200], dtype=np.uint8)
    upper_white = np.array([180, 30, 255], dtype=np.uint8)

    # Define lower and upper bounds for yellow color in HSV
    lower_yellow = np.array([20, 100, 100], dtype=np.uint8)
    upper_yellow = np.array([30, 255, 255], dtype=np.uint8)

    # Create masks
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Combine masks
    mask = cv2.bitwise_or(mask_white, mask_yellow)

    # Apply mask to the original frame
    filtered_frame = cv2.bitwise_and(frame, frame, mask=mask)

    return filtered_frame

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked_img = cv2.bitwise_and(img, mask)
    return masked_img

def draw_lines(img, lines):
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

def filter_lines(lines):
    filtered_lines = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        # Calculate slope
        if x2 - x1 != 0:
            slope = (y2 - y1) / (x2 - x1)
            # Filter lines with slopes between 1 and -1
            if abs(slope) > 1:
                filtered_lines.append(line)
    return filtered_lines

if __name__=='__main__':
    print('Started')
    while True:
        try:
            # Fetching each frame
            array = picam2.capture_array("main")
            frame = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            if frame is None:
                break
            
            # Apply color filtering
            filtered_frame = filter_colors(frame)
            
            # Apply Gaussian blur
            blurred_frame = cv2.GaussianBlur(filtered_frame, (15, 15), 0)
            
            # Apply Canny edge detection
            edges = cv2.Canny(blurred_frame, 50, 150)
            
            # Define vertices for trapezoidal ROI
            height, width = edges.shape
            bottom_left = [width // 9, height]
            top_left = [width // 9, height // 3]
            top_right = [width * 8 // 9, height // 3]
            bottom_right = [width * 8 // 9, height]
            vertices = np.array([[bottom_left, top_left, top_right, bottom_right]], dtype=np.int32)

            # Apply ROI
            roi_edges = region_of_interest(edges, vertices)

            # Detect line segments using HoughLinesP
            lines = cv2.HoughLinesP(roi_edges, 1, np.pi/180, 100, np.array([]), minLineLength=10, maxLineGap=250)

            # Filter lines based on slope
            if lines is not None:
                filtered_lines = filter_lines(lines)
                
                # Overlay filtered lines on one of your images
                lines_image = np.zeros_like(frame)
                draw_lines(lines_image, filtered_lines)
                # Combine the original frame with the lines image
                overlay = cv2.addWeighted(frame, 0.8, lines_image, 1, 0)

                # Display current frame
                cv2.imshow('Current Frame', frame)
                # Display grayscale image after Canny edge detection and region of interest masking
                cv2.imshow('Canny Edges with ROI', roi_edges)
                # Display image with detected line segment drawn on it
                cv2.imshow('Filtered Lines Overlay', overlay)

            keyboard = cv2.waitKey(30)
            if keyboard == 27:
                break
            
            # Introduce delay for frame rate reduction
            time.sleep(frame_delay)
            
        except KeyboardInterrupt:
            break

    # Cleanup
    cv2.destroyAllWindows()
    picam2.close()
    print('Stopped')
