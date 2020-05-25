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


    print("key: c (start/stop)")


    while(True):

        ret, frame = cap.read()
        if not ret: continue
        
        h, w, c = frame.shape
        # frame = cv2.flip(frame, 1)

        if template is not None:
            ncc = cv2.matchTemplate(frame, template, cv2.TM_CCORR_NORMED)
            _, _, _, top_left = cv2.minMaxLoc(ncc)
            cv2.rectangle(frame, top_left, (top_left[0] + win_size*2,
                                            top_left[1] + win_size*2), (255, 255, 255), 2)
            ncc_visualize = (ncc / ncc.max()) ** 20
            cv2.imshow('NCC score', ncc_visualize / ncc_visualize.max())


        k = cv2.waitKey(1)
        if k == ord('q'):
            break

        if k == ord('c'):
            if template is not None:
                template = None
                cv2.destroyWindow('NCC score')
            else:
                template = frame[h//2 - win_size:h//2 + win_size,
                                 w//2 - win_size:w//2 + win_size].copy()



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
