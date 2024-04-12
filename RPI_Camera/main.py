from picamera2 import Picamera2
import cv2
import time
picam2 = Picamera2()
picam2.start()
time.sleep(1)
if __name__=='__main__':
    print('Started')
    while True:
        try:
            # fetching each frame
            array = picam2.capture_array("main")
            frame = cv2.cvtColor(array, cv2.COLOR_RGB2BGR)
            if frame is None:
                break
            cv2.imshow('Frame', frame)
            keyboard = cv2.waitKey(30)
            if keyboard == 27:
                break
        except KeyboardInterrupt:
            break
    # cleanup
    cv2.destroyAllWindows()
    picam2.close()
    print('Stopped')
