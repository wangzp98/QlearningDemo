N_STATES = 16   # 状态数，即世界的长度，本例共有6格
ACTIONS = ['up','down','left', 'right']     # 动作空间，有几个可以选择的动作
EPSILON = 0.99   # ε-greedy中的ε，数值越小，随机性越强
ALPHA = 0.1     # 学习率
GAMMA = 0.9    # 衰减因子，对于未来的Reward的关注程度
MAX_EPISODES = 40   # 最大episode数，完成一局游戏是一个episode


sweetStateList = [8,13,15] # 糖果所在的位置

FRESH_TIME = 0.02    # 刷新动画时间间隔