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


    win_size = 50



    template = None

    detector_dic = {ord('k'): cv2.AKAZE_create(), 
                    ord('o'): cv2.ORB_create()}
    detector = detector_dic[ord('k')]

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    kp1 = des1 = kp2 = des2 = None


    print("k (kaze), o (orb), c (start/stop)")


    while(True):

        ret, frame = cap.read()
        if not ret: continue
        
        h, w, c = frame.shape
        # frame = cv2.flip(frame, 1)

        if template is not None:
            kp2, des2 = detector.detectAndCompute(frame, None)
            matches = bf.match(des1,des2)
            matches = sorted(matches, key = lambda x: x.distance)
            img3 = cv2.drawMatches(template, kp1, frame, kp2, matches[:30], None, flags=0)
            cv2.imshow('frame', img3)

        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        if k in detector_dic.keys():
            detector = detector_dic[k]
            if template is not None:
                kp1, des1 = detector.detectAndCompute(template, None)

        if k == ord('c'):
            if template is not None:
                template = None
            else:
                template = frame[h//2 - win_size:h//2 + win_size, 
                                 w//2 - win_size:w//2 + win_size].copy()
                kp1, des1 = detector.detectAndCompute(template, None)




        if template is None:
            cv2.rectangle(frame, (w//2 - win_size, h//2 - win_size), 
                                 (w//2 + win_size, h//2 + win_size), (0, 255, 0), 2)

        if template is not None:
            frame[0:win_size*2, 0:win_size*2] = template.copy()

        cv2.imshow('frame', frame)



    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
    
