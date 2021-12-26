import cv2 # opencv-contrib-python(https://pypi.org/project/opencv-contrib-python/)
from matplotlib import pyplot as plt
from lib import image_processing as myProcessing
from lib import line_detection

if __name__ == '__main__':

    # file_name = 'input/line_detection_test.jpg'
    # file_name = 'input/ch1_p1.JPG'
    # test_detect(file_name)

    # file_name = 'input/ch1_p1.JPG'
    # detect_contour(file_name, 130)
    # detect_contour('input/Text/Part1/DSC_0279.JPG', 180)

    # img = cv2.imread('input/Text/Part1/DSC_0279.JPG')
    img = cv2.imread('input/QuestionSound/Part1/DSC_0301.JPG')
    img_white = myProcessing.detect_white_paper(img, threshold=80)
    xmin,xmax,ymin,ymax = myProcessing.find_and_draw_contours(img, img_white)
    print(img_white.shape)
    print(" ".join(str(x) for x in [xmin, xmax,ymin, ymax]))
    img_clip = img[ymin:ymax, xmin:xmax] # [top:bottom, left:right]
    cv2.namedWindow('clip', cv2.WINDOW_NORMAL)
    cv2.imshow('clip', img_clip)
    cv2.waitKey(0)

    # lines, img = line_detection.line_detection(file_name, algorithm=3)
    # print(str(len(lines)))

    # # # for haugh transformation
    # # for line in lines:
    # #     x1, y1, x2, y2 = line[0]

    # #     img = cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 1)

    # cv2.namedWindow("line_detection", cv2.WINDOW_NORMAL)
    # cv2.imshow("line_detection", img)
    # cv2.waitKey(0)
