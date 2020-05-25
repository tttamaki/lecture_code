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


    for i in range(30):
        ret, back = cap.read() # wait for 1sec (30fps)
    back = cv2.cvtColor(back, cv2.COLOR_BGR2GRAY)


    th = 50


    while(True):

        ret, frame = cap.read()
        if not ret: continue

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)


        k = cv2.waitKey(1)
        if k == ord('q'):
            break
        if k == ord('+'):
            th = min(255, th + 1)
            # print(th)
        if k == ord('-'):
            th = max(0, th - 1)
            # print(th)


        sub = np.abs(frame.astype(np.float) - back.astype(np.float))
        sub[sub <= th] = 0
        sub[sub > th] = 1.

        # cv2.putText(sub, str(th), (100, 100), cv2.FONT_HERSHEY_COMPLEX_SMALL, 4, (255,255,255))
        cv2.imshow('sub', sub)

        

    cap.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()