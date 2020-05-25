import cv2
import numpy as np
import sys

from skimage.feature import corner_harris, corner_peaks, corner_fast, blob_dog, ORB


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

    keys = ['h', 'f', 'o', 'd']
    detectors = ['harris', 'fast', 'ORB', 'DoG']
    detector = ''
    print('key: h (harris), f (fast), o (ORB), d (DoG)')



    while(True):

        ret, frame = cap.read()
        if not ret: continue
        
        h, w, c = frame.shape
        # frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        for i, d in zip(keys, detectors):
            if k == ord(i):
                detector = d
                print('detector:', detector)


        if detector == 'harris':
            coords = corner_peaks(corner_harris(gray, sigma=5), min_distance=1)
            for c in coords:
                cv2.circle(frame, (c[1], c[0]), 10, (0, 0, 255), 2)

        if detector == 'fast':
            coords = corner_peaks(corner_fast(gray), min_distance=1)
            for c in coords:
                cv2.circle(frame, (c[1], c[0]), 10, (0, 0, 255), 2)

        if detector == 'DoG':
            coords = blob_dog(gray, max_sigma=50, threshold=0.2)
            for c in coords:
                cv2.circle(frame, ( int(c[1]), int(c[0]) ), int(c[2]), (0, 0, 255), 2)

        if detector == 'ORB':
            descriptor_extractor = ORB(n_keypoints=100)
            descriptor_extractor.detect(gray)
            keypoints1 = descriptor_extractor.keypoints
            scales1 = descriptor_extractor.scales
            for c, s in zip(keypoints1, scales1):
                cv2.circle(frame, ( int(c[1]), int(c[0]) ), int(s), (0, 0, 255), 2)




        cv2.imshow('frame', frame)



    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
