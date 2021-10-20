# from tkinter import *
# import cv2
# from PIL import Image, ImageTk
#
# isrunning = 0
#
# def start():
#     global isrunning
#     if isrunning == 0:
#         global cap
#         cap = cv2.VideoCapture(0)
#         isrunning = 1
#         lmain.grid(row = 1,column = 1)
#         def show_frame():
#             _, frame = cap.read()
#             frame = cv2.flip(frame, 1)
#             frame = cv2.resize(frame, (400,300))
#             cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
#             img = Image.fromarray(cv2image)
#             imgtk = ImageTk.PhotoImage(image=img)
#             lmain.imgtk = imgtk
#             lmain.configure(image=imgtk)
#             if isrunning == 1:
#                 lmain.after(10, show_frame)
#             else:
#                 cap.release()
#     show_frame()
#
# def Stop():
#     global isrunning
#     isrunning = 0
#     lmain.grid_forget()
#
# def main():
#     Stop()
#     #Reset.invoke()
#     #stopFunc.invoke()
#
# root = Tk()
# lmain = Label(root, width = 400, height = 300, bg = "blue")
# stopFunc = Button(root, text = "stop", command = Stop)
# Reset = Button(root, text = "Reset", command = start)
# Main = Button(root, text = "Stop", command = main)
# Start = Button(root, text = "Start", command = start)
# Start.grid(row = 0, column = 0)
# Main.grid(row = 0, column = 1)
#
# root.mainloop()


import threading
import time
import tkinter as tk
from tkinter import ttk


def formatForm(form, width, heigth):
    """设置居中显示"""
    # 得到屏幕宽度
    win_width = form.winfo_screenwidth()
    # 得到屏幕高度
    win_higth = form.winfo_screenheight()

    # 计算偏移量
    width_adjust = (win_width - width) / 2
    higth_adjust = (win_higth - heigth) / 2

    form.geometry("%dx%d+%d+%d" % (width, heigth, width_adjust, higth_adjust))


class LoadingBar(object):

    def __init__(self, width=200):
        # 存储显示窗体
        self.__dialog = None
        # 记录显示标识
        self.__showFlag = True
        # 设置滚动条的宽度
        self.__width = width
        # 设置窗体高度
        self.__heigth = 20

    def show(self, speed=10, sleep=0):
        """显示的时候支持重置滚动条速度和标识判断等待时长"""
        # 防止重复创建多个
        if self.__dialog is not None:
            return

        # 线程内读取标记的等待时长（单位秒）
        self.__sleep = sleep

        # 创建窗体
        self.__dialog = tk.Toplevel()
        self.__dialog.title('系统识别中，请稍后...')
        # 去除边框
        self.__dialog.overrideredirect(-1)
        # 设置置顶
        self.__dialog.wm_attributes("-topmost", True)
        formatForm(self.__dialog, self.__width, self.__heigth)
        # 实际的滚动条控件
        self.bar = ttk.Progressbar(self.__dialog, length=self.__width, mode="indeterminate",
                                   orient=tk.HORIZONTAL)
        self.bar.pack(expand=True)
        # 数值越小，滚动越快
        self.bar.start(speed)
        # 开启新线程保持滚动条显示
        t = threading.Thread(target=self.waitClose)
        t.setDaemon(True)
        t.start()

    def waitClose(self):
        # 控制在线程内等待回调销毁窗体
        while self.__showFlag:
            time.sleep(self.__sleep)

        # 非空情况下销毁
        if self.__dialog is not None:
            self.__dialog.destroy()

        # 重置必要参数
        self.__dialog = None
        self.__showFlag = True

    def close(self):
        # 设置显示标识为不显示
        self.__showFlag = False


loading = LoadingBar()

if __name__ == '__main__':
    root = tk.Tk()
    root.title('Loading滚动条演示')
    formatForm(root, 400, 300)

    # 展示滚动条,指定速度
    loading.show(speed=5)

    tk.Button(root, text='关闭滚动条', command=loading.close).pack(side=tk.TOP)
    tk.Button(root, text='开启滚动条', command=loading.show).pack(side=tk.TOP)

    root.mainloop()