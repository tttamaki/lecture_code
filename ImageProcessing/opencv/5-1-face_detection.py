import cv2
import numpy as np
import sys


def draw_rec(frame, obj):
    for target in obj:
        x, y, w, h = target
        frame = cv2.rectangle(frame,
                              (x, y), (x+w, y+h),
                              (255, 0, 0), 
                              3)
    return frame


def main():

    if len(sys.argv) == 1: # pass the device number
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(int(sys.argv[1]))


    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    face_detector = cv2.CascadeClassifier('data/haarcascade_frontalface_alt.xml')
    eye_detector = cv2.CascadeClassifier('data/haarcascade_eye_tree_eyeglasses.xml')


    detecting = None
    print("key: c (start/stop)")


    while(True):

        ret, frame = cap.read()
        if not ret: continue
        
        h, w, c = frame.shape
        frame = cv2.flip(frame, 1)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break


        if k == ord('c'):
            detecting = not detecting

        if detecting:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_gray = cv2.equalizeHist(frame_gray)

            faces = face_detector.detectMultiScale(frame_gray)
            eyes = eye_detector.detectMultiScale(frame_gray)

            if len(faces) > 0:
                draw_rec(frame, faces)
            if len(eyes) > 0:
                draw_rec(frame, eyes)
            

        cv2.imshow('frame', frame)



    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
