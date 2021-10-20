#
# def add_one_line():
#     global counter
#
#     chat_record_box.configure(state=tk.NORMAL)
#     text = f'Line {counter}'
#     if counter:
#         text = '\n'+text
#     chat_record_box.insert("end", text)
#     chat_record_box.see("end")
#     chat_record_box.configure(state=tk.DISABLED)
#     counter += 1
#
# mainWnd = tk.Tk()
# mainWnd.title("test")
#
# mainWnd.attributes("-alpha",0.95)
# chat_record_box = tk.Text(mainWnd, fg='Violet', font=("楷体"),bg='FloralWhite',
#     highlightthickness='2', selectbackground='blue')
# chat_record_box.pack(padx=10, pady=10)
# chat_record_box.configure(state=tk.DISABLED)
#
# button = tk.Button(text="Add one line", command=add_one_line)
# button.pack()
# counter = 0
#
# mainWnd.mainloop()

#
# ROOT = Tk()
#
# def ask_for_userinput():
#     user_input = input("Give me your command! Just type \"exit\" to close: ")
#     if user_input == "exit":
#         ROOT.after_cancel(ask_for_userinput)
#     else:
#         label = Label(ROOT, text=user_input)
#         label.pack()
#         ROOT.after(100, ask_for_userinput)
#
# LABEL = Label(ROOT, text="Hello, world!")
# LABEL.pack()
# ROOT.after(1000, ask_for_userinput)
# ROOT.mainloop()
# from tkinter import *
# import threading, queue
#
#
# class App(threading.Thread):
#
#     def __init__(self, top):
#         self.notify_queue = queue.Queue()
#         self.top = Toplevel(top)
#         self.loop_active = True
#         # 在UI线程启动消息队列循环
#         self.process_msg()
#         threading.Thread.__init__(self)
#         self.setDaemon(True)
#         self.start()
#
#     def run(self):
#         while self.loop_active:
#             user_input = input("Give me your command! Just type \"exit\" to close: ")
#             label = Label(self.top, text=user_input)
#             label.pack()
#             if user_input == "exit":
#                 # loop_active = False
#                 self.notify_queue.put(1)
#         self.top.destroy()
#
#     def process_msg(self):
#         self.top.after(400, self.process_msg)
#         while not self.notify_queue.empty():
#             try:
#                 msg = self.notify_queue.get()
#                 print(msg)
#                 if msg == 1:
#                     self.loop_active = False
#                     print(self.loop_active)
#             except queue.Empty:
#                 pass
#
#
# ROOT = Tk()
# APP = App(ROOT)
# ROOT.mainloop()

# def auto_accept(*args):
#     print('111111111111111')
#     # while True:
#     #     try:
#     #         app = pywinauto.Application()
#     #         app.window_(title='新建文本文档 (2).txt-记事本').SetFocus()
#     #         app.window_(title='新建文本文档 (2).txt-记事本').TypeKeys("{1}{2}{3}")
#     #     except (pywinauto.findwindows.WindowNotFoundError, pywinauto.timings.TimeoutError):
#     #         pass
# ROOT = Tk()
# # APP = App(ROOT)
# ROOT.after(10, auto_accept)
# ROOT.mainloop()

'''for wmplayer operations, win8.1 os
    'wmplayer_start',
    'wmplayer_close',

    'wmplayer_open_media_file',
    'wmplayer_play'
    'wmplayer_pause'
    'wmplayer_set_repeat_on',
    'wmplayer_set_repeat_off'
    'wmplayer_volume_up'
    'wmplayer_volume_down'
    'wmplayer_mute'
    'wmplayer_unmute'
    'wmplayer_seek'

    'wmplayer_wait_playback_end',
'''

import os

import AXUI

config_file = "windows.cfg"
app_map = "windows_media_player.xml"

AXUI.Config(config_file)
appmap = AXUI.AppMap(app_map)


def wmplayer_start():
    appmap.wmplayer_Window.start()


def wmplayer_close():
    appmap.wmplayer_Window.stop()


def wmplayer_open_media_file(media_file):
    if not os.path.isfile(media_file):
        print(("media file not exist: %s" % media_file))
        return
    appmap.wmplayer_Window.Open_Dialog.FileName_ComboBox.FileName_Edit.ValuePattern.SetValue(media_file)
    appmap.wmplayer_Window.Open_Dialog.Open_Button.InvokePattern.Invoke()


def wmplayer_play():
    appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.start()
    if appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.Name == "Play":
        appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.InvokePattern.Invoke()


def wmplayer_pause():
    appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.start()
    if appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.Name == "Pause":
        appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.InvokePattern.Invoke()


def wmplayer_set_repeat_on():
    appmap.wmplayer_Window.TransportSubview_Group.repeat_Button.start()
    if appmap.wmplayer_Window.TransportSubview_Group.repeat_Button.Name == "Turn repeat on":
        appmap.wmplayer_Window.TransportSubview_Group.repeat_Button.InvokePattern.Invoke()


def wmplayer_set_repeat_off():
    appmap.wmplayer_Window.TransportSubview_Group.repeat_Button.start()
    if appmap.wmplayer_Window.TransportSubview_Group.repeat_Button.Name == "Turn repeat off":
        appmap.wmplayer_Window.TransportSubview_Group.repeat_Button.InvokePattern.Invoke()


def wmplayer_volume_up():
    appmap.wmplayer_Window.keyboard.Input('{F9}')


def wmplayer_volume_down():
    appmap.wmplayer_Window.keyboard.Input('{F8}')


def wmplayer_mute():
    appmap.wmplayer_Window.MenuBar.Play_MenuItem.SetFocus()
    if int(appmap.wmplayer_Window.Volume_Menu.Mute_MenuItem.LegacyIAccessiblePattern.CurrentState) == int(0):
        appmap.wmplayer_Window.Volume_Menu.Mute_MenuItem.InvokePattern.Invoke()


def wmplayer_unmute():
    appmap.wmplayer_Window.MenuBar.Play_MenuItem.SetFocus()
    if int(appmap.wmplayer_Window.Volume_Menu.Mute_MenuItem.LegacyIAccessiblePattern.CurrentState) == int(16):
        appmap.wmplayer_Window.Volume_Menu.Mute_MenuItem.InvokePattern.Invoke()


def wmplayer_seek(seek_value):
    left, right, top, bottom = appmap.wmplayer_Window.Seek_Slider.coordinate

    x = (right - left) * (seek_value / 100) + left
    y = (bottom + top) / 2

    appmap.wmplayer_Window.Seek_Slider.SetFocus()
    appmap.wmplayer_Window.Seek_Slider.Mouse.left_click((x, y))


def wmplayer_wait_playback_end():
    import time
    while True:
        time.sleep(1)
        if appmap.wmplayer_Window.TransportSubview_Group.Play_Pause_Button.Name == "Play":
            break
