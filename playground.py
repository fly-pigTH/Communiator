import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.animation import FuncAnimation

field_w=750
field_h=468

# 加载足球场图像
soccer_field = mpimg.imread('soccer_field.jpg')

# 创建一个实时绘制的图像窗口
fig, ax = plt.subplots()
ax.imshow(soccer_field, extent=[0, field_w, 0, field_h])  # 设置足球场图像的坐标范围
scatter = ax.scatter([], [])
ax.set_title('实时坐标绘制')
ax.set_xlabel('X轴')
ax.set_ylabel('Y轴')

# 更新散点坐标的回调函数
def update(i):
    x = np.random.uniform(0, field_w)  # 在足球场范围内生成随机X坐标
    y = np.random.uniform(0, field_h)   # 在足球场范围内生成随机Y坐标
    scatter.set_offsets(np.array([[x, y]]))

# 使用FuncAnimation实时更新散点坐标
ani = FuncAnimation(fig, update, interval=1000)  # 每1000毫秒更新一次
plt.show()
