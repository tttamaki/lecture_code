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

    cv2.namedWindow('title') # create win with win name
    cv2.createTrackbar('value', # name of value
                       'title', # win name
                       0, # min ：まちがい．これはデフォルト値
                       20, # max
                       myfunc) # callback func

    while(True):

        ret, frame = cap.read()
        if not ret: continue

        v = cv2.getTrackbarPos('value',  # get the value
                               'title')  # of the win

        ## do something by using v
        # print(v)

        cv2.imshow('title', frame)  # show in the win

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()