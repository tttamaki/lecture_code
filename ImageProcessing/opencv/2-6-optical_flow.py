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
        ret, frame_pre = cap.read() # wait for 1sec (30fps)
    gray_pre = cv2.cvtColor(frame_pre, cv2.COLOR_BGR2GRAY)


    hsv = np.zeros_like(frame_pre)
    hsv[..., 1] = 255

    while(True):

        ret, frame = cap.read()
        if not ret: continue
        cv2.imshow('frame', frame)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        flow = cv2.calcOpticalFlowFarneback(gray_pre, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        
        magnitude, angle = cv2.cartToPolar(flow[...,0], flow[...,1])
        hsv[..., 0] = np.rad2deg(angle) / 2
        hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
        color_flow = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        cv2.imshow('flow', color_flow)


        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        gray_pre = gray
        frame_pre = frame


    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()