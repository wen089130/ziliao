#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

import kongzhi

sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
from aip import AipOcr
import queue,progressbar
from kongzhi import *
import fenci
import time, threading
from ctypes import windll
import cv2
# on Windows Server and early Windows this setting will fail
windll.shcore.SetProcessDpiAwareness(2)
if sys.version_info[0] == 2:
    # from Tkinter import *
    # from tkFont import Font
    # from ttk import *
    # # Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    # from tkMessageBox import *
    # # Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    # # import tkFileDialog
    # # import tkSimpleDialog
    pass

else:  # Python 3.x
    from tkinter import *
    from tkinter.font import Font
    from tkinter.ttk import *
    # import tkinter.filedialog as tkFileDialog
    # import tkinter.simpledialog as tkSimpleDialog    #askstring()

from PIL import Image, ImageTk
# from main import Application

class Application_ui(Frame):
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。

    name=''
    pz=False

    def __init__(self, master=None):

        self.notify_queue = queue.Queue()
        self.gress_bar = progressbar.GressBar()
        self.fenci = fenci.fenci
        Frame.__init__(self, master)
        self.master.title('智能资料机器人_V1.0')
        # To center the window on the screen.
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()

        x = (ws / 2) - (987 / 2)
        y = (hs / 2) - (655 / 2)
        self.master.geometry('%dx%d+%d+%d' % (987, 655, x, y))
        self.process_msg()
        self.createWidgets()

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.style.configure('TFrame1.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame1.TLabelframe.Label', font=('宋体', 9))
        self.Frame1 = LabelFrame(self.top, text='表格样式', style='TFrame1.TLabelframe')
        self.Frame1.place(relx=0.016, rely=0.024, relwidth=0.495, relheight=0.515)

        self.style.configure('TFrame3.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame3.TLabelframe.Label', font=('宋体', 9))
        self.Frame3 = LabelFrame(self.top, text='状态区', style='TFrame3.TLabelframe')
        self.Frame3.place(relx=0.016, rely=0.574, relwidth=0.966, relheight=0.392)

        self.style.configure('TFrame2.TLabelframe', font=('宋体', 9))
        self.style.configure('TFrame2.TLabelframe.Label', font=('宋体', 9))
        self.Frame2 = LabelFrame(self.top, text='签字内容', style='TFrame2.TLabelframe')
        self.Frame2.place(relx=0.543, rely=0.024, relwidth=0.439, relheight=0.515)

        self.Command4Var = StringVar(value='重置')
        self.style.configure('TCommand4.TButton', font=('宋体', 9))
        self.Command4 = Button(self.Frame3, text='重置', textvariable=self.Command4Var, command=self.Command4_Cmd,
                               style='TCommand4.TButton')
        self.Command4.setText = lambda x: self.Command4Var.set(x)
        self.Command4.text = lambda: self.Command4Var.get()
        self.Command4.place(relx=0.613, rely=0.498, relwidth=0.068, relheight=0.097)

        self.Command3Var = StringVar(value='测试')
        self.style.configure('TCommand3.TButton', font=('宋体', 9))
        self.Command3 = Button(self.Frame3, text='测试', textvariable=self.Command3Var, command=self.Command3_Cmd,
                               style='TCommand3.TButton')
        self.Command3.setText = lambda x: self.Command3Var.set(x)
        self.Command3.text = lambda: self.Command3Var.get()
        self.Command3.place(relx=0.722, rely=0.28, relwidth=0.06, relheight=0.097)

        self.Command2Var = StringVar(value='初始化')
        self.style.configure('TCommand2.TButton', font=('宋体', 9))
        self.Command2 = Button(self.Frame3, text='初始化', textvariable=self.Command2Var, command=self.Command2_Cmd,
                               style='TCommand2.TButton')
        self.Command2.setText = lambda x: self.Command2Var.set(x)
        self.Command2.text = lambda: self.Command2Var.get()
        self.Command2.place(relx=0.613, rely=0.28, relwidth=0.068, relheight=0.097)

        self.Command1Var = StringVar(value='停止')
        self.style.configure('TCommand1.TButton', font=('宋体', 9))
        self.Command1 = Button(self.Frame3, text='停止', textvariable=self.Command1Var, command=self.Command1_Cmd,
                               style='TCommand1.TButton')
        self.Command1.setText = lambda x: self.Command1Var.set(x)
        self.Command1.text = lambda: self.Command1Var.get()
        self.Command1.place(relx=0.831, rely=0.28, relwidth=0.068, relheight=0.097)

        self.Text1Font = Font(font=('宋体', 9))
        self.Text1 = Text(self.Frame3, font=self.Text1Font)

        self.Text1.place(relx=0.008, rely=0.28, relwidth=0.505, relheight=0.689)
        self.Text1.insert('1.0', '')

        self.Label2Var = StringVar(value='管片0021-0030环模具报审、报验表')
        self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体', 9, 'bold'))
        self.Label2 = Label(self.Frame3, text='管片0021-0030环模具报审、报验表', textvariable=self.Label2Var,
                            style='TLabel2.TLabel')
        self.Label2.setText = lambda x: self.Label2Var.set(x)
        self.Label2.text = lambda: self.Label2Var.get()
        self.Label2.place(relx=0.101, rely=0.125, relwidth=0.412, relheight=0.066)

        self.Label1Var = StringVar(value='当前表格标题：')
        self.style.configure('TLabel1.TLabel', anchor='w', font=('宋体', 9))
        self.Label1 = Label(self.Frame3, text='当前表格标题：', textvariable=self.Label1Var, style='TLabel1.TLabel')
        self.Label1.setText = lambda x: self.Label1Var.set(x)
        self.Label1.text = lambda: self.Label1Var.get()
        self.Label1.place(relx=0.008, rely=0.125, relwidth=0.102, relheight=0.066)

        # self.Picture1 = Canvas(self.Frame1, takefocus=1)
        # self.Picture1.place(relx=0.016, rely=0.047, relwidth=0.951, relheight=0.905)
        self.labelPic = Label(self.Frame1,takefocus=1, text="realimage", font=("Arial", 14))
        self.labelPic.place(relx=0.016, rely=0.047, relwidth=0.951, relheight=0.905)
        self.labelPic1 = Label(self.Frame2, takefocus=1, text="realimage", font=("Arial", 14))
        self.labelPic1.place(relx=0.018, rely=0.047, relwidth=0.945, relheight=0.905)
        # self.Picture2 = Canvas(self.Frame2, takefocus=1)
        # self.Picture2.place(relx=0.018, rely=0.047, relwidth=0.945, relheight=0.905)
        self.Command5Var = StringVar(value='摄像头校准')
        self.style.configure('TCommand5.TButton', font=('宋体', 9))
        self.Command5 = Button(self.Frame3, text='摄像头校准', textvariable=self.Command5Var, command=self.Command5_Cmd,
                               style='TCommand5.TButton')
        self.Command5.setText = lambda x: self.Command5Var.set(x)
        self.Command5.text = lambda: self.Command5Var.get()
        self.Command5.place(relx=0.722, rely=0.498, relwidth=0.06, relheight=0.097)

        self.Command6Var = StringVar(value='自动')
        self.style.configure('TCommand6.TButton', font=('宋体', 9))
        self.Command6 = Button(self.Frame3, text='自动', textvariable=self.Command6Var, command=self.Command6_Cmd,
                               style='TCommand6.TButton')
        self.Command6.setText = lambda x: self.Command6Var.set(x)
        self.Command6.text = lambda: self.Command6Var.get()
        self.Command6.place(relx=0.831, rely=0.498, relwidth=0.068, relheight=0.097)

        self.Command7Var = StringVar(value='复制标题')
        self.style.configure('TCommand7.TButton', font=('宋体', 9))
        self.Command7 = Button(self.Frame3, text='复制标题', textvariable=self.Command7Var, command=self.Command7_Cmd,
                               style='TCommand7.TButton')
        self.Command7.setText = lambda x: self.Command7Var.set(x)
        self.Command7.text = lambda: self.Command7Var.get()
        self.Command7.place(relx=0.613, rely=0.716, relwidth=0.068, relheight=0.097)

    # pb = ttk.Progressbar(self.Frame3, length=400, value=0, mode="indeterminate")
        # pb.place(relx=0.613, rely=0.716, relwidth=0.295, relheight=0.097)
        # pb.start()
    def fanhui(self,cname):
        global name
        name=cname
        print(name)
        self.pz=TRUE
        # kongzhi.kongzhi.huanzhi(self,name)
        # print(name)
    def fanhuipz(self,name):
        # self.name=name
        self.pz=False
    def updateui(self):
        self.im_orig = cv2.imread('123.png')

        self.xmin_orig = 8
        self.ymin_orig = 12
        self.xmax_orig = 352
        self.ymax_orig = 498



        cv2.rectangle(
            self.im_orig,
            pt1=(self.xmin_orig, self.ymin_orig),
            pt2=(self.xmax_orig, self.ymax_orig),
            color=(0, 255, 0),
            thickness=2
        )

        def changeSize(self, event):
            im = cv2.resize(self.im_orig, (event.winfo_width(), event.winfo_height()))

            tkim = ImageTk.PhotoImage(Image.fromarray(im))
            self.labelPic1['image'] = tkim
            self.labelPic1.image = tkim
        self.im_orig = self.im_orig[:, :, ::-1]  # bgr => rgb   necessary

        # tkim = ImageTk.PhotoImage(Image.fromarray(self.im_orig))
        # self.labelPic1['image'] = tkim
        # self.labelPic1.image = tkim

        self.labelPic1.bind('<Configure>', changeSize(self,self.Frame2))
        self.labelPic1.pack()
    def updateui1(self):
        self.im_orig = cv2.imread('mb.jpg')
        self.labelPic = Label(self.Frame1, takefocus=1, text="realimage", font=("Arial", 14))
        self.labelPic.place(relx=0.016, rely=0.047, relwidth=0.951, relheight=0.905)
        self.xmin_orig = 8
        self.ymin_orig = 12
        self.xmax_orig = 352
        self.ymax_orig = 498

        cv2.rectangle(
            self.im_orig,
            pt1=(self.xmin_orig, self.ymin_orig),
            pt2=(self.xmax_orig, self.ymax_orig),
            color=(0, 255, 0),
            thickness=2
        )

        def changeSize(self, event):
            im = cv2.resize(self.im_orig, (event.winfo_width(), event.winfo_height()))

            tkim = ImageTk.PhotoImage(Image.fromarray(im))
            self.labelPic['image'] = tkim
            self.labelPic.image = tkim
        self.im_orig = self.im_orig[:, :, ::-1]  # bgr => rgb   necessary

        # tkim = ImageTk.PhotoImage(Image.fromarray(self.im_orig))
        # self.labelPic1['image'] = tkim
        # self.labelPic1.image = tkim

        self.labelPic.bind('<Configure>', changeSize(self,self.Frame2))
        self.labelPic.pack()

    def process_msg(self):
        self.master.after(400, self.process_msg)
        while not self.notify_queue.empty():
            try:
                msg = self.notify_queue.get()
                if msg[0] == 1:
                    self.gress_bar.quit()

            except queue.Empty:
                pass


class Application(Application_ui):
    videoThreadRun = False
    labelPicWidth = 1900
    ceshi=False

    labelPicHeight = 1900

    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)


    # 测试
    def Command3_Cmd(self, event=None):

        # kongzhi.paizhaoshibie(self)
        # time.sleep(1)
        # while TRUE:
        #     print(self.pz)
        # if self.pz == True:
        #     kongzhi.xunzhao(self, self.name)


        #换纸
        # kongzhi.huanzhi(self)
        # 找表格并点击
        # print('11111111111111111111111')
        # print(Application_ui.name)
        if Application_ui.name=='':
            kongzhi.paizhaoshibie(self)
        else:
            print(Application_ui.name)
            kongzhi.xunzhao(self,name)
        #执行书写任务
        # kongzhi.shuxie(self)


        # aa=self.fenci.tfidf(self)
        # print(aa)
        # for i in range(0, len(aa)):
        #    if aa[i].endswith('报审'):
        #         print(aa[i])
        #    if aa[i].endswith('构配件'):
        #         print(aa[i])




        # TODO, Please finish the function here!
        # self.Text1.delete(0.0, END)
        # self.Label2Var = StringVar(value='管片')
        # self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体', 9, 'bold'))
        # self.Label2 = Label(self.Frame3, text='管片', textvariable=self.Label2Var,
        #                     style='TLabel2.TLabel')
        # self.Label2.setText = lambda x: self.Label2Var.set(x)
        # self.Label2.text = lambda: self.Label2Var.get()
        # self.Label2.place(relx=0.101, rely=0.125, relwidth=0.412, relheight=0.066)
        # text = StringVar()
        # text.set('old')
        # self.Label2.setText = lambda x: text.set(x)
        # self.Label2.pack()
        # kongzhi.diaoyong(self,'工程名称:长沙市轨道交通6号线长庆站-和馨园站区间盾构工程报审、报验表')

    # 初始化机器人
    def Command2_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.write_log_to_Text("设备初始化成功，准备开始工作11111111111111")
        # self.updateui1()

        kongzhi.qidong(self)






    # 手动控制
    def Command6_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.write_log_to_Text("开始分析表格内容。。。")
        self.updateui1()
        def ocr(_queue):

            self.write_log_to_Text("开始拍照")
            # self.gress_bar.quit()
            APP_ID = '24933039'
            API_KEY = 'AAVqjiTKU7elSmEM6RwRp2hZ'
            SECRET_KEY = 'sVUzwhAgxn7VnjQrfFKgSMYPBSb9ypUF'
            client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            # cap = cv2.VideoCapture(1)
            # cap.set(3, 1920)  # width=1920
            # cap.set(4, 1080)  # height=1080
            # ret, frame = cap.read()
            # # cv2.imshow('video', frame)
            # cv2.imwrite('mb.jpg', frame)
            def get_file_content(filePath):
                with open(filePath, 'rb') as fp:
                    return fp.read()
            image = get_file_content('mb.jpg')
            options = {}
            options["language_type"] = "CHN_ENG"
            options["detect_direction"] = "true"
            options["detect_language"] = "true"
            options["probability"] = "false"
            result = client.basicGeneral(image, options)
            print(result['words_result'])
            self.write_log_to_Text(result['words_result'])

            for i in range(0, len(result['words_result'])):
                if result['words_result'][i]['words'].endswith('报验表'):
                    b = str(result['words_result'][i]['words'])
                if result['words_result'][i]['words'].startswith('工程名称'):
                    a = str(result['words_result'][i]['words'])
                else:
                    self.gress_bar.quit()
                    # self.write_log_to_Text('表格无法识别，请手动选取模板')

            cname = a + b
            print(cname)
            # self.Text1.delete(0.0, END)
            self.Label2Var = StringVar(value=cname)
            self.style.configure('TLabel2.TLabel', anchor='w', font=('宋体', 9, 'bold'))
            self.Label2 = Label(self.Frame3, text=cname, textvariable=self.Label2Var,
                                style='TLabel2.TLabel')
            self.Label2.setText = lambda x: self.Label2Var.set(x)
            self.Label2.text = lambda: self.Label2Var.get()
            self.Label2.place(relx=0.101, rely=0.125, relwidth=0.412, relheight=0.066)
            # kongzhi.diaoyong(self, '工程名称:长沙市轨道交通6号线长庆站-和馨园站区间盾构工程报审、报验表')
            self.write_log_to_Text('成功识别出表格标题  '+cname)
            # self.write_log_to_Text(cname)
            kongzhi.diaoyong(self, cname)
            self.write_log_to_Text('--------------------------------')

            _queue.put((1,))
            self.gress_bar.quit()


        th = threading.Thread(target=ocr, args=(self.notify_queue,))
        th.setDaemon(True)

        th.start()
        self.gress_bar.start()


    # 复制模板标题至剪贴板
    def Command7_Cmd(self, event=None):
        # print(type(self.main_spec.window(title=r'定位测试', control_type="Button").isEnabled))
        # self.waitzx()
        print(self.name)
        kongzhi.xunzhao(self, self.name)

    def waitzx(self):
        self.main_spec.window(title=r'进纸', control_type="Button").click()
        # self.main_spec.window(title=r'进纸', control_type="Button").(isenabled)
        time.sleep(10)
        self.main_spec.window(title=r'🚩 开始', control_type="Button").click()
        aa1 = self.main_spec.child_window(auto_id='MainWindow.centralWidget.frame_2.progressBar')
        num1=aa1.legacy_properties()['Value']
        time.sleep(1)
        num2=aa1.legacy_properties()['Value']
        print(num1)
        print(num2)
        def gongzuo(_queue):
            while 1:
                num1 = aa1.legacy_properties()['Value']
                time.sleep(2)
                num2 = aa1.legacy_properties()['Value']
                if num1==num2:
                    break
            self.gress_bar.quit()
            # tkinter.messagebox.showinfo('提示', '系统正在进行表格内容识别，请稍后')
            self.main_spec.window(title=r'出纸', control_type="Button").click()
            time.sleep(10)
            _queue.put((1,))

        th = threading.Thread(target=gongzuo, args=(self.notify_queue,))
        th.setDaemon(True)
        th.start()
        # 启动进度条
        self.gress_bar.start()


    # 摄像头校准
    def Command5_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.write_log_to_Text("测试按钮点击成功")
        cap = cv2.VideoCapture('aa.mp4')
        cap = cv2.VideoCapture(0)

        cap.set(3, 1920)  # width=1920
        cap.set(4, 1080)  # height=1080
        while (True):
            # 获取一帧
            # 第1个参数ret(return value缩写)是一个布尔值，表示当前这一帧是否获取正确
            ret, frame = cap.read()
            # 将这帧转换为灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2RGBA)

            cv2.imshow('frame', gray)
            if cv2.waitKey(1) == ord('q'):
                break

    # 停止资料绘制
    def Command1_Cmd(self, event=None):
        # TODO, Please finish the function here!
        # 说明图片位置，并导入图片到画布上
        self.write_log_to_Text("设备停止工作")
        kongzhi.tuichu(self)
        # im1 = None
        # im2 = None
        # im1 = Image.open("pic.gif")  # 支持相对或绝对路径，支持多种格式
        # im2 = ImageTk.PhotoImage(im1)
        # self.pilImage = Image.open("aa.png")
        # im2 = ImageTk.PhotoImage(image=self.pilImage)
        # self.Picture1.create_image(10, 10, anchor=NW, image=im2)

    # 重置状态栏
    def Command4_Cmd(self, event=None):
        # TODO, Please finish the function here!
        self.Text1.delete(0.0, 'end')
        # self.labelPic.destroy()
        self.updateui1()
        # self.loadVideo()

    # 写日志到状态区
    def write_log_to_Text(self, logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) + " " + str(logmsg) + "\n"  # 换行
        # if LOG_LINE_NUM <= 7:
        #     self.Text1.insert(END, logmsg_in)
        #     LOG_LINE_NUM = LOG_LINE_NUM + 1
        # else:
        # self.Text1.delete(0.0,'end')
        self.Text1.insert(END, logmsg_in)
        self.Text1.see("end")
        # self.Text1.configure(state=tkinter.DISABLED)

    # 获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        return current_time






if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
