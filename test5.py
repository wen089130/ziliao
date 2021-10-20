# # created by Huang Lu
# # 27/08/2016 17:05:45
# # Department of EE, Tsinghua Univ.
#
# import cv2
# import numpy as np
#
# cap = cv2.VideoCapture(1)
# cap.set(3, 240)  # width=1920
# cap.set(4, 960)  # height=1080
# while(1):
#     # get a frame
#     ret, frame = cap.read()
#     # show a frame
#     cv2.imshow("capture", frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cap.release()
# cv2.destroyAllWindows()
# import cv2
#
# cap = cv2.VideoCapture(rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp' )
#
#
#
#
# cap.set(3, 1920)  # width=1920
# cap.set(4, 1080)  # height=1080
# # get a frame
# ret, frame = cap.read()
# # show a frame
# cv2.imshow("capture", frame)
# cv2.imwrite("d:\\123.jpeg", frame)
# cv2.waitKey(1000)
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# # user: admin
# # pwd: 12345
# # main: 主码流
# # ip: 192.168.1.64
# # Channels: 实时数据
# # 1： 通道
# cap = cv2.VideoCapture("rtsp://admin:admin123@192.168.1.108:554/cam/realmonitor?channel=2&subtype=0")
# # cap.set(3, 1920)  # width=1920
# # cap.set(4, 1080)  # height=1080
# print (cap.isOpened())
# while cap.isOpened():
#     success,frame = cap.read()
#     cv2.imshow("frame",frame)
#     cv2.waitKey(1)
# coding=utf-8

import sys
import argparse
import cv2
import numpy as np

if __name__ == "__main__":

    image_width = 1920
    image_height = 1080
    rtsp_latency = 200

    uri = "rtsp://192.168.1.108:554/user=admin&password=&channel=1&stream=0.sdp?"
    gst_str = (
        "rtspsrc location={} latency={} ! rtph264depay ! h264parse ! omxh264dec ! nvvidconv ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! videoconvert ! appsink sync=false").format(
        uri, rtsp_latency, image_width, image_height)
    cap = cv2.VideoCapture(gst_str)
    if not cap.isOpened():
        sys.exit("Failed to open camera!")

    # 显示窗口相关设置
    width = 640
    height = 480
    windowName = "CameraDemo"
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, width, height)
    cv2.moveWindow(windowName, 0, 0)
    cv2.setWindowTitle(windowName, "Camera Demo for Jetson TX2/TX1")

    showHelp = True
    showFullScreen = False
    helpText = "'Esc' to Quit, 'H' to Toggle Help, 'F' to Toggle Fullscreen"
    font = cv2.FONT_HERSHEY_PLAIN

    image = ''
    i = 0

    while True:
        if cv2.getWindowProperty(windowName, 0) < 0:  # 检查用户是否关闭窗口
            break;
        ret_val, displayBuf = cap.read();
        if showHelp == True:
            cv2.putText(displayBuf, helpText, (11, 20), font, 1.0, (32, 32, 32), 4, cv2.LINE_AA)
            cv2.putText(displayBuf, helpText, (10, 20), font, 1.0, (240, 240, 240), 1, cv2.LINE_AA)
        # 显示视频内容
        cv2.imshow(windowName, displayBuf)
        key = cv2.waitKey(10)
        # 保存图片
        i += 1
        image = "/home/nvidia/trans/1111/image" + str(i) + ".jpg"
        cv2.imwrite(image, displayBuf)
        # 按钮相关操作：退出/帮助/全屏
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('H') or key == ord('h'):  # toggle help message
            showHelp = not showHelp
        elif key == ord('F') or key == ord('f'):  # toggle fullscreen
            showFullScreen = not showFullScreen
            if showFullScreen == True:
                cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            else:
                cv2.setWindowProperty(windowName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

    cap.release()
    cv2.destroyAllWindows()