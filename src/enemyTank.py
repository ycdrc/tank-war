# -*- coding: utf-8 -*-
"""
敌方坦克类模块
定义了游戏中敌方坦克的属性和行为
坦克类型：
1. 普通坦克
2. 快速坦克
3. 重型坦克（3条命）
4. 特殊坦克
"""

import pygame
import random
import os
import bulletClass

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'image')

class EnemyTank(pygame.sprite.Sprite):
    """
    敌方坦克类
    继承自pygame的Sprite类，用于处理敌方坦克的显示和移动
    """
    def __init__(self, x=None, kind=None, isred=None):
        """
        初始化敌方坦克对象
        
        参数:
            x: 坦克的出生位置（1-3）
            kind: 坦克类型（1-4）
            isred: 是否携带道具
        """
        pygame.sprite.Sprite.__init__(self)

        # 坦克动画相关属性
        self.flash = False  # 是否在出生动画中
        self.times = 90     # 动画计时器

        # 设置坦克类型
        self.kind = kind if kind else random.choice([1, 2, 3, 4])

        # 根据类型加载坦克图片
        self._load_tank_images()

        # 设置坦克属性
        self.isred = isred if isred is not None else random.choice((True, False, False, False, False))
        self.tank = self.enemy_x_3 if self.isred else self.enemy_x_0
        self.x = (x if x else random.choice([1, 2, 3])) - 1

        # 设置坦克移动图片
        self.tank_R0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        self.rect = self.tank_R0.get_rect()
        self.rect.left, self.rect.top = 3 + self.x * 12 * 24, 3

        # 坦克基本属性
        self.speed = 3 if self.kind == 2 else 1  # 快速坦克速度更快
        self.dir_x, self.dir_y = 0, 1  # 初始向下移动
        self.life = 3 if self.kind == 3 else 1  # 重型坦克有3条命
        self.bulletNotCooling = True  # 子弹冷却状态
        self.bullet = bulletClass.Bullet()  # 创建子弹对象
        self.dirChange = False  # 方向是否改变

    def _load_tank_images(self):
        """
        根据坦克类型加载对应的图片
        """
        if self.kind == 1:
            self.enemy_x_0 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_1_0.png')).convert_alpha()
            self.enemy_x_3 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_1_3.png')).convert_alpha()
        elif self.kind == 2:
            self.enemy_x_0 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_2_0.png')).convert_alpha()
            self.enemy_x_3 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_2_3.png')).convert_alpha()
        elif self.kind == 3:
            self.enemy_x_0 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_3_1.png')).convert_alpha()
            self.enemy_x_3 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_3_0.png')).convert_alpha()
        elif self.kind == 4:
            self.enemy_x_0 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_4_0.png')).convert_alpha()
            self.enemy_x_3 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_4_3.png')).convert_alpha()
        
        # 加载重型坦克的特殊图片
        self.enemy_3_0 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_3_0.png')).convert_alpha()
        self.enemy_3_2 = pygame.image.load(os.path.join(IMAGE_DIR, 'enemy_3_2.png')).convert_alpha()

    def shoot(self):
        """
        发射子弹
        根据坦克当前方向设置子弹的初始位置和方向
        """
        self.bullet.life = True
        self.bullet.changeImage(self.dir_x, self.dir_y)
        
        # 根据方向设置子弹初始位置
        if self.dir_x == 0 and self.dir_y == -1:  # 向上
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top + 1
        elif self.dir_x == 0 and self.dir_y == 1:  # 向下
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom - 1
        elif self.dir_x == -1 and self.dir_y == 0:  # 向左
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.dir_x == 1 and self.dir_y == 0:  # 向右
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20

    def move(self, tankGroup, brickGroup, ironGroup):
        """
        移动坦克并处理碰撞
        
        参数:
            tankGroup: 坦克组
            brickGroup: 砖块组
            ironGroup: 铁块组
        """
        # 移动坦克
        self.rect = self.rect.move(self.speed * self.dir_x, self.speed * self.dir_y)
        
        # 更新坦克图片
        self._update_tank_image()
        
        # 处理碰撞
        self._handle_collision(tankGroup, brickGroup, ironGroup)

    def _update_tank_image(self):
        """
        根据移动方向更新坦克图片
        """
        if self.dir_x == 0 and self.dir_y == -1:  # 向上
            self.tank_R0 = self.tank.subsurface((0, 0), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 0), (48, 48))
        elif self.dir_x == 0 and self.dir_y == 1:  # 向下
            self.tank_R0 = self.tank.subsurface((0, 48), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 48), (48, 48))
        elif self.dir_x == -1 and self.dir_y == 0:  # 向左
            self.tank_R0 = self.tank.subsurface((0, 96), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 96), (48, 48))
        elif self.dir_x == 1 and self.dir_y == 0:  # 向右
            self.tank_R0 = self.tank.subsurface((0, 144), (48, 48))
            self.tank_R1 = self.tank.subsurface((48, 144), (48, 48))

    def _handle_collision(self, tankGroup, brickGroup, ironGroup):
        """
        处理坦克的碰撞
        
        参数:
            tankGroup: 坦克组
            brickGroup: 砖块组
            ironGroup: 铁块组
        """
        # 处理地图边界碰撞
        if self.rect.top < 3:  # 上边界
            self.rect = self.rect.move(0, self.speed)
            self._change_direction()
        elif self.rect.bottom > 630 - 3:  # 下边界
            self.rect = self.rect.move(0, -self.speed)
            self._change_direction()
        elif self.rect.left < 3:  # 左边界
            self.rect = self.rect.move(self.speed, 0)
            self._change_direction()
        elif self.rect.right > 630 - 3:  # 右边界
            self.rect = self.rect.move(-self.speed, 0)
            self._change_direction()
            
        # 处理与其他物体的碰撞
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None) \
            or pygame.sprite.spritecollide(self, tankGroup, False, None):
            self.rect = self.rect.move(-self.speed * self.dir_x, -self.speed * self.dir_y)
            self._change_direction()

    def _change_direction(self):
        """
        随机改变坦克的移动方向
        """
        self.dir_x, self.dir_y = random.choice(([0,1],[0,-1],[1,0],[-1,0]))
