import cv2
import numpy as np

# アルゴリズム：{ハフ変換、LSD、FastLineDetecor(opencv>=4.1.0)}
ALG_HOUGH = 0
ALG_HOUGH_P = 1
ALG_LSD = 2
ALG_FAST_LINE_DETECTOR = 3

def line_detection(image_file, algorithm=ALG_HOUGH_P) -> list:

    # read an image and convert it into a gray scaled
    img = cv2.imread(image_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bitwise = cv2.bitwise_not(img_gray)
    #gray_bitwise = cv2.Canny(gray, 220, 250, apertureSize = 3)
    img_out = img_bitwise.copy()

    # detect lines by using each algorithm
    if algorithm == ALG_HOUGH:
        # returns combinations of (rho, theta) for all detected lines.
        # an input image must be binalized.
        lines_polar = cv2.HoughLines(img_bitwise, threshold=80)

        lines = []
        for line in lines_polar:
            rho, theta = line[0]
            # a = np.cos(theta)
            # b = np.sin(theta)
            # x0 = a*rho
            # y0 = b*rho
            x1 = int(rho*np.cos(theta) - 1000*np.sin(theta))
            y1 = int(rho*np.sin(theta) + 1000*np.cos(theta))
            x2 = int(rho*np.cos(theta) + 1000*np.sin(theta))
            y2 = int(rho*np.sin(theta) - 1000*np.cos(theta))
            lines.append([x1,y1,x2,y2])

    elif algorithm == ALG_HOUGH_P:
        # maxLineGap is a parameter for doted lines
        lines = cv2.HoughLinesP(img_bitwise, rho=1, theta=np.pi/180, threshold=200, minLineLength=1000, maxLineGap=10)
    elif algorithm == ALG_LSD:
        #lines = lsd(img_bitwise)
        pass
    elif algorithm == ALG_FAST_LINE_DETECTOR:
        length_threshold = 4 # 10
        distance_threshold = 1.41421356
        canny_th1 = 50.0
        canny_th2 = 50.0
        canny_aperture_size = 3
        do_merge = False 
        # fld = cv2.ximgproc.createFastLineDetector(length_threshold, distance_threshold, canny_th1, canny_th2, canny_aperture_size, do_merge)
        fld = cv2.ximgproc.createFastLineDetector()
        lines = fld.detect(img_bitwise)
        img_out = fld.drawSegments(img_bitwise, lines)
    else:
        lines = []

    return lines, img_out


    ''' algorithm:
     - based on the equation: rho = x cos(theta) + y sin(theta), where (rho, theta) is distance and angle of the line from origin respectively.
     - calculation order: "the number of pixels (x,y)" times "resolution of theta"
     - algorithm:
        - for each (x,y), examine a pixel value (usually bilnalized).
        - if the pixel value is 
        - the combination of (rho, theta) which obtained the number of counts over a specified threshold is regarded as lines.
        - (mathmatically, this algorithm achieves calculating a intersection(s) of each curve, rho = x cos(theta) + y sin(theta) for all (x,y)s )

    ref:
    http://www.allisone.co.jp/html/Notes/image/Hough/index.html
    '''
