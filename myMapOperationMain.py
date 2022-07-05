# -*- coding: UTF-8 -*-
"""
--------------------------------------------------------
@File             : myMapOperationMain.py
@Creat Time       : 2022-03-21
@Author           : wzp
@Site             : 
@Software         : PyCharm
@file Conent      :
--------------------------------------------------------
@Revise history   :
@Version          : V12
@Amendant records :
     1)wangzp  2022/03/21
"""
import sys

from myMap import Ui_MainWindow
from QlearingMain import *
from qtpy import QtWidgets
import threading

lock = threading.Lock()


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)


    # 定义按钮单击事件
    def onclickStartBtn(self):
        # self.Agent.setGeometry(160, 90, 60, 60)
        t = threading.Thread(target=self.rl)
        t.start()


    # 控制UI的函数，传入位置，循环次数，步数
    def update_env(self,S,episode,step_counter):

        AgentWidth, AgentHeight = 110, 110
        lock.acquire()
        self.label_lun_num.setText(str(episode))
        self.label_bu_num.setText(str(step_counter))
        # if q_table_str is not None:
        #     self.QtableBrowser.setText(q_table_str)
        if S == 0:
            self.Agent.setGeometry(0, 70, AgentWidth, AgentHeight)
        elif S == 1:
            self.Agent.setGeometry(130, 70, AgentWidth, AgentHeight)
        elif S == 2:
            self.Agent.setGeometry(260, 70, AgentWidth, AgentHeight)
        elif S == 3:
            self.Agent.setGeometry(390, 70, AgentWidth, AgentHeight)
        elif S == 4:
            self.Agent.setGeometry(0, 180, AgentWidth, AgentHeight)
        elif S == 5:
            self.Agent.setGeometry(130, 180, AgentWidth, AgentHeight)
        elif S == 6:
            self.Agent.setGeometry(260, 180, AgentWidth, AgentHeight)
        elif S == 7:
            self.Agent.setGeometry(390, 180, AgentWidth, AgentHeight)
        elif S == 8:
            self.Agent.setGeometry(0, 300, AgentWidth, AgentHeight)
        elif S == 9:
            self.Agent.setGeometry(130, 300, AgentWidth, AgentHeight)
        elif S == 10:
            self.Agent.setGeometry(260, 300, AgentWidth, AgentHeight)
        elif S ==11:
            self.Agent.setGeometry(390, 300, AgentWidth, AgentHeight)
        elif S == 12:
            self.Agent.setGeometry(0, 420, AgentWidth, AgentHeight)
        elif S == 13:
            self.Agent.setGeometry(130, 420, AgentWidth, AgentHeight)
        elif S == 14:
            self.Agent.setGeometry(260, 420, AgentWidth, AgentHeight)
        elif S == 15:
            self.Agent.setGeometry(390, 420, AgentWidth, AgentHeight)
        lock.release()

    # Qlearing主循环函数
    def rl(self):
        try:
            ALPHA = self.AlphaLearnRate.value()      # 获取学习率
            MAX_EPISODES = self.MAX_EPISODES.value() # 获取游戏局数
            GAMMA = self.GAMMA.value()               # 获取衰减因子，对于未来的Reward的关注程度
            FRESH_TIME = self.FRESH_TIME.value()     # 获取地图刷新间隔
            EPSILON = self.EPSILON.value()           # 获取ε-greedy中的ε，数值越小，随机性越强
        except Exception as e:
            print("参数更新失败！！",e)
        q_table = create_Q_table(N_STATES, ACTIONS)  # 创建Q表
        bestStepsNum = 9999999 # 记录最佳步数
        bestFlag = False       # 是否找到一条成功路径
        bestStepPath = ""      # 成功的路径
        for episode in range(1,MAX_EPISODES+1):  # 游戏局数，episode数(1~MAX_EPISODES)
            bagSet = set()    # 用来判断三个糖果是否都找到
            starNum = 0       # 找到的糖果数量
            isSuccessStr = '' # 撞墙/成果搜索
            stepPath = "0"   # 当前次迭代搜索的步数
            step_counter = 0  # 计数器，计算本次游戏步数
            S = 0  # 本次游戏状态初始化为第一个格子
            is_terminal = False  # 是否达到终态的标记 用于退出该次迭代
            thisIsSuccess = False # 本次迭代是否成功的标记
            time.sleep(0.3)
            # 启动线程 渲染地图 将Agent小人 初始化位置
            t1 = threading.Thread(target=self.update_env, args=(S, episode, step_counter))
            t1.start()

            while not is_terminal:  # 未到达终态
                self.update()
                time.sleep(FRESH_TIME)
                A = choose_action(S, q_table)  # ε-greedy选择动作，一开始随机选择，因为都是0
                S_, R = get_env_feedback(S, A)  # 与环境交互获得下一状态状态和回报值
                stepPath = stepPath + "-" + str(S_)
                if S_ in sweetStateList: # 判断下一个节点是否为糖果所在位置
                    if S_ in bagSet:     # 判断是否重复拾取
                        R = -1           # 重复拾取的糖果位置 没有奖励 奖励为-1
                    # 利用集合无重复元素的机制
                    a = len(bagSet)
                    bagSet.add(S_)
                    if len(bagSet) > a: # 如果成功放入（size+1），则代表拾取到了新的糖果
                        starNum += 1

                q_predict = q_table.loc[S, A]  # 估计Q值，也就是当前的Q值
                if S_ == 'over':
                    q_target = R
                    is_terminal = True
                    isSuccessStr = "撞墙"
                    t = threading.Thread(target=self.update_env, args=(0, episode, step_counter))
                    t.start()
                if S_ != 'over':
                    q_target = R + GAMMA * q_table.iloc[S_, :].max()  # 最大Q值对应的动作，真实值估计
                if starNum >= 3:  # 成功拾取三个糖果
                    q_target = R  # 终态的话，直接得到真实的回报值
                    is_terminal = True
                    isSuccessStr = "成功搜索"
                    thisIsSuccess = True
                # 更新Q表的关键函数
                q_table.loc[S, A] += ALPHA * (q_target - q_predict)  # 更新Q表
                S = S_  # 状态转移
                step_counter += 1  # 本次迭代的步数 加一步
                # 启用线程 渲染状态下的环境
                t2 = threading.Thread(target=self.update_env, args=(S, episode, step_counter))
                t2.start()
            self.update() # 刷新
            # print(starNum)
            print("第{0}轮结束，步数为{1},{2},路径为{3}".format(episode, step_counter, isSuccessStr, stepPath))
            if thisIsSuccess:  # 判断是否成功搜索
                bestFlag = True
                bestStepsNum = min(bestStepsNum,step_counter)
                bestStepPath = stepPath

        time.sleep(0.5)
        print(q_table)  # 输出最终的Q表
        if bestFlag:
            str1 = "经过{0}次迭代搜索，本次搜索成功，最小步数为{1}，最短路径为{2}".format(MAX_EPISODES, bestStepsNum, bestStepPath)
            print(str1)
        else:
            str2 = "经过{0}次迭代搜索，本次搜索失败".format(MAX_EPISODES)
            print(str2)
        return q_table





if __name__ == '__main__':
    # sys.path.append(r"/Users/wangzhipeng/PycharmProjects/QlearningDemo")
    app = QtWidgets.QApplication(sys.argv)

    win = MyWindow()
    win.startButton.clicked.connect(win.onclickStartBtn) # 设置点击事件
    win.show()
    sys.exit(app.exec_())