import cv2
import numpy as np
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


    while True:

        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame', frame)


        spec = np.fft.fft2(frame)
        spec = np.abs(spec)
        spec = np.fft.fftshift(spec)
        spec = np.log(spec + 1)
        spec /= spec.max()

        cv2.imshow('FFT', spec)


        k = cv2.waitKey(1)
        if k == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()