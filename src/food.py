# -*- coding: utf-8 -*-
"""
食物/道具类模块
定义了游戏中各种道具的属性和行为
道具类型：
1. 炸弹：消灭所有敌人
2. 时钟：使敌人静止
3. 枪：增强子弹威力
4. 铁：保护基地
5. 保护：坦克无敌
6. 星星：坦克升级
7. 坦克：增加生命
"""

import pygame
import random
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'image')

class Food(pygame.sprite.Sprite):
    """
    食物/道具类
    继承自pygame的Sprite类，用于处理游戏中的各种道具
    """
    def __init__(self):
        """
        初始化道具对象
        加载所有道具图片，随机选择一种道具类型
        """
        pygame.sprite.Sprite.__init__(self)
        
        # 加载所有道具图片
        self.food_boom = pygame.image.load(os.path.join(IMAGE_DIR, 'food_boom.png')).convert_alpha()
        self.food_clock = pygame.image.load(os.path.join(IMAGE_DIR, 'food_clock.png')).convert_alpha()
        self.food_gun = pygame.image.load(os.path.join(IMAGE_DIR, 'food_gun.png')).convert_alpha()
        self.food_iron = pygame.image.load(os.path.join(IMAGE_DIR, 'food_iron.png')).convert_alpha()
        self.food_protect = pygame.image.load(os.path.join(IMAGE_DIR, 'food_protect.png')).convert_alpha()
        self.food_star = pygame.image.load(os.path.join(IMAGE_DIR, 'food_star.png')).convert_alpha()
        self.food_tank = pygame.image.load(os.path.join(IMAGE_DIR, 'food_tank.png')).convert_alpha()

        # 随机选择道具类型
        self.kind = random.choice([1, 2, 3, 4, 5, 6, 7])
        self._update_image()
        
        # 设置道具位置和状态
        self.rect = self.image.get_rect()
        self.rect.left = self.rect.top = random.randint(100, 500)
        self.life = False
        
    def _update_image(self):
        """
        根据道具类型更新道具图片
        """
        if self.kind == 1:
            self.image = self.food_boom
        elif self.kind == 2:
            self.image = self.food_clock
        elif self.kind == 3:
            self.image = self.food_gun
        elif self.kind == 4:
            self.image = self.food_iron
        elif self.kind == 5:
            self.image = self.food_protect
        elif self.kind == 6:
            self.image = self.food_star
        elif self.kind == 7:
            self.image = self.food_tank
        
    def change(self):
        """
        改变道具类型和位置
        随机选择新的道具类型，更新图片，并随机设置新的位置
        """
        self.kind = random.choice([1, 2, 3, 4, 5, 6, 7])
        self._update_image()
        self.rect.left = self.rect.top = random.randint(100, 500)
        self.life = True

