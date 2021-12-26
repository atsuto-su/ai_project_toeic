import cv2 # opencv-contrib-python(https://pypi.org/project/opencv-contrib-python/)
import numpy as np
from matplotlib import pyplot as plt

def test_detect(file_name):
    img = cv2.imread(file_name) # 画像読み込み
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # グレースケール化
    outLineImage = cv2.bitwise_not(gray)
    outLineImage = cv2.Canny(gray, 220, 250, apertureSize = 3)  
    lines = cv2.HoughLinesP(outLineImage, rho=1, theta=np.pi/180, threshold=100, minLineLength=100, maxLineGap=100)

    print('count of lines: ' + str(len(lines)))

    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2) # 緑色で直線を引く
    cv2.namedWindow("test", cv2.WINDOW_NORMAL)
    cv2.imshow("test", img)
    cv2.waitKey(0)

def detect_contour(file_name, bin_threshold):
    img = cv2.imread(file_name)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret, img_binary = cv2.threshold(img_gray, bin_threshold, 255, cv2.THRESH_BINARY)
    img_binary = cv2.threshold(img_gray, bin_threshold, 255, cv2.THRESH_BINARY)[1]

    # for more detail about morphology: http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    kernel = np.ones((100,100), np.uint8)
    # opening (stress black)
    img_opening = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)
    # closing (stress white)
    img_closing = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours_open, hierarchy = cv2.findContours(img_opening, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours_close, hierarchy = cv2.findContours(img_closing, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # note: can delete strings
    img_contour = cv2.drawContours(img, contours, -1, (0,255,0), 5)
    img_contour_open =  cv2.drawContours(img, contours_open, -1, (0,255,0), 5)
    img_contour_close =  cv2.drawContours(img, contours_close, -1, (0,255,0), 5)


    # fig, axes_tmp = plt.subplots(2, 3, figsize=(20, 12))
    # axes = axes_tmp.ravel()
    # imgs = [img, img_gray, img_binary, img_contour, img_opening, img_closing]
    # for idx, axis in enumerate(axes):
    #     axis.imshow(imgs[idx])
    # plt.show()

    cv2.namedWindow('test', cv2.WINDOW_NORMAL)
    cv2.imshow('test', img_contour)
    cv2.namedWindow('bit', cv2.WINDOW_NORMAL)
    cv2.imshow('bit', img_binary)
    cv2.namedWindow('gray', cv2.WINDOW_NORMAL)
    cv2.imshow('gray', img_gray)
    cv2.namedWindow('opening', cv2.WINDOW_NORMAL)
    cv2.imshow('opening', img_opening)
    cv2.namedWindow('closing', cv2.WINDOW_NORMAL)
    cv2.imshow('closing', img_closing)
    cv2.waitKey(0)

def convert_binary(img, threshold):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_binary = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)[1]

    cv2.namedWindow('bin', cv2.WINDOW_NORMAL)
    cv2.imshow('bin', img_binary)

    return img_binary

def detect_white_paper(img, threshold, kernel_closing=np.ones((10,10), np.uint8), kernel_opening=np.ones((100,100), np.uint8)):

    img_binary = convert_binary(img, threshold)

    # for more detail about morphology: http://labs.eecs.tottori-u.ac.jp/sd/Member/oyamada/OpenCV/html/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    # closing (stress white) to delete contents on the white paper
    img_closing = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, kernel_closing)
    # opening (stress black) to delete 
    img_white = cv2.morphologyEx(img_closing, cv2.MORPH_OPEN, kernel_opening)
    # closing (stress white)

    cv2.namedWindow('white', cv2.WINDOW_NORMAL)
    cv2.imshow('white', img_white)

    return img_white

def find_and_draw_contours(img_ori, img_processed):
    contours = cv2.findContours(img_processed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    contour_max = max(contours, key=lambda x: cv2.contourArea(x))   # lambda [arg]: return
    x0, y0, w, h = cv2.boundingRect(contour_max)
    xmin = x0
    xmax = x0 + w
    ymin = y0
    ymax = y0 + h
    img_contour = cv2.drawContours(img_ori, contours, -1, (0,255,0), 5)

    cv2.namedWindow('contour', cv2.WINDOW_NORMAL)
    cv2.imshow('contour', img_contour)

    return xmin, xmax, ymin, ymax

def image_clip(img, x0, y0, width, height):
    return img[y0 : y0+height, x0 : x0+width]
