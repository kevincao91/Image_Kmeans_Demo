import tkinter
import tkinter.messagebox
import os
import sys


class Settings:
    # 配置程序所有的设置数据
    def __init__(self):
        #  初始化程序的设置
        self.display_info = None
        self.display_index = 0

    # GUI上显示的滚动行
    def print_gui(self, string):
        self.display_info.insert(self.display_index, string)
        self.display_info.see(self.display_index)
        self.display_info.select_clear(0, 'end')
        self.display_info.select_set(self.display_index)
        self.display_info.update()
        self.display_index += 1

    # 前提条件检查
    def sys_log_check(self):
        # 显示信息
        string = '系统自检中 ... ...'
        self.print_gui(string)
        # 判断各类表是否存在
        file_path_1 = 'img.jpg'
        if os.path.exists(file_path_1):
            pass
        else:
            print('have no ' + file_path_1 + '!')
            string = '缺失文件：' + file_path_1
            self.print_gui(string)
            tkinter.messagebox.showerror(title='错误', message=string)  # 提出错误对话窗
            sys.exit()
        # 显示信息
        string = '系统自检成功，载入数据完成！'
        self.print_gui(string)
