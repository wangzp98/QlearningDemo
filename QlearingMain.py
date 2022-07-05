# -*- coding: UTF-8 -*-
"""
--------------------------------------------------------
@File             : simpleDemo1.py
@Creat Time       : 2022-03-19
@Author           : wzp
@Site             :
@Software         : PyCharm
@file Conent      :
--------------------------------------------------------
@Revise history   :
@Version          : V12
@Amendant records :
     1)wangzp  2022/03/19
"""
import numpy as np
import pandas as pd
import time
import sys

np.random.seed(2)  # 设置随机种子，保证生成随机数相同

from data import *

# 建立Q表函数
def create_Q_table(state_num, actions):  # 输入状态数和动作空间
    table = pd.DataFrame(np.zeros((state_num, len(actions))), columns=actions)  # 创建一个表格，规格为状态数*动作数，列名为动作空间名称
    print("创建的Q表如下：")
    print(table)  # 输出表格观察
    return table


# 动作选择函数，根据ε和Q值选择状态s下的最佳动作
def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]  # 选择表格对应s行的所有列值
    # if (np.random.uniform() > EPSILON) or (state_actions.all() == 0):  # 生成随机数，如果大于0.9也就是0.1的几率，或者两个动作Q值都为0
    #     action_name = np.random.choice(ACTIONS)   # 随机选择一个动作，返回动作名称"left" 或 "right"
    # else:
    #     action_name = state_actions.idxmax()  # 返回最大Q值对应的动作名称
    # return action_name  # 返回名称，可能因为pandas用列名访问
    """
    我的改进
    """
    update_flag = False
    for item in state_actions:
        if (item>0):
            update_flag = True

    if (state_actions.all() == 0):  # 四个动作Q值都为0
        action_name = np.random.choice(ACTIONS)   # 随机选择一个动作，返回动作名称"left" 或 "right" "up" "down"
    elif((update_flag == False) and (np.random.uniform() > EPSILON)):
        action_name = np.random.choice(ACTIONS)
    elif((update_flag == True) and (np.random.uniform() > (EPSILON+(1-EPSILON)*0.5)   )):
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax()  # 返回最大Q值对应的动作名称
    return action_name  # 返回名称，可能因为pandas用列名访问


# 环境反馈函数
def get_env_feedback(state, action):  # 输入一个状态和动作
    # if action == 'right':  # 向右走
    #     if state == N_STATES - 2:  # 下一步就是终态，现在在倒数第二个格
    #         state = 'terminal'  # 标记为终点
    #         R = 1  # 获得奖励
    #     else:
    #         state = state + 1  # 往右走一格
    #         R = 0  # 普通格子无奖励
    # else:  # 向左走
    #     R = 0  # 这里的意思是往左走不可能到达终态
    #     if state == 0:  # 走到最左边，再走下一步撞墙了
    #         state = state  # 原地不动，下一状态还是原地
    #     else:
    #         state = state - 1  # 向左走一格
    if action == 'up':
        if state in [0,1,2,3]:
            state = 'over'
            R = -100
        else:
            state = state - 4
            R = -1
            if state == 8:
                R = 10
    if action == 'down':
        if state in [12, 13, 14, 15]:
            state = 'over'
            R = -100
        else:
            state = state + 4
            R = -1
            if state in sweetStateList:
                R = 10

    if action == 'left':
        if state in [0, 4, 8, 12]:
            state = 'over'
            R = -100
        else:
            state = state - 1
            R = -1
            if state in sweetStateList:
                R = 10

    if action == 'right':
        if state in [3, 7,11, 15]:
            state = 'over'
            R = -100
        else:
            state = state + 1
            R = -1
            if state in sweetStateList:
                R = 10

     # 返回下一个状态及奖励
    return state, R


# 更新环境动画界面函数，纯粹根据当前状态绘制图像（命令行）
# def update_env(state, episode, step_counter):
#     env_list = ['-']*(N_STATES - 1) + ['T']  # 一开始的环境列表是['-', '-', '-', '-', '-', 'T']
#     if state == 'terminal':  # 到达终态
#         interaction = 'Episode {0}: total_steps = {1}'.format(episode, step_counter)  # 输出本次进程的信息，第几次游戏，一共走了几步到终点
#         print('\r{}'.format(interaction), end='')  # \r是光标回到前一行，应该是原地刷新
#         time.sleep(2)  # 暂停
#         print('\r                                ', end='')  # 输出空行，视觉暂留
#     else:
#         env_list[state] = 'o'  # 标记机器人位置
#         interaction = ''.join(env_list)  # 把列表转成字符串
#         print('\r{}'.format(interaction), end='')
#         time.sleep(FRESH_TIME)  # 暂停







# def startGame():
#     q_table = rl()  # 返回Q表
#     print("\r最终Q表:")
#     print(q_table)


#
# if __name__ == '__main__':
#     # 主函数
#     q_table = rl()  # 返回Q表
#     print("\r最终Q表:")
#     print(q_table)
