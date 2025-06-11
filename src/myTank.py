# -*- coding: utf-8 -*-
"""
我方坦克类模块
定义了游戏中玩家控制的坦克的属性和行为
坦克等级：
0级：基础坦克
1级：增强子弹速度
2级：增强子弹威力
3级：最大威力
"""

import pygame
import bulletClass
import os

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 定义资源目录
IMAGE_DIR = os.path.join(BASE_DIR, 'image')

# 坦克图片路径
tank_T1_0 = os.path.join(IMAGE_DIR, 'tank_T1_0.png')
tank_T1_1 = os.path.join(IMAGE_DIR, 'tank_T1_1.png')
tank_T1_2 = os.path.join(IMAGE_DIR, 'tank_T1_2.png')
tank_T2_0 = os.path.join(IMAGE_DIR, 'tank_T2_0.png')
tank_T2_1 = os.path.join(IMAGE_DIR, 'tank_T2_1.png')
tank_T2_2 = os.path.join(IMAGE_DIR, 'tank_T2_2.png')

class MyTank(pygame.sprite.Sprite):
    """
    我方坦克类
    继承自pygame的Sprite类，用于处理玩家坦克的显示和移动
    """
    def __init__(self, playerNumber):
        """
        初始化我方坦克对象
        
        参数:
            playerNumber: 玩家编号（1或2）
        """
        pygame.sprite.Sprite.__init__(self)
        
        # 坦克基本属性
        self.life = True  # 坦克是否存活
        self.level = 0    # 坦克等级
        
        # 根据玩家编号加载对应的坦克图片
        if playerNumber == 1:
            self.tank_L0_image = pygame.image.load(tank_T1_0).convert_alpha()
            self.tank_L1_image = pygame.image.load(tank_T1_1).convert_alpha()
            self.tank_L2_image = pygame.image.load(tank_T1_2).convert_alpha()
        if playerNumber == 2:
            self.tank_L0_image = pygame.image.load(tank_T2_0).convert_alpha()
            self.tank_L1_image = pygame.image.load(tank_T2_1).convert_alpha()
            self.tank_L2_image = pygame.image.load(tank_T2_2).convert_alpha()
        
        # 设置初始坦克图片
        self.tank = self.tank_L0_image
        
        # 设置坦克移动图片
        self.tank_R0 = self.tank.subsurface((0, 0),(48, 48))
        self.tank_R1 = self.tank.subsurface((48, 0),(48, 48))
        self.rect = self.tank_R0.get_rect()
        
        # 设置坦克初始位置
        if playerNumber == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24 
        if playerNumber == 2:
            self.rect.left, self.rect.top = 3 + 24 * 16, 3 + 24 * 24 
        
        # 坦克移动相关属性
        self.speed = 3  # 移动速度
        self.dir_x, self.dir_y = 0, -1  # 移动方向
        self.life = 3  # 生命值
        self.bulletNotCooling = True  # 子弹冷却状态
        self.bullet = bulletClass.Bullet()  # 创建子弹对象
    
    def shoot(self):
        """
        发射子弹
        根据坦克当前方向设置子弹的初始位置和方向
        根据坦克等级设置子弹的属性
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
        
        # 根据等级设置子弹属性
        if self.level == 1:
            self.bullet.speed = 16
            self.bullet.strong = False
        if self.level == 2:
            self.bullet.speed = 16
            self.bullet.strong = True
        if self.level == 3:
            self.bullet.speed = 48
            self.bullet.strong = True
    
    def levelUp(self):
        """
        提升坦克等级
        更新坦克图片和子弹属性
        """
        if self.level < 2:
            self.level += 1
        if self.level == 0:
            self.tank = self.tank_L0_image
        if self.level == 1:
            self.tank = self.tank_L1_image
        if self.level == 2:
            self.tank = self.tank_L2_image
        if self.level == 3:
            self.tank = self.tank_L2_image
            
    def levelDown(self):
        """
        降低坦克等级
        更新坦克图片和子弹属性
        """
        if self.level > 0:
            self.level -= 1
        if self.level == 0:
            self.tank = self.tank_L0_image
            self.bullet.speed = 6
            self.bullet.strong = False
        if self.level == 1:
            self.tank = self.tank_L1_image
        if self.level == 2:
            self.tank = self.tank_L2_image
        
    def moveUp(self, tankGroup, brickGroup, ironGroup):
        """
        向上移动坦克
        
        参数:
            tankGroup: 坦克组
            brickGroup: 砖块组
            ironGroup: 铁块组
            
        返回:
            bool: 是否发生碰撞
        """
        self.rect = self.rect.move(self.speed * 0, self.speed * -1)
        self.tank_R0 = self.tank.subsurface((0, 0),(48, 48))
        self.tank_R1 = self.tank.subsurface((48, 0),(48, 48))
        self.dir_x, self.dir_y = 0, -1
        
        # 检查碰撞
        if self.rect.top < 3:  # 上边界
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):  # 与砖块或铁块碰撞
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):  # 与其他坦克碰撞
            self.rect = self.rect.move(self.speed * 0, self.speed * 1)
            return True
        return False

    def moveDown(self, tankGroup, brickGroup, ironGroup):
        """
        向下移动坦克
        
        参数:
            tankGroup: 坦克组
            brickGroup: 砖块组
            ironGroup: 铁块组
            
        返回:
            bool: 是否发生碰撞
        """
        self.rect = self.rect.move(self.speed * 0, self.speed * 1)
        self.tank_R0 = self.tank.subsurface((0, 48),(48, 48))
        self.tank_R1 = self.tank.subsurface((48, 48),(48, 48))
        self.dir_x, self.dir_y = 0, 1
        
        # 检查碰撞
        if self.rect.bottom > 630 - 3:  # 下边界
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):  # 与砖块或铁块碰撞
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):  # 与其他坦克碰撞
            self.rect = self.rect.move(self.speed * 0, self.speed * -1)
            return True
        return False

    def moveLeft(self, tankGroup, brickGroup, ironGroup):
        """
        向左移动坦克
        
        参数:
            tankGroup: 坦克组
            brickGroup: 砖块组
            ironGroup: 铁块组
            
        返回:
            bool: 是否发生碰撞
        """
        self.rect = self.rect.move(self.speed * -1, self.speed * 0)
        self.tank_R0 = self.tank.subsurface((0, 96),(48, 48))
        self.tank_R1 = self.tank.subsurface((48, 96),(48, 48))
        self.dir_x, self.dir_y = -1, 0
        
        # 检查碰撞
        if self.rect.left < 3:  # 左边界
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):  # 与砖块或铁块碰撞
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):  # 与其他坦克碰撞
            self.rect = self.rect.move(self.speed * 1, self.speed * 0)
            return True
        return False

    def moveRight(self, tankGroup, brickGroup, ironGroup):
        """
        向右移动坦克
        
        参数:
            tankGroup: 坦克组
            brickGroup: 砖块组
            ironGroup: 铁块组
            
        返回:
            bool: 是否发生碰撞
        """
        self.rect = self.rect.move(self.speed * 1, self.speed * 0)
        self.tank_R0 = self.tank.subsurface((0, 144),(48, 48))
        self.tank_R1 = self.tank.subsurface((48, 144),(48, 48))
        self.dir_x, self.dir_y = 1, 0
        
        # 检查碰撞
        if self.rect.right > 630 - 3:  # 右边界
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, brickGroup, False, None) \
            or pygame.sprite.spritecollide(self, ironGroup, False, None):  # 与砖块或铁块碰撞
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        if pygame.sprite.spritecollide(self, tankGroup, False, None):  # 与其他坦克碰撞
            self.rect = self.rect.move(self.speed * -1, self.speed * 0)
            return True
        return False