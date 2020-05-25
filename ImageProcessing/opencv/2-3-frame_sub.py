import numpy as np
import cv2
import sys

def myfunc(i):
    pass # do nothing now


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

    cv2.namedWindow('frame') # create win with win name
    cv2.createTrackbar('th', # name of value
                       'frame', # win name
                       0, # min
                       255, # max
                       myfunc) # callback func

    ret, frame_pre = cap.read()
    frame_pre = cv2.cvtColor(frame_pre, cv2.COLOR_BGR2GRAY)


    while(True):

        ret, frame = cap.read()
        if not ret: continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)


        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        th = cv2.getTrackbarPos('th',  # get the value
                                'frame')  # of the win

        sub = np.abs(frame.astype(np.float) - frame_pre.astype(np.float))
        sub[sub <= th] = 0.
        sub[sub > th] = 1.

        cv2.imshow('sub', sub)

        frame_pre = frame
        

    cap.release()
    cv2.destroyAllWindows()




if __name__ == '__main__':
    main()
