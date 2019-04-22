from k_means_rgb_img import KMeansRGB

from settings import Settings
import os
import tkinter
import tkinter.messagebox


class AppGUI(object):
    def __init__(self):
        # 初始化参数
        self.global_set = Settings()
        # 创建主窗口,用于容纳其它组件
        self.root_window = tkinter.Tk()
        self.root_window.geometry("800x500")
        # 预定义显示对象
        self.display_info = None
        self.file_label_1 = None
        self.file_label_2 = None
        self.cos_dis_listbox_1 = None
        self.cos_dis_listbox_2 = None
        self.text_1 = None
        self.text_2 = None
        self.cos_dis_label = None
        self.search_text_entry = None
        self.search_listbox = None
        self.search_text_show = None
        self.k_means_c_class_listbox = None
        self.k_means_c_file_listbox = None
        self.k_means_c_text_show = None
        self.k_means_e_class_listbox = None
        self.k_means_e_file_listbox = None
        self.k_means_e_text_show = None
        # 预定义显示子窗口
        self.search_window = None
        self.cos_dis_window = None
        self.k_means_c_window = None
        self.k_means_e_window = None
        # 预定义类
        self.CDC = None
        self.k_means_c = None
        self.k_means_e = None
        # 运算变量
        self.word_list = []
        self.file_seq_list = []
        self.idf_list = []

    # root窗口布局
    def root_gui_arrange(self):
        # 给主窗口设置标题内容
        self.root_window.title("图片K-means聚类-演示系统")
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root_window, width=50)
        self.global_set.display_info = self.display_info
        # 创建Scrollbar
        y_scrollbar = tkinter.Scrollbar(self.root_window)
        y_scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.display_info.config(yscrollcommand=y_scrollbar.set)
        y_scrollbar.config(command=self.display_info.yview)

        # 创建菜单项
        menu_bar = tkinter.Menu(self.root_window)
        # 下拉菜单2
        menu_c2 = tkinter.Menu(self.root_window, tearoff=0)
        # 添加的是下拉菜单的菜单项
        menu_c2.add_command(label='功能 1:-> 图像像素聚类（基于RGB）', command=self.RGBKmeans_gui_arrange)
        menu_c2.add_command(label='功能 2:-> 图像像素聚类（基于RGBXY）', command=self.RGBXYKmeans_gui_arrange)
        # 下拉菜单3
        menu_c3 = tkinter.Menu(self.root_window, tearoff=0)
        for item in ['版权信息', '其他说明']:
            menu_c3.add_command(label=item)
        # 指明父菜单
        menu_bar.add_cascade(label="主要功能", menu=menu_c2)
        menu_bar.add_cascade(label="关于", menu=menu_c3)
        # 菜单实例应用到大窗口中
        self.root_window['menu'] = menu_bar
        # 信息显示框布局
        self.display_info.pack(expand='yes', fill='both')

    # K-Means 中文文档 窗口布局
    def RGBKmeans_gui_arrange(self):
        # 定义长在窗口上的搜索窗口
        self.search_window = tkinter.Toplevel(self.root_window)
        self.search_window.geometry('360x100')
        self.search_window.title('搜索文档')

        # 设定标签
        show_label_1 = tkinter.Label(self.search_window, text='图像像素聚类（基于RGB）')
        show_label_2 = tkinter.Label(self.search_window, text='请输入K值：')
        # 设定输入框
        self.search_text_entry = tkinter.Entry(self.search_window)
        # 设定按钮
        button = tkinter.Button(self.search_window, text='开始！', command=self.RGBKmeans_btn_fun)

        # 布局
        # 第一行
        show_label_1.grid(row=0, column=3)
        # 第二行
        show_label_2.grid(row=1, column=0)
        self.search_text_entry.grid(row=1, column=1, columnspan=8, sticky=tkinter.E + tkinter.W)
        button.grid(row=1, column=9)

    # K-Means 中文文档 窗口布局
    def RGBXYKmeans_gui_arrange(self):
        # 定义长在窗口上的搜索窗口
        self.search_window = tkinter.Toplevel(self.root_window)
        self.search_window.geometry('800x450')
        self.search_window.title('搜索文档')

        # 设定标签
        show_label_1 = tkinter.Label(self.search_window, text='搜索文档（对所有文档）')
        show_label_2 = tkinter.Label(self.search_window, text='请输入关键词：')
        show_label_3 = tkinter.Label(self.search_window, text='搜索结果：')
        show_label_4 = tkinter.Label(self.search_window, text='文档原文（双击列表框内文件名显示原文）：')
        # 设定输入框
        self.search_text_entry = tkinter.Entry(self.search_window)
        # 设定按钮
        button = tkinter.Button(self.search_window, text='搜索！', command=self.search_btn_fun)
        # 创建第一个Listbox
        self.search_listbox = tkinter.Listbox(self.search_window, height=20, width=25)
        # 创建匹配的Scrollbar
        y_scrollbar_1 = tkinter.Scrollbar(self.search_window)
        self.search_listbox.config(yscrollcommand=y_scrollbar_1.set)
        y_scrollbar_1.config(command=self.search_listbox.yview)
        # 绑定事件
        self.search_listbox.bind('<Double-Button-1>', self.search_listbox_click_fun)
        # 设定文本框
        self.search_text_show = tkinter.Text(self.search_window, height=20, width=80)
        # 创建匹配的Scrollbar
        y_scrollbar_2 = tkinter.Scrollbar(self.search_window)
        self.search_text_show.config(yscrollcommand=y_scrollbar_2.set)
        y_scrollbar_2.config(command=self.search_text_show.yview)

        # 布局
        # 第一行
        show_label_1.grid(row=0, column=3)
        # 第二行
        show_label_2.grid(row=1, column=0)
        self.search_text_entry.grid(row=1, column=1, columnspan=8, sticky=tkinter.E + tkinter.W)
        button.grid(row=1, column=9)
        # 第三行
        show_label_3.grid(row=2, column=0, sticky=tkinter.W)
        show_label_4.grid(row=2, column=3, sticky=tkinter.W)
        # 第四行
        self.search_listbox.grid(row=3, column=0, columnspan=2, sticky=tkinter.E + tkinter.W)
        y_scrollbar_1.grid(row=3, column=2, sticky=tkinter.N + tkinter.S + tkinter.W)
        self.search_text_show.grid(row=3, column=3, columnspan=7, sticky=tkinter.N + tkinter.S)
        y_scrollbar_2.grid(row=3, column=10, sticky=tkinter.N + tkinter.S + tkinter.W)

    # K_Means 中文文档 界面 - 聚类功能
    def RGBKmeans_btn_fun(self):
        self.k_means_c = KMeansRGB(self.global_set)
        k_value = int(self.search_text_entry.get())
        self.k_means_c.k_means_cal(k_value)

    # K_Means 中文文档 界面 - 聚类功能
    def RGBXYKmeans_btn_fun(self):
        self.k_means_c = KMeansChineseNews(self.global_set)
        self.k_means_c.k_means_cal()
        # 取前三个大类 加入类列表
        self.k_means_c_class_listbox.delete(0, 'end')
        for index in range(3):
            class_label = self.k_means_c.class_file_seq_list[index][0]
            # 取类对应特征词前8个
            class_feature_word = self.k_means_c.class_word_seq_list[class_label][1][0:8]
            class_listbox_str = '类序号:' + str(class_label) + ' > 类特征词:' + str(class_feature_word)
            self.k_means_c_class_listbox.insert('end', class_listbox_str)
        # 类列表 默认选第一类
        class_label = 0
        self.k_means_c_class_listbox.select_set(class_label)
        self.k_means_c_file_listbox.delete(0, 'end')
        # 取类中所有文件 加入文件列表
        for file_index in self.k_means_c.class_file_seq_list[class_label][1]:
            file_name = 'News_' + str(file_index + 1) + '_C.txt'
            self.k_means_c_file_listbox.insert('end', file_name)
        # 文件列表 默认选第一个
        file_index = 0
        self.k_means_c_file_listbox.select_set(file_index)
        # 取文件内容
        file_name = self.k_means_c_file_listbox.get(0)
        print('default file selected: ' + file_name)
        self.k_means_c_text_show.delete('1.0', 'end')
        self.k_means_c_text_show.insert('insert', self.get_txt(file_name))


def main():
    # 初始化对象
    app = AppGUI()
    # 进行布局
    app.root_gui_arrange()
    # 程序自检
    app.global_set.sys_log_check()
    # 主程序执行
    tkinter.mainloop()


if __name__ == "__main__":
    main()
