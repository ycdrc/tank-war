# -*- coding: utf-8 -*-
"""
坦克大战游戏主模块
实现了游戏的主要逻辑，包括：
1. 游戏初始化
2. 玩家控制
3. 敌方坦克AI
4. 碰撞检测
5. 道具系统
6. 游戏状态管理
"""

import pygame
import sys
import traceback
import os
import wall
import myTank
import enemyTank
import food

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'image')
MUSIC_DIR = os.path.join(BASE_DIR, 'music')

def main():
    """
    游戏主函数
    负责初始化游戏、加载资源、运行游戏主循环
    """
    # 初始化pygame
    pygame.init()
    pygame.mixer.init()
    
    # 设置游戏窗口
    resolution = 630, 630
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("坦克大战")
    
    # 加载游戏资源
    # 图片资源
    background_image = pygame.image.load(os.path.join(IMAGE_DIR, 'background.png'))
    home_image = pygame.image.load(os.path.join(IMAGE_DIR, 'home.png'))
    home_destroyed_image = pygame.image.load(os.path.join(IMAGE_DIR, 'home_destroyed.png'))
    appearance_image = pygame.image.load(os.path.join(IMAGE_DIR, 'appear.png')).convert_alpha()
    gameover_image = pygame.image.load(os.path.join(IMAGE_DIR, 'gameover.png')).convert_alpha()
    
    # 音效资源
    bang_sound = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'bang.wav'))
    bang_sound.set_volume(1)
    fire_sound = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'Gunfire.wav'))
    start_sound = pygame.mixer.Sound(os.path.join(MUSIC_DIR, 'start.wav'))
    start_sound.play()
    
    # 玩家选择界面
    try:
        # 尝试使用系统默认字体
        font = pygame.font.SysFont('SimHei', 48)
    except:
        # 如果失败则使用系统默认字体
        font = pygame.font.SysFont(None, 48)
    text1 = font.render("按9键选择单人模式", True, (255, 255, 255))
    text2 = font.render("按0键选择双人模式", True, (255, 255, 255))
    text_rect1 = text1.get_rect(center=(resolution[0]/2, resolution[1]/2 - 50))
    text_rect2 = text2.get_rect(center=(resolution[0]/2, resolution[1]/2 + 50))
    
    # 等待玩家选择
    player_selection = None
    while player_selection is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_9:  # 单人模式
                    player_selection = 1
                elif event.key == pygame.K_0:  # 双人模式
                    player_selection = 2
        
        # 绘制选择界面
        screen.fill((0, 0, 0))
        screen.blit(text1, text_rect1)
        screen.blit(text2, text_rect2)
        pygame.display.flip()
        pygame.time.delay(100)
    
    # 定义精灵组
    allTankGroup = pygame.sprite.Group()      # 所有坦克组
    mytankGroup = pygame.sprite.Group()       # 我方坦克组
    allEnemyGroup = pygame.sprite.Group()     # 所有敌方坦克组
    redEnemyGroup = pygame.sprite.Group()     # 红色敌方坦克组
    greenEnemyGroup = pygame.sprite.Group()   # 绿色敌方坦克组
    otherEnemyGroup = pygame.sprite.Group()   # 其他敌方坦克组
    enemyBulletGroup = pygame.sprite.Group()  # 敌方子弹组
    
    # 游戏状态变量
    game_over = False  # 游戏是否结束
    
    # 游戏控制变量
    delay = 100  # 动画延迟
    moving = 0   # 玩家1移动控制
    movdir = 0   # 玩家1移动方向
    moving2 = 0  # 玩家2移动控制
    movdir2 = 0  # 玩家2移动方向
    enemyCouldMove = True  # 敌方坦克是否可以移动
    switch_R1_R2_image = True  # 坦克动画切换
    homeSurvive = True  # 基地是否存活
    running_T1 = True   # 玩家1坦克动画状态
    running_T2 = True   # 玩家2坦克动画状态
    
    def reset_game():
        """
        重置游戏状态
        清空所有精灵组，重新初始化游戏对象
        """
        nonlocal allTankGroup, mytankGroup, allEnemyGroup, redEnemyGroup, greenEnemyGroup, otherEnemyGroup, enemyBulletGroup
        nonlocal myTank_T1, myTank_T2, bgMap, prop, enemyNumber, homeSurvive, game_over
        nonlocal moving, movdir, moving2, movdir2, running_T1, running_T2, delay, enemyCouldMove, switch_R1_R2_image
        
        # 清空所有精灵组
        allTankGroup.empty()
        mytankGroup.empty()
        allEnemyGroup.empty()
        redEnemyGroup.empty()
        greenEnemyGroup.empty()
        otherEnemyGroup.empty()
        enemyBulletGroup.empty()
        
        # 重置地图
        bgMap = wall.Map()
        
        # 重置食物/道具
        prop = food.Food()
        
        # 重置我方坦克
        myTank_T1 = myTank.MyTank(1)
        allTankGroup.add(myTank_T1)
        mytankGroup.add(myTank_T1)
        myTank_T2 = None  # 初始化myTank_T2为None
        if player_selection == 2:  # 双人模式才创建二号坦克
            myTank_T2 = myTank.MyTank(2)
            allTankGroup.add(myTank_T2)
            mytankGroup.add(myTank_T2)
            moving2 = 0  # 重置玩家2移动控制
            movdir2 = 0  # 重置玩家2移动方向
            running_T2 = True  # 重置玩家2坦克动画状态
        
        # 重置玩家1控制变量
        moving = 0  # 重置玩家1移动控制
        movdir = 0  # 重置玩家1移动方向
        running_T1 = True  # 重置玩家1坦克动画状态
        
        # 重置其他游戏变量
        delay = 100
        enemyCouldMove = True
        switch_R1_R2_image = True
        homeSurvive = True
        
        # 重置敌方坦克
        enemyNumber = 3
        for i in range(1, 4):
            enemy = enemyTank.EnemyTank(i)
            allTankGroup.add(enemy)
            allEnemyGroup.add(enemy)
            if enemy.isred:
                redEnemyGroup.add(enemy)
                continue
            if enemy.kind == 3:
                greenEnemyGroup.add(enemy)
                continue
            otherEnemyGroup.add(enemy)
            
        # 重置游戏状态
        game_over = False
    
    # 初始化游戏对象
    bgMap = wall.Map()  # 创建地图
    prop = food.Food()  # 创建食物/道具
    
    # 创建我方坦克
    myTank_T1 = myTank.MyTank(1)
    allTankGroup.add(myTank_T1)
    mytankGroup.add(myTank_T1)
    myTank_T2 = None  # 初始化myTank_T2为None
    if player_selection == 2:  # 双人模式才创建二号坦克
        myTank_T2 = myTank.MyTank(2)
        allTankGroup.add(myTank_T2)
        mytankGroup.add(myTank_T2)
        moving2 = 0  # 玩家2移动控制
        movdir2 = 0  # 玩家2移动方向
        running_T2 = True   # 玩家2坦克动画状态
    
    # 创建敌方坦克
    enemyNumber = 3
    for i in range(1, 4):
        enemy = enemyTank.EnemyTank(i)
        allTankGroup.add(enemy)
        allEnemyGroup.add(enemy)
        if enemy.isred:
            redEnemyGroup.add(enemy)
            continue
        if enemy.kind == 3:
            greenEnemyGroup.add(enemy)
            continue
        otherEnemyGroup.add(enemy)
    
    # 敌方坦克出现动画
    appearance = []
    appearance.append(appearance_image.subsurface((0, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((48, 0), (48, 48)))
    appearance.append(appearance_image.subsurface((96, 0), (48, 48)))
    
    # 自定义事件
    DELAYEVENT = pygame.constants.USEREVENT  # 创建敌方坦克延迟
    pygame.time.set_timer(DELAYEVENT, 200)
    
    ENEMYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 1  # 敌方子弹冷却
    pygame.time.set_timer(ENEMYBULLETNOTCOOLINGEVENT, 1000)
    
    MYBULLETNOTCOOLINGEVENT = pygame.constants.USEREVENT + 2  # 我方子弹冷却
    pygame.time.set_timer(MYBULLETNOTCOOLINGEVENT, 200)
    
    NOTMOVEEVENT = pygame.constants.USEREVENT + 3  # 敌方坦克静止
    pygame.time.set_timer(NOTMOVEEVENT, 8000)
    
    # 游戏主循环
    clock = pygame.time.Clock()
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 游戏结束后只处理退出和重置事件
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c and pygame.KMOD_CTRL:  # Ctrl+C退出
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_r:  # R键重置游戏
                        reset_game()
                continue
            
            # 我方子弹冷却事件
            if event.type == MYBULLETNOTCOOLINGEVENT:
                myTank_T1.bulletNotCooling = True
            
            # 敌方子弹冷却事件
            if event.type == ENEMYBULLETNOTCOOLINGEVENT:
                for each in allEnemyGroup:
                    each.bulletNotCooling = True
            
            # 敌方坦克静止事件
            if event.type == NOTMOVEEVENT:
                enemyCouldMove = True
            
            # 创建敌方坦克延迟
            if event.type == DELAYEVENT:
                if enemyNumber < 4:
                    enemy = enemyTank.EnemyTank()
                    if pygame.sprite.spritecollide(enemy, allTankGroup, False, None):
                        break
                    allEnemyGroup.add(enemy)
                    allTankGroup.add(enemy)
                    enemyNumber += 1
                    if enemy.isred:
                        redEnemyGroup.add(enemy)
                    elif enemy.kind == 3:
                        greenEnemyGroup.add(enemy)
                    else:
                        otherEnemyGroup.add(enemy)
                                
            # 键盘事件处理
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.KMOD_CTRL:  # Ctrl+C退出
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r and game_over:  # R键重置游戏
                    reset_game()
                if event.key == pygame.K_e:  # E键升级一号坦克
                    myTank_T1.levelUp()
                if event.key == pygame.K_q:  # Q键降级一号坦克
                    myTank_T1.levelDown()
                if event.key == pygame.K_3:  # 3键直接升到3级一号坦克
                    myTank_T1.levelUp()
                    myTank_T1.levelUp()
                    myTank_T1.level = 3
                if event.key == pygame.K_2:  # 2键切换一号坦克速度
                    if myTank_T1.speed == 3:
                        myTank_T1.speed = 6
                    else:
                        myTank_T1.speed = 3
                if event.key == pygame.K_1:  # 1键创建砖墙
                    for x, y in [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]:
                        bgMap.brick = wall.Brick()
                        bgMap.brick.rect.left, bgMap.brick.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.brickGroup.add(bgMap.brick)                
                if event.key == pygame.K_4:  # 4键创建铁墙
                    for x, y in [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]:
                        bgMap.iron = wall.Iron()
                        bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                        bgMap.ironGroup.add(bgMap.iron)                
                # 二号坦克控制
                if event.key == pygame.K_KP1:  # 小键盘1升级二号坦克
                    myTank_T2.levelUp()
                if event.key == pygame.K_KP2:  # 小键盘2降级二号坦克
                    myTank_T2.levelDown()
                if event.key == pygame.K_KP3:  # 小键盘3直接升到3级
                    myTank_T2.levelUp()
                    myTank_T2.levelUp()
                    myTank_T2.level = 3
                if event.key == pygame.K_KP4:  # 小键盘4切换二号坦克速度
                    if myTank_T2.speed == 3:
                        myTank_T2.speed = 6
                    else:
                        myTank_T2.speed = 3

        # 检查用户的键盘操作
        key_pressed = pygame.key.get_pressed()
        
        # 游戏结束后不处理移动和射击
        if not game_over:
            # 玩家一的移动操作
            if moving:
                moving -= 1
                if movdir == 0:  # 向上移动
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                if movdir == 1:  # 向下移动
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                if movdir == 2:  # 向左移动
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                if movdir == 3:  # 向右移动
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving += 1
                    allTankGroup.add(myTank_T1)
                    running_T1 = True
                
            if not moving:
                if key_pressed[pygame.K_w]:  # W键向上移动
                    moving = 7
                    movdir = 0
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                elif key_pressed[pygame.K_s]:  # S键向下移动
                    moving = 7
                    movdir = 1
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                elif key_pressed[pygame.K_a]:  # A键向左移动
                    moving = 7
                    movdir = 2
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                elif key_pressed[pygame.K_d]:  # D键向右移动
                    moving = 7
                    movdir = 3
                    running_T1 = True
                    allTankGroup.remove(myTank_T1)
                    if myTank_T1.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup):
                        moving = 0
                    allTankGroup.add(myTank_T1)
                
            if key_pressed[pygame.K_j]:  # J键发射子弹
                if not myTank_T1.bullet.life and myTank_T1.bulletNotCooling:
                    fire_sound.play()
                    myTank_T1.shoot()
                    myTank_T1.bulletNotCooling = False
                
            # 玩家二的移动操作（仅在双人模式下）
            if player_selection == 2 and myTank_T2 is not None:
                if moving2:
                    moving2 -= 1
                    if movdir2 == 0:  # 向上移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        running_T2 = True
                    if movdir2 == 1:  # 向下移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        running_T2 = True
                    if movdir2 == 2:  # 向左移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        running_T2 = True
                    if movdir2 == 3:  # 向右移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        running_T2 = True
                
                if not moving2:
                    if key_pressed[pygame.K_UP]:  # 上方向键向上移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveUp(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        moving2 = 7
                        movdir2 = 0
                        running_T2 = True
                    elif key_pressed[pygame.K_DOWN]:  # 下方向键向下移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveDown(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        moving2 = 7
                        movdir2 = 1
                        running_T2 = True
                    elif key_pressed[pygame.K_LEFT]:  # 左方向键向左移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveLeft(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        moving2 = 7
                        movdir2 = 2
                        running_T2 = True
                    elif key_pressed[pygame.K_RIGHT]:  # 右方向键向右移动
                        allTankGroup.remove(myTank_T2)
                        myTank_T2.moveRight(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                        allTankGroup.add(myTank_T2)
                        moving2 = 7
                        movdir2 = 3
                        running_T2 = True
                
                if key_pressed[pygame.K_KP0]:  # 数字键盘0键发射子弹
                    if myTank_T2 is not None and not myTank_T2.bullet.life:
                        myTank_T2.shoot()
            
            # 绘制游戏画面
            # 绘制背景
            screen.blit(background_image, (0, 0))
            
            # 绘制砖块
            for each in bgMap.brickGroup:
                screen.blit(each.image, each.rect)        
            
            # 绘制铁块
            for each in bgMap.ironGroup:
                screen.blit(each.image, each.rect)        
            
            # 绘制基地
            if homeSurvive:
                screen.blit(home_image, (3 + 12 * 24, 3 + 24 * 24))
            else:
                screen.blit(home_destroyed_image, (3 + 12 * 24, 3 + 24 * 24))
                
            # 绘制我方坦克1
            if not (delay % 5):
                switch_R1_R2_image = not switch_R1_R2_image
            if switch_R1_R2_image and running_T1:
                screen.blit(myTank_T1.tank_R0, (myTank_T1.rect.left, myTank_T1.rect.top))
                running_T1 = False
            else:
                screen.blit(myTank_T1.tank_R1, (myTank_T1.rect.left, myTank_T1.rect.top))
                
            # 绘制我方坦克2（仅在双人模式下）
            if player_selection == 2 and myTank_T2 is not None:
                if switch_R1_R2_image and running_T2:
                    screen.blit(myTank_T2.tank_R0, (myTank_T2.rect.left, myTank_T2.rect.top))
                    running_T2 = False
                else:
                    screen.blit(myTank_T2.tank_R1, (myTank_T2.rect.left, myTank_T2.rect.top))    
            
            # 绘制敌方坦克
            for each in allEnemyGroup:
                # 判断是否播放出现动画
                if each.flash:
                    # 绘制坦克动画
                    if switch_R1_R2_image:
                        screen.blit(each.tank_R0, (each.rect.left, each.rect.top))
                        if enemyCouldMove:
                            allTankGroup.remove(each)
                            each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                            allTankGroup.add(each)
                    else:
                        screen.blit(each.tank_R1, (each.rect.left, each.rect.top))
                        if enemyCouldMove:
                            allTankGroup.remove(each)
                            each.move(allTankGroup, bgMap.brickGroup, bgMap.ironGroup)
                            allTankGroup.add(each)                    
                else:
                    # 播放出现动画
                    if each.times > 0:
                        each.times -= 1
                        if each.times <= 10:
                            screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 20:
                            screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 30:
                            screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 40:
                            screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 50:
                            screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 60:
                            screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 70:
                            screen.blit(appearance[2], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 80:
                            screen.blit(appearance[1], (3 + each.x * 12 * 24, 3))
                        elif each.times <= 90:
                            screen.blit(appearance[0], (3 + each.x * 12 * 24, 3))
                    if each.times == 0:
                        each.flash = True
      
            # 绘制我方子弹1
            if myTank_T1.bullet.life:
                myTank_T1.bullet.move()    
                screen.blit(myTank_T1.bullet.bullet, myTank_T1.bullet.rect)
                
                # 子弹碰撞检测
                # 子弹与子弹碰撞
                for each in enemyBulletGroup:
                    if each.life:
                        if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                            myTank_T1.bullet.life = False
                            each.life = False
                            pygame.sprite.spritecollide(myTank_T1.bullet, enemyBulletGroup, True, None)
                            
                # 子弹与敌方坦克碰撞
                if pygame.sprite.spritecollide(myTank_T1.bullet, redEnemyGroup, True, None):
                    prop.change()
                    bang_sound.play()
                    enemyNumber -= 1
                    myTank_T1.bullet.life = False
                elif pygame.sprite.spritecollide(myTank_T1.bullet, greenEnemyGroup, False, None):
                    for each in greenEnemyGroup:
                        if pygame.sprite.collide_rect(myTank_T1.bullet, each):
                            if each.life == 1:
                                pygame.sprite.spritecollide(myTank_T1.bullet, greenEnemyGroup, True, None)
                                bang_sound.play()
                                enemyNumber -= 1
                            elif each.life == 2:
                                each.life -= 1
                                each.tank = each.enemy_3_0
                            elif each.life == 3:
                                each.life -= 1
                                each.tank = each.enemy_3_2
                    myTank_T1.bullet.life = False
                elif pygame.sprite.spritecollide(myTank_T1.bullet, otherEnemyGroup, True, None):
                    bang_sound.play()
                    enemyNumber -= 1
                    myTank_T1.bullet.life = False    
                    
                # 子弹与砖块碰撞
                if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.brickGroup, True, None):
                    myTank_T1.bullet.life = False
                    myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                    
                # 子弹与铁块碰撞
                if myTank_T1.bullet.strong:
                    if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, True, None):
                        myTank_T1.bullet.life = False
                        myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                else:    
                    if pygame.sprite.spritecollide(myTank_T1.bullet, bgMap.ironGroup, False, None):
                        myTank_T1.bullet.life = False
                        myTank_T1.bullet.rect.left, myTank_T1.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                        
                # 子弹与基地碰撞
                if homeSurvive and myTank_T1.bullet.rect.colliderect(pygame.Rect(3 + 12 * 24, 3 + 24 * 24, 48, 48)):
                    homeSurvive = False
                    myTank_T1.bullet.life = False
                    game_over = True
                    bang_sound.play()
            
            # 绘制我方子弹2（仅在双人模式下）
            if player_selection == 2 and myTank_T2 is not None and myTank_T2.bullet.life:
                myTank_T2.bullet.move()    
                screen.blit(myTank_T2.bullet.bullet, myTank_T2.bullet.rect)
                
                # 子弹碰撞检测
                # 子弹与敌方坦克碰撞
                if pygame.sprite.spritecollide(myTank_T2.bullet, allEnemyGroup, True, None):
                    bang_sound.play()
                    enemyNumber -= 1
                    myTank_T2.bullet.life = False
                    
                # 子弹与砖块碰撞
                if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.brickGroup, True, None):
                    myTank_T2.bullet.life = False
                    myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                    
                # 子弹与铁块碰撞
                if myTank_T2.bullet.strong:
                    if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, True, None):
                        myTank_T2.bullet.life = False
                        myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                else:    
                    if pygame.sprite.spritecollide(myTank_T2.bullet, bgMap.ironGroup, False, None):
                        myTank_T2.bullet.life = False
                        myTank_T2.bullet.rect.left, myTank_T2.bullet.rect.right = 3 + 12 * 24, 3 + 24 * 24
                            
                # 子弹与基地碰撞
                if homeSurvive and myTank_T2.bullet.rect.colliderect(pygame.Rect(3 + 12 * 24, 3 + 24 * 24, 48, 48)):
                    homeSurvive = False
                    myTank_T2.bullet.life = False
                    game_over = True
                    bang_sound.play()
            
            # 绘制敌人子弹
            for each in allEnemyGroup:
                # 如果子弹没有生命，则赋予子弹生命
                if not each.bullet.life and each.bulletNotCooling and enemyCouldMove:
                    enemyBulletGroup.remove(each.bullet)
                    each.shoot()
                    enemyBulletGroup.add(each.bullet)
                    each.bulletNotCooling = False
                    
                # 如果出现动画播放完毕且子弹存活，则绘制敌方子弹
                if each.flash:
                    if each.bullet.life:
                        # 如果敌人可以移动
                        if enemyCouldMove:
                            each.bullet.move()
                        screen.blit(each.bullet.bullet, each.bullet.rect)
                        
                        # 子弹碰撞检测
                        # 子弹与我方坦克碰撞
                        if pygame.sprite.collide_rect(each.bullet, myTank_T1):
                            bang_sound.play()
                            myTank_T1.rect.left, myTank_T1.rect.top = 3 + 8 * 24, 3 + 24 * 24 
                            each.bullet.life = False
                            moving = 0  # 重置移动控制参数
                            for i in range(myTank_T1.level+1):
                                myTank_T1.levelDown()
                        if player_selection == 2 and myTank_T2 is not None and pygame.sprite.collide_rect(each.bullet, myTank_T2):
                            bang_sound.play()
                            myTank_T2.rect.left, myTank_T2.rect.top = 3 + 16 * 24, 3 + 24 * 24 
                            each.bullet.life = False
                            
                        # 子弹与砖块碰撞
                        if pygame.sprite.spritecollide(each.bullet, bgMap.brickGroup, True, None):
                            each.bullet.life = False
                            
                        # 子弹与铁块碰撞
                        if each.bullet.strong:
                            if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, True, None):
                                each.bullet.life = False
                        else:    
                            if pygame.sprite.spritecollide(each.bullet, bgMap.ironGroup, False, None):
                                each.bullet.life = False
                                
                        # 子弹与基地碰撞
                        if homeSurvive and each.bullet.rect.colliderect(pygame.Rect(3 + 12 * 24, 3 + 24 * 24, 48, 48)):
                            homeSurvive = False
                            each.bullet.life = False
                            game_over = True
                            bang_sound.play()
             
            # 绘制食物/道具
            if prop.life:
                screen.blit(prop.image, prop.rect)
                # 我方坦克碰撞食物/道具
                if pygame.sprite.collide_rect(myTank_T1, prop):
                    if prop.kind == 1:  # 敌人全毁
                        for each in allEnemyGroup:
                            if pygame.sprite.spritecollide(each, allEnemyGroup, True, None):
                                bang_sound.play()
                                enemyNumber -= 1
                        prop.life = False
                    if prop.kind == 2:  # 敌人静止
                        enemyCouldMove = False
                        prop.life = False
                    if prop.kind == 3:  # 子弹增强
                        myTank_T1.bullet.strong = True
                        prop.life = False
                    if prop.kind == 4:  # 家得到保护
                        for x, y in [(11,23),(12,23),(13,23),(14,23),(11,24),(14,24),(11,25),(14,25)]:
                            bgMap.iron = wall.Iron()
                            bgMap.iron.rect.left, bgMap.iron.rect.top = 3 + x * 24, 3 + y * 24
                            bgMap.ironGroup.add(bgMap.iron)                
                        prop.life = False
                    if prop.kind == 5:  # 坦克无敌
                        prop.life = False
                        pass
                    if prop.kind == 6:  # 坦克升级
                        myTank_T1.levelUp()
                        prop.life = False
                    if prop.kind == 7:  # 坦克生命+1
                        myTank_T1.life += 1
                        prop.life = False
                    
            # 更新动画延迟
            delay -= 1
            if not delay:
                delay = 100    
        
        # 如果游戏结束，显示游戏结束图片
        if game_over:
            screen.blit(gameover_image, (resolution[0]/2 - gameover_image.get_width()/2, resolution[1]/2 - gameover_image.get_height()/2))
        
        # 更新显示
        pygame.display.flip()
        clock.tick(60)
    
if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()