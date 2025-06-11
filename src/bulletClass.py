# -*- coding: utf-8 -*-
"""
子弹类模块
定义了游戏中所有子弹的基本属性和行为
"""

import pygame
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'image')

class Bullet(pygame.sprite.Sprite):
    """
    子弹类
    继承自pygame的Sprite类，用于处理子弹的显示和移动
    """
    def __init__(self):
        """
        初始化子弹对象
        加载子弹图片，设置基本属性
        """
        pygame.sprite.Sprite.__init__(self)
        
        # 加载四个方向的子弹图片
        self.bullet_up = pygame.image.load(os.path.join(IMAGE_DIR, 'bullet_up.png'))
        self.bullet_down = pygame.image.load(os.path.join(IMAGE_DIR, 'bullet_down.png'))
        self.bullet_left = pygame.image.load(os.path.join(IMAGE_DIR, 'bullet_left.png'))
        self.bullet_right = pygame.image.load(os.path.join(IMAGE_DIR, 'bullet_right.png'))

        # 子弹的基本属性
        self.dir_x, self.dir_y = 0, 0  # 子弹的移动方向
        self.speed = 6  # 子弹的移动速度
        self.life = False  # 子弹是否存活
        self.strong = False  # 子弹是否具有穿墙能力

        # 设置子弹的初始图像和位置
        self.bullet = self.bullet_up
        self.rect = self.bullet.get_rect()
        self.rect.left, self.rect.right = 3 + 12 * 24, 3 + 24 * 24
    
    def changeImage(self, dir_x, dir_y):
        """
        根据移动方向改变子弹图片
        
        参数:
            dir_x: x方向的移动方向 (-1:左, 0:不动, 1:右)
            dir_y: y方向的移动方向 (-1:上, 0:不动, 1:下)
        """
        self.dir_x, self.dir_y = dir_x, dir_y
        if self.dir_x == 0 and self.dir_y == -1:
            self.bullet = self.bullet_up
        elif self.dir_x == 0 and self.dir_y == 1:
            self.bullet = self.bullet_down
        elif self.dir_x == -1 and self.dir_y == 0:
            self.bullet = self.bullet_left
        elif self.dir_x == 1 and self.dir_y == 0:
            self.bullet = self.bullet_right
    
    def move(self):
        """
        移动子弹并处理边界碰撞
        当子弹碰到边界时，子弹消失
        """
        # 根据方向和速度移动子弹
        self.rect = self.rect.move(self.speed * self.dir_x,
                                   self.speed * self.dir_y)
                
        # 检查是否碰到边界
        if self.rect.top < 3:  # 上边界
            self.life = False
        if self.rect.bottom > 630 - 3:  # 下边界
            self.life = False
        if self.rect.left < 3:  # 左边界
            self.life = False
        if self.rect.right > 630 - 3:  # 右边界
            self.life = False
        
        # 检查是否碰到 brickGroup
        #if pygame.sprite.spritecollide(self, brickGroup, True, None):
        #    self.life = False
        #    moving = 0
        # 检查是否碰到 ironGroup
        #if self.strong:
        #    if pygame.sprite.spritecollide(self, ironGroup, True, None):
        #        self.life = False
        #else:    
        #    if pygame.sprite.spritecollide(self, ironGroup, False, None):
        #        self.life = False
        #    moving = 0
        #return moving
