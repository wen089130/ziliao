import sys
import win32api
import win32gui
import win32ui
from tkinter import Frame
import os
# set coinit_flags (there will be a warning message printed in console by pywinauto, you may ignore that)
sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
import psutil
from pywinauto.application import Application as application1
from pywinauto import mouse
from PIL import ImageGrab
from PIL import Image
import main
import tkinter
import win32con
import win32clipboard as w
import pygame
import fuzzywuzzy.fuzz
from ctypes import windll
import cv2
from aip import AipOcr
import time, threading
windll.shcore.SetProcessDpiAwareness(2)
class kongzhi():
    # 这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    # 这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('智能资料机器人_V1.0')
        # To center the window on the screen.
        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        x = (ws / 2) - (987 / 2)
        y = (hs / 2) - (655 / 2)

        self.createWidgets()

    def qidong(self):


        a = False
        for pid in psutil.pids():
            p = psutil.Process(pid)
            if p.name() == "LTCv2.exe":
                a = True
        if a == True:
            app = application1(backend="uia").connect(title='LT Center')
            self.main_spec = app.window(title=r'LT Center')  # 定位窗口
            self.main_spec.wait("exists ready", timeout=5, retry_interval=3)  # 等到窗口真的开着
        else:
            app = application1(backend="uia").start("C:\Program Files (x86)\LichTech\LT Center\LTCv2.exe")  # 启动程序
            log_spec = app.window(title='20211017 - Login')  # 定位窗口
            log_spec.wait("exists ready", timeout=5, retry_interval=3)  # 等到窗口真的开着
            # time.sleep(1)
            log_spec.window(title=r'登陆', control_type="Button").click()  # 点击Button控件，进入登录界面
            self.main_spec = app.window(title=r'LT Center')  # 定位窗口
            self.main_spec.wait("exists ready", timeout=5, retry_interval=3)  # 等到窗口真的开着


    # 点击listitem内容
    def __get_element_postion(element):
        """获取元素的中心点位置"""
        # 元素坐标
        element_position = element.rectangle()
        # 算出中心点位置
        center_position = (int((element_position.left + element_position.right) / 2),
                           int((element_position.top + element_position.bottom) / 2))
        return center_position

    def diaoyong(self, name=None):
        # 点击进入任务队列选项卡

        self.main_spec.set_focus()
        # time.sleep(1)
        self.main_spec.window(title=r'任务队列', control_type="TabItem").invoke()  # 点击选项卡，点击(uia mode)
        # time.sleep(1)
        # 3、点击listitem内容
        dlg_main = self.main_spec.ListItem
        print(dlg_main.items)
        item = dlg_main.ListItem
        #
        # for item in dlg_main.items():
        #     print('调用')
        #     try:
        #         if item.text()=='报审表':
        #             item.select()
        #     except Exception:
        #         pass
        file_helper_element = self.main_spec.window(title=name, control_type="ListItem")  # 点击Button控件，进入登录界面
        def bofang(name):
            file = name  # 文件名是完整路径名
            pygame.mixer.init()  # 初始化音频
            track = pygame.mixer.music.load(file)  # 载入音乐文件
            pygame.mixer.music.play()  # 开始播放
            time.sleep(1)  # 播放10秒
            pygame.mixer.music.stop()  # 停止播放
        if file_helper_element.exists():
            bofang('sucess.mp3')
            mouse.click(button='left', coords=kongzhi.__get_element_postion(file_helper_element))
            time.sleep(1)
            aa1 = self.main_spec.child_window(auto_id='MainWindow.centralWidget.widgetShowXY')
            # print(GetControlCoord.get_coord(self,aa1))
            # kongzhi.capture_image((10, 929, 122, 1070),'default.png')
            a = self.main_spec.capture_as_image().save('123.png')
            main.Application.write_log_to_Text(self,'成功检测到表格签字文件，开始书写任务')


            main.Application_ui.updateui(self)
            # 开始写字
            self.main_spec.set_focus()
            main.Application.waitzx(self)
            # self.main_spec.window(title=r'🚩 开始', control_type="Button").click()  # 点击选项卡，点击(uia mode)
        else:
            main.Application.write_log_to_Text(self,'未检测到表格签字文件，请按提示操作')
            bofang('error.mp3')
            aa='当前表格名称为  '+name+'  。系统未检测到此标题的模板。请先于存储库中定义此标题的模板,然点击”确定“以复制表格名称至剪贴板'
            # tkinter.messagebox.showinfo('提示', aa)
            Q = tkinter.messagebox.askokcancel(title='提示', message=aa)  # resurn 'True' or 'False'
            if Q==True:
                w.OpenClipboard()
                w.SetClipboardData(win32con.CF_UNICODETEXT, name)
                w.CloseClipboard()
            # main.Application.Command3_Cmd(self)
            print('模板不存在')
        # print(dir(file_helper_element))

    #开始执行书写流程
    def shuxie(self):

        def gongzuo(_queue):
            main.Application.write_log_to_Text(self,"写字机正在工作中，请稍后")
            self.main_spec.window(title=r'🚩 开始', control_type="Button").click()
            time.sleep(1)
            self.main_spec.window(title=r'🚩 开始', control_type="Button").wait('visible', 100)
            main.Application.write_log_to_Text(self,'写字机已完成工作  ')
            # self.write_log_to_Text(cname)
            # kongzhi.diaoyong(self, cname)
            self.write_log_to_Text('--------------------------------')
            kongzhi.paizhaoshibie(self)
            _queue.put((2,))
            
            # self.gress_bar.quit()
        th = threading.Thread(target=gongzuo, args=(self.notify_queue,))
        th.setDaemon(True)
        th.start()
        # self.gress_bar.start()

    # 拍照并设别表格标题，核心算法
    def paizhaoshibie(self):
        # TODO, Please finish the function here!
        # self.write_log_to_Text("开始分析表格内容。。。")
        # self.updateui1()
        # global a=[,]

        def ocr(_queue, ):
            main.Application.write_log_to_Text(self,"开始拍照")
            # self.gress_bar.quit()
            APP_ID = '24933039'
            API_KEY = 'AAVqjiTKU7elSmEM6RwRp2hZ'
            SECRET_KEY = 'sVUzwhAgxn7VnjQrfFKgSMYPBSb9ypUF'
            client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
            cap = cv2.VideoCapture(0)
            cap.set(3, 1920)  # width=1920
            cap.set(4, 1080)  # height=1080
            ret, frame = cap.read()
            cv2.imwrite('mb.jpg', frame)
            main.Application_ui.updateui1(self)
            main.Application.write_log_to_Text(self,"拍照成功，开始识别表格内容")
            def get_file_content(filePath):
                with open(filePath, 'rb') as fp:
                    return fp.read()
            image = get_file_content('mb.jpg')
            options = {}
            options["language_type"] = "CHN_ENG"
            options["detect_direction"] = "true"
            options["detect_language"] = "true"
            options["probability"] = "false"

            try:
                result = client.basicGeneral(image, options)
            except:
                main.Application.write_log_to_Text(self, '第一次识别表格失败，开始第二次识别')

                # logdebug('requests failed one time')
                try:
                    result = client.basicGeneral(image, options)
                except:
                    # logdebug('requests failed two time')
                    main.Application.write_log_to_Text(self, '多次识别均失败，请检查您的网络情况')
            print(result['words_result'])
            self.write_log_to_Text(result['words_result'])
            global cname
            cname=''

            for i in range(0, len(result['words_result'])):
                if result['words_result'][i]['words'].startswith('报审、报验表'):
                    cname = '钢筋报审、报验表'

                    # # print(result['words_result'][i-1]['words'])
                    # if result['words_result'][i-1]['words'].startswith('模具'):
                    #     cname = '模具报审、报验表'
                    # if result['words_result'][i-1]['words'].startswith('钢筋'):
                    #     cname = '钢筋报审、报验表'
                    # if result['words_result'][i-1]['words'].startswith('混凝土'):
                    #     cname = '混凝土报审、报验表'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '钢筋加工检验批质量验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('钢筋加工检验批'):
                    cname='钢筋加工检验批质量验收记录'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '钢筋安装检验批质量验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('钢筋安装检验批'):
                    cname='钢筋安装检验批质量验收记录'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '钢筋原材料检验批质量验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('钢筋原材料检验批'):
                    cname='钢筋原材料检验批质量验收记录'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '混凝土浇灌令') > 95:
                # if result['words_result'][i]['words'].startswith('混凝土浇灌令'):
                    cname='混凝土浇灌令'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '埋设件检验批质量验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('埋设件检验批'):
                    cname='埋设件检验批质量验收记录'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '建筑结构隐蔽工程验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('建筑结构隐蔽'):
                    cname='建筑结构隐蔽工程验收记录'
                if  fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '防水混凝土检验批质量验收记录表')>95:
                    cname = '防水混凝土检验批质量验收记录'
                # if result['words_result'][i]['words'].startswith('防水混凝土检验批'):
                #     print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
                #     print(fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '防水混凝土检验批质量验收记录表表'))
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '模板安装检验批质量验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('模板安装检验批'):
                    cname='模板安装检验批质量验收记录'
                if fuzzywuzzy.fuzz.ratio(result['words_result'][i]['words'], '管片外观尺寸偏差检验批质量验收记录') > 95:
                # if result['words_result'][i]['words'].startswith('管片外观尺寸偏差检验批'):
                    cname='管片外观尺寸偏差检验批质量验收记录'

            main.Application.write_log_to_Text(self,'成功识别出表格标题  ' + cname)


            path = 'mb.jpg'  # 文件路径
            if os.path.exists(path):  # 如果文件存在
                # 删除文件，可使用以下两种方法。
                os.remove(path)

            main.Application_ui.fanhui(self,cname)
            # self.xunzhao(self,'aaaa')
            # self.xunzhao(cname)


            # print(a)

            # self.write_log_to_Text(cname)
            # kongzhi.diaoyong(self, cname)
            self.write_log_to_Text('--------------------------------')
            _queue.put((1,))
            self.gress_bar.quit()

        th = threading.Thread(target=ocr, args=(self.notify_queue,))
        th.setDaemon(True)
        th.start()
        self.gress_bar.start()


    #书写完毕出纸，并加载准备开始书写的纸张
    def huanzhi(self,name):
        self.main_spec.window(title=r'出纸', control_type="Button").click()
        time.sleep(1)
        self.main_spec.window(auto_id='MainWindow.centralWidget.frame.groupBox_7.cmdout', control_type="Button").wait('enabled',100)
        # time.sleep(6)
        self.main_spec.window(title=r'进纸', control_type="Button").click()
        time.sleep(10)
        # self.main_spec.window(auto_id='MainWindow.centralWidget.frame.groupBox_7.cmdin', control_type="Button").wait('enabled', 100)
        # time.sleep(10)
        print('aaaaaaaaaaaaaaaa')
        if name=='':
            kongzhi.paizhaoshibie(self)
            print('表格名称不可用，已自动跳过')
            print('未识别')

        else:
            kongzhi.xunzhao(self,name)
            print('已识别')

    #根据模板标题寻找模板并点击
    def xunzhao(self,name):
        self.main_spec.window(title=r'任务队列', control_type="TabItem").invoke()  # 点击选项卡，点击(uia mode) #
        self.main_spec.window(
            auto_id=r'MainWindow.centralWidget.tabWidget.qt_tabwidget_stackedwidget.tab4.stored.storedscan',
            control_type="Edit").set_text('')
        self.main_spec.window(
            auto_id=r'MainWindow.centralWidget.tabWidget.qt_tabwidget_stackedwidget.tab4.stored.storedscan',
            control_type="Edit").set_text(name)

        def __get_element_postion(element):
            element_position = element.rectangle()  # 算出中心点位置
            center_position = (int((element_position.left + element_position.right) / 2),
                               int((element_position.top + element_position.bottom) / 2))
            return center_position  # 点击进入任务队列选项卡

        # 点击listitem内容，拼接字符串
        aa='.*'+name+'.*'
        file_helper_element = self.main_spec.window(title_re=aa, control_type="ListItem")  # 点击Button控件，进入登录界面
        if file_helper_element.exists():
            file_helper_element.wrapper_object().click_input()
            print('完成')
            # self.main_spec.window(title=r'前往', control_type="Button").click()
            # kongzhi.shuxie(self)
        else:
            print('模板不存在，请重新定义模板')
        # main.Application_ui.fanhuipz(self, cname)




        def capture_as_image(self, rect=None):
            """
            Return a PIL image of the control.

            See PIL documentation to know what you can do with the resulting
            image.
            """
            control_rectangle = self.rectangle()
            if not (control_rectangle.width() and control_rectangle.height()):
                return None

            # PIL is optional so check first
            if not ImageGrab:
                print("PIL does not seem to be installed. "
                      "PIL is required for capture_as_image")
                self.actions.log("PIL does not seem to be installed. "
                                 "PIL is required for capture_as_image")
                return None

            if rect:
                control_rectangle = rect

            # get the control rectangle in a way that PIL likes it
            width = control_rectangle.width()
            height = control_rectangle.height()
            left = control_rectangle.left
            right = control_rectangle.right
            top = control_rectangle.top
            bottom = control_rectangle.bottom
            box = (left, top, right, bottom)

            # check the number of monitors connected
            if (sys.platform == 'win32') and (len(win32api.EnumDisplayMonitors()) > 1):
                hwin = win32gui.GetDesktopWindow()
                hwindc = win32gui.GetWindowDC(hwin)
                srcdc = win32ui.CreateDCFromHandle(hwindc)
                memdc = srcdc.CreateCompatibleDC()
                bmp = win32ui.CreateBitmap()
                bmp.CreateCompatibleBitmap(srcdc, width, height)
                memdc.SelectObject(bmp)
                memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

                bmpinfo = bmp.GetInfo()
                bmpstr = bmp.GetBitmapBits(True)
                pil_img_obj = Image.frombuffer('RGB',
                                               (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
                                               bmpstr,
                                               'raw',
                                               'BGRX',
                                               0,
                                               1)
            else:
                # grab the image and get raw data as a string
                pil_img_obj = ImageGrab.grab(box)

            return pil_img_obj

    # save_img 截图保存命名，coord以元组形式传入控件坐标
    def capture_image(coord=(10, 929, 122, 1070), save_img='default.png'):
        im = ImageGrab.grab(coord)
        # 参数 保存截图文件的路径
        im.save(save_img)

    def tuichu(self):
        # 关闭app并退出
        self.main_spec.wait("exists ready", timeout=5, retry_interval=3)  # 等到窗口真的开着
        self.main_spec.set_focus()
        self.main_spec.window(title=r'×', control_type="Button").click()  # 点击Button控件，进入登录界面
        self.main_spec.window(title=r'是', control_type="Button").click()  # 点击Button控件，进入登录界面

        # TempStdoutArea对象为为重定向标准输出准备的空间，以列表形式存在


class TempStdoutArea:
    def __init__(self):
        self.buffer = []

    def write(self, *args, **kwargs):
        self.buffer.append(args)


# 实现获取指定控件坐标的对象
class GetControlCoord:
    # app为 pywinauto框架实例化的Application对象
    def __init__(self, app):
        self.app = app

    # 获取指定控件坐标的方法，control参数传入指定控件
    def get_coord(self, control):
        # 重定向标准输出，将原本的标准输出信息写入自定义的空间内，以获取控件信息
        stdout = sys.stdout
        sys.stdout = TempStdoutArea()
        # pywinauto框架提供的print_control_identifiers()方法，可以打印出应用程序的控件信息，其中就包含控件坐标
        self.main_spec.print_control_identifiers()
        # 将控件信息转移到control_identifiers，并还原标准输出
        control_identifiers, sys.stdout = sys.stdout, stdout
        # print(control_identifiers.buffer)

        all_coord = []
        # 遍历控件信息，获取指定控件的坐标
        for a_control_identifier in control_identifiers.buffer:
            # print(a_control_identifier)
            print(a_control_identifier[0])
            a_control_identifier = a_control_identifier[0]
            # print(dir(a_control_identifier.find(control)))
            if a_control_identifier.find(control) > -1:
                # print(a_control_identifier)
                a_coord = []
                str_coord = a_control_identifier[
                            a_control_identifier.find('(') + 1: a_control_identifier.find(')')].split(',')
                # print(str_coord)
                for i in str_coord:
                    num = int(i.strip()[1:])
                    a_coord.append(num)
                all_coord.append(a_coord)
        return all_coord
