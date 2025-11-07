import sys
import pygame

# --- 关键修复 (针对您之前的 ALSA 声音报错) ---
# 必须在 import pygame 之前，告诉系统使用一个“假的”声音驱动
# 这样 pygame.init() 就不会因为找不到声卡而报错了
import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
# -----------------------------------------------


class Rocket:
    """管理火箭的类"""

    def __init__(self, game):
        """初始化火箭并设置其初始位置"""
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # 加载火箭图像并获取其外接矩形
        # 我们重用上一节的飞船图像，您也可以换成 "rocket.bmp"
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # *** 新增 ***: 将火箭放在屏幕中央
        # (之前的练习是 self.rect.midbottom)
        self.rect.center = self.screen_rect.center

        # --- 新增：用于平滑移动的设置 ---
        # 1. 速度设置
        self.speed = 1.5
        
        # 2. 在浮点数中存储火箭的精确位置
        #    因为 rect 的 x/y 只能存储整数，会导致精度丢失
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 3. 移动标志位 (Flags)
        #    当按键按下时，它们会变为 True，松开时变为 False
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """
        根据移动标志位更新火箭的位置。
        这是实现“边界检测”的核心。
        """
        # --- 关键：边界检测 ---
        
        # 检查向右移动，并且 (and) 火箭的右边缘没有超过屏幕的右边缘
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.speed
            
        # 检查向左移动，并且 (and) 火箭的左边缘大于 0 (屏幕左边缘)
        if self.moving_left and self.rect.left > 0:
            self.x -= self.speed
            
        # 检查向下移动，并且 (and) 火箭的下边缘没有超过屏幕的下边缘
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.speed
            
        # 检查向上移动，并且 (and) 火箭的上边缘大于 0 (屏幕上边缘)
        if self.moving_up and self.rect.top > 0:
            self.y -= self.speed

        # --- 更新 ---
        # 用浮点数更新 rect 的整数位置
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制火箭"""
        self.screen.blit(self.image, self.rect)


class RocketGame:
    """管理游戏资源和行为的主类"""

    def __init__(self):
        """初始化游戏并创建资源"""
        pygame.init()
        
        # 设置屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height))
        pygame.display.set_caption("Rocket Control")

        self.bg_color = (230, 230, 230)  # 浅灰色背景

        # 创建火箭实例
        # 传递 self (也就是 RocketGame 实例) 给 Rocket
        self.rocket = Rocket(self)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 1. 监听事件
            self._check_events()
            
            # 2. 更新火箭状态 (调用火箭的 update)
            self.rocket.update()
            
            # 3. 重绘屏幕 (调用屏幕的 update)
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            # --- 关键：按下按键 (KEYDOWN) ---
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                
            # --- 关键：松开按键 (KEYUP) ---
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键按下"""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = True  # 按下时，将标志位设为 True
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = True
        elif event.key == pygame.K_UP:
            self.rocket.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """响应按键松开"""
        if event.key == pygame.K_RIGHT:
            self.rocket.moving_right = False  # 松开时，将标志位设为 False
        elif event.key == pygame.K_LEFT:
            self.rocket.moving_left = False
        elif event.key == pygame.K_UP:
            self.rocket.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.rocket.moving_down = False

    def _update_screen(self):
        """更新屏幕上的图像，并切换到新屏幕"""
        # 每次循环时都重绘背景色
        self.screen.fill(self.bg_color)
        
        # 在背景上绘制火箭
        self.rocket.blitme()
        
        # 让最近绘制的屏幕可见
        pygame.display.flip()


# --- 启动游戏 ---
if __name__ == '__main__':
    game = RocketGame()
    game.run_game()


