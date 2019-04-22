import time

from sklearn.cluster import KMeans
import cv2
import numpy as np


class KMeansRGB:
    # 配置程序所有的设置数据
    def __init__(self, global_set):
        #  初始化程序的设置
        self.global_set = global_set
        self.im_ori = None
        self.im_recrt = None
        self.weight = None
        self.cluster_centers = []
        self.labels = []

    def load_data(self):

        im_ori = cv2.imread('img.jpg')
        self.im_ori = im_ori

        # BGR转换为RGB
        im_ori = im_ori[:, :, :: -1]

        width, height, depth = im_ori.shape
        weight = im_ori.reshape(width * height, depth)
        self.weight = np.array(weight, dtype=np.float64)

    def recreate_image(self):
        w, h, d = np.shape(self.im_ori)
        im_recrt = np.zeros((w, h, d), dtype='uint8')
        label_idx = 0
        for i in range(w):
            for j in range(h):
                im_recrt[i][j] = self.cluster_centers[self.labels[label_idx]]
                label_idx += 1

        # RGB to BGR
        im_recrt = im_recrt[..., ::-1]
        self.im_recrt = im_recrt

    def k_means_cal(self, k_value):
        #  开始功能
        string = 'K_Means RGB IMG Function Start.'
        self.global_set.print_gui(string)
        # 计时
        fun_start_time = time.time()

        # 1 加载语料
        # 显示开始信息
        string = '1-> 加载像素内容'
        self.global_set.print_gui(string)
        self.load_data()

        # 2 对向量进行聚类
        # 显示开始信息
        string = '2-> 进行聚类'
        self.global_set.print_gui(string)

        # 指定分成 class_num 个类
        k_means = KMeans(n_clusters=k_value)
        k_means.fit(self.weight)

        # 打印出各个族的中心点
        for center in k_means.cluster_centers_:
            center = [int(item) for item in center]
            self.cluster_centers.append(center)
            print(center)
        # 分组结果
        for pix_index, class_label in enumerate(k_means.labels_, 1):
            # print("index: {}, label: {}".format(pix_index, class_label))
            self.labels.append(class_label)

        # 样本距其最近的聚类中心的平方距离之和，用来评判分类的准确度，值越小越好
        # k-means的超参数n_clusters可以通过该值来评估
        print("inertia: {}".format(k_means.inertia_))

        # 6 图像重建
        # 显示开始信息
        string = '2-> 图像重建'
        self.global_set.print_gui(string)
        self.recreate_image()
        cv2.imwrite('re_img.jpg', self.im_recrt)
        # cv2.imshow('img', self.im_recrt)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

        #  显示结束信息
        fun_end_time = time.time()
        print('Function Finished! in ' + str(fun_end_time - fun_start_time) + 's')
        string = '处理完毕！ 用时： ' + str(round(fun_end_time - fun_start_time, 2)) + '秒'
        self.global_set.print_gui(string)
