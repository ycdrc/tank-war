# -*- coding: utf-8 -*-
"""
墙壁类模块
定义了游戏中的砖块、铁块和地图类
"""

import pygame
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'image')

# 墙壁图片路径
brickImage = os.path.join(IMAGE_DIR, 'brick.png')
ironImage = os.path.join(IMAGE_DIR, 'iron.png')

class Brick(pygame.sprite.Sprite):
    """
    砖块类
    继承自pygame的Sprite类，用于表示可被摧毁的砖块
    """
    def __init__(self):
        """
        初始化砖块对象
        加载砖块图片并设置其矩形区域
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(brickImage)
        self.rect = self.image.get_rect()

class Iron(pygame.sprite.Sprite):
    """
    铁块类
    继承自pygame的Sprite类，用于表示不可被普通子弹摧毁的铁块
    """
    def __init__(self):
        """
        初始化铁块对象
        加载铁块图片并设置其矩形区域
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(ironImage)
        self.rect = self.image.get_rect()

class Map():
    """
    地图类
    用于创建和管理游戏地图中的砖块和铁块
    """
    def __init__(self):
        """
        初始化地图对象
        创建砖块组和铁块组，并在地图上放置相应的障碍物
        """
        # 创建精灵组
        self.brickGroup = pygame.sprite.Group()  # 砖块组
        self.ironGroup  = pygame.sprite.Group()  # 铁块组
        
        # 定义地图布局
        # 第一、三、七、九列砖块的位置
        X1379 = [2, 3, 6, 7, 18, 19, 22, 23]
        Y1379 = [2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, 20, 21, 22, 23]
        # 第二、八列砖块的位置
        X28 = [10, 11, 14, 15]
        Y28 = [2, 3, 4, 5, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20]
        # 第四、六列砖块的位置
        X46 = [4, 5, 6, 7, 18, 19, 20, 21]
        Y46 = [13, 14]
        # 第五列砖块的位置
        X5  = [12, 13]
        Y5  = [16, 17]
        # 基地周围的砖块位置
        X0Y0 = [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]

        # 放置第一、三、七、九列的砖块
        for x in X1379:
            for y in Y1379:
                self._place_brick(x, y)
        
        # 放置第二、八列的砖块
        for x in X28:
            for y in Y28:
                self._place_brick(x, y)
        
        # 放置第四、六列的砖块
        for x in X46:
            for y in Y46:
                self._place_brick(x, y)
        
        # 放置第五列的砖块
        for x in X5:
            for y in Y5:
                self._place_brick(x, y)
        
        # 放置基地周围的砖块
        for x, y in X0Y0:
            self._place_brick(x, y)
        
        # 放置铁块
        iron_positions = [(0,14),(1,14),(12,6),(13,6),(12,7),(13,7),(24,14),(25,14)]
        for x, y in iron_positions:
            self._place_iron(x, y)

    def _place_brick(self, x, y):
        """
        在指定位置放置砖块
        
        参数:
            x: x坐标
            y: y坐标
        """
        self.brick = Brick()
        self.brick.rect.left, self.brick.rect.top = 3 + x * 24, 3 + y * 24
        self.brickGroup.add(self.brick)

    def _place_iron(self, x, y):
        """
        在指定位置放置铁块
        
        参数:
            x: x坐标
            y: y坐标
        """
        self.iron = Iron()
        self.iron.rect.left, self.iron.rect.top = 3 + x * 24, 3 + y * 24
        self.ironGroup.add(self.iron)

