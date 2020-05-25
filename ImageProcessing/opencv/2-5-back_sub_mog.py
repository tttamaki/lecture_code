import numpy as np
import cv2
import sys


def main():

    if len(sys.argv) == 1: # pass the device number
        cap = cv2.VideoCapture(0)
    else:
        try:
            cap = cv2.VideoCapture(int(sys.argv[1]))
        except:
            cap = cv2.VideoCapture(sys.argv[1])


    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


    fgbg = cv2.createBackgroundSubtractorMOG2()
    # fgbg = cv2.createBackgroundSubtractorMOG2(history=500,
    #                      varThreshold=16, detectShadows=True)


    while(True):

        ret, frame = cap.read()
        if not ret: continue

        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break


        sub = fgbg.apply(frame)

        cv2.imshow('sub', sub)

        

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()