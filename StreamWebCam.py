import cv2
import sys
import API_Class as API

def demo(myAPI):
    myAPI.initializer()
    video_capture = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read() #np.array

        frame = cv2.resize(frame, (320, 240))

        key = cv2.waitKey(100) & 0xFF
        if  key == ord('q'):
            break
        elif key == ord('r'):
            pass
        frame = myAPI.caller(frame)

        # Display the resulting frame
        cv2.imshow('Video', frame)

    # When everything is done, release the capture
    video_capture.release()
    cv2.destroyAllWindows()


# demo(API.openCV())
demo(API.SkyBiometry())
# demo(API.Azure())
