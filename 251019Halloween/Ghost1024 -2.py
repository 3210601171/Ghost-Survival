import pygame
import sys
import random
import os
from enum import Enum

# 初始化pygame
pygame.init()

# 屏幕设置
SCREEN_WIDTH = 1980
SCREEN_HEIGHT = 1200
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ghost Survival")

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)

# 尺寸设置
GHOST_SIZE = 110  # 鬼魂尺寸
POLICE_SIZE = 110  # 警察尺寸
BOX_SIZE = 80  # 宝箱尺寸
COLLISION_RATIO = 0.8  # 碰撞体相对于图像尺寸的比例（稍微减小一点）

# 游戏状态枚举
class GameScreen(Enum):
    START = 1
    PLAYING = 2
    GAME_OVER = 3

# 时间状态枚举
class TimeState(Enum):
    MORNING = 1
    NIGHT = 2

# 鬼魂类
class Ghost:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.is_moving = False
        self.direction = "right"  # 默认方向
        
        # 加载鬼魂图像
        self.images_left = self.load_images("251019Halloween/image/Ghost/GhostLeft")
        self.images_right = self.load_images("251019Halloween/image/Ghost/GhostRight")
        self.current_images = self.images_right
        self.image_index = 0
        self.animation_timer = 0
        self.animation_delay = 100  # 毫秒
        
        # 创建碰撞矩形（比图像小一点点）
        collision_size = int(GHOST_SIZE * COLLISION_RATIO)
        self.rect = pygame.Rect(
            x + (GHOST_SIZE - collision_size) // 2,
            y + (GHOST_SIZE - collision_size) // 2,
            collision_size,
            collision_size
        )
        
    def load_images(self, folder_path):
        images = []
        if os.path.exists(folder_path):
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(folder_path, filename)
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (GHOST_SIZE, GHOST_SIZE))
                    images.append(img)
        return images
        
    def move(self, direction):
        self.is_moving = True
        self.direction = direction
        
        # 更新动画方向
        if direction == "left":
            self.current_images = self.images_left
        elif direction == "right":
            self.current_images = self.images_right
        # 上下方向保持上一个水平方向的动画
        
        if direction == "left":
            self.x -= self.speed
        elif direction == "right":
            self.x += self.speed
        elif direction == "up":
            self.y -= self.speed
        elif direction == "down":
            self.y += self.speed
            
        # 限制在屏幕内
        self.x = max(0, min(self.x, SCREEN_WIDTH - GHOST_SIZE))
        self.y = max(0, min(self.y, SCREEN_HEIGHT - GHOST_SIZE))
        
        # 更新碰撞矩形位置（保持居中）
        collision_size = int(GHOST_SIZE * COLLISION_RATIO)
        self.rect.x = self.x + (GHOST_SIZE - collision_size) // 2
        self.rect.y = self.y + (GHOST_SIZE - collision_size) // 2
        
    def stop_moving(self):
        self.is_moving = False
        
    def update_animation(self, dt):
        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= self.animation_delay:
                self.animation_timer = 0
                self.image_index = (self.image_index + 1) % len(self.current_images)
        
    def draw(self, screen):
        if self.current_images:
            screen.blit(self.current_images[self.image_index], (self.x, self.y))
        else:
            # 如果没有图片，使用默认图形
            if self.direction == "left":
                pygame.draw.rect(screen, BLUE, (self.x, self.y, GHOST_SIZE, GHOST_SIZE))
            elif self.direction == "right":
                pygame.draw.rect(screen, GREEN, (self.x, self.y, GHOST_SIZE, GHOST_SIZE))
            else:
                pygame.draw.rect(screen, BLUE, (self.x, self.y, GHOST_SIZE, GHOST_SIZE))

# 宝箱类
class TreasureBox:
    def __init__(self):
        # 加载宝箱图像
        self.image = self.load_image("251019Halloween/image/UI/Box.png")
        self.respawn()  # 初始生成宝箱
        self.timer = 0  # 宝箱存在计时器
        self.max_time = 5000  # 5秒后自动重置
        
    def load_image(self, file_path):
        if os.path.exists(file_path):
            try:
                img = pygame.image.load(file_path).convert_alpha()
                return pygame.transform.scale(img, (BOX_SIZE, BOX_SIZE))
            except pygame.error:
                print(f"Cannot load treasure box image: {file_path}")
                return None
        else:
            print(f"Treasure box image does not exist: {file_path}")
            return None
            
    def respawn(self):
        # 确保宝箱在屏幕内生成
        self.x = random.randint(50, SCREEN_WIDTH - BOX_SIZE - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - BOX_SIZE - 50)
        self.rect = pygame.Rect(self.x, self.y, BOX_SIZE, BOX_SIZE)
        self.timer = 0  # 重置计时器
        
    def update(self, dt):
        # 更新宝箱计时器
        self.timer += dt
        
        # 如果超过最大时间，重新生成宝箱
        if self.timer >= self.max_time:
            self.respawn()
        
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
            
            # 绘制宝箱剩余时间指示器
            time_left = max(0, self.max_time - self.timer)
            progress = time_left / self.max_time
            
            # 绘制背景条
            bar_width = BOX_SIZE
            bar_height = 8
            bar_x = self.x
            bar_y = self.y - 15
            
            pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
            
            # 绘制进度条
            progress_width = int(bar_width * progress)
            color = GREEN if progress > 0.5 else YELLOW if progress > 0.2 else RED
            pygame.draw.rect(screen, color, (bar_x, bar_y, progress_width, bar_height))

# 时间状态类
class TimeStateManager:
    def __init__(self):
        # 修改：初始状态改为夜晚
        self.state = TimeState.NIGHT
        self.durations = {
            TimeState.MORNING: 3000,  # 3秒
            TimeState.NIGHT: 8000     # 8秒
        }
        self.current_duration = 0
        self.acceleration_timer = 0
        self.transition_timer = 0
        self.is_transitioning = False
        self.transition_progress = 0
        self.blink_timer = 0
        self.blink_count = 0
        self.text_visible = True
        
        # 加载背景图片 - 直接加载图片文件
        self.background_morning = self.load_background("251019Halloween/image/Background/Morning.png")
        self.background_night = self.load_background("251019Halloween/image/Background/Night.png")
        
        # 创建表面用于透明度变化
        self.morning_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.background_morning:
            self.morning_surface.blit(self.background_morning, (0, 0))
        else:
            self.morning_surface.fill((200, 230, 255))
            
        self.night_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        if self.background_night:
            self.night_surface.blit(self.background_night, (0, 0))
        else:
            self.night_surface.fill((20, 20, 60))
    
    def load_background(self, file_path):
        """直接加载背景图片文件"""
        if os.path.exists(file_path):
            try:
                img = pygame.image.load(file_path).convert()
                return pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error:
                print(f"Cannot load background image: {file_path}")
                return None
        else:
            print(f"Background image does not exist: {file_path}")
            return None
        
    def update(self, dt):
        self.current_duration += dt
        self.acceleration_timer += dt
        
        # 每10秒加速一次
        if self.acceleration_timer >= 10000:
            self.acceleration_timer = 0
            # 缩短持续时间，但保持最小1秒
            for state in self.durations:
                self.durations[state] = max(1000, int(self.durations[state] * 0.9))
        
        # 检查是否需要切换状态
        if self.current_duration >= self.durations[self.state]:
            self.current_duration = 0
            self.is_transitioning = True
            self.transition_timer = 0
            self.transition_progress = 0
            self.blink_timer = 0
            self.blink_count = 0
            self.text_visible = True
            
        # 处理状态切换过渡
        if self.is_transitioning:
            self.transition_timer += dt
            
            # 处理文字闪烁
            self.blink_timer += dt
            if self.blink_timer >= 250:  # 每250毫秒闪烁一次
                self.blink_timer = 0
                self.text_visible = not self.text_visible
                if not self.text_visible:  # 计算闪烁次数（每次从可见到不可见算一次）
                    self.blink_count += 1
                    
            # 三次闪烁后完成过渡
            if self.blink_count >= 3:
                self.is_transitioning = False
                # 切换状态
                if self.state == TimeState.MORNING:
                    self.state = TimeState.NIGHT
                else:
                    self.state = TimeState.MORNING
    
    def draw(self, screen):
        # 绘制夜晚背景（始终在底层）
        if self.background_night:
            screen.blit(self.background_night, (0, 0))
        else:
            screen.fill((20, 20, 60))
            
        # 绘制白天背景（根据透明度覆盖在夜晚背景上）
        if self.state == TimeState.MORNING or self.is_transitioning:
            if self.is_transitioning and self.state == TimeState.MORNING:
                # 白天转夜晚，逐渐降低白天背景透明度
                alpha = int(255 * (1 - min(1.0, self.transition_timer / 1000)))
                self.morning_surface.set_alpha(alpha)
            elif self.is_transitioning and self.state == TimeState.NIGHT:
                # 夜晚转白天，逐渐增加白天背景透明度
                alpha = int(255 * min(1.0, self.transition_timer / 1000))
                self.morning_surface.set_alpha(alpha)
            else:
                # 非过渡期，白天背景完全显示
                self.morning_surface.set_alpha(255)
                
            screen.blit(self.morning_surface, (0, 0))
            
        # 绘制状态文字（在最顶层）
        if self.is_transitioning and not self.text_visible:
            pass  # 不绘制文字（实现闪烁效果）
        else:
            # 创建大字体
            font = pygame.font.SysFont(None, 72)  # 72号字体，比较大
            
            if self.state == TimeState.MORNING:
                state_text = font.render("MORNING", True, WHITE)
            else:
                state_text = font.render("NIGHT", True, WHITE)
                
            # 在右上角绘制状态文字
            screen.blit(state_text, (SCREEN_WIDTH - state_text.get_width() - 20, 20))

# 警察类
class Police:
    def __init__(self, direction, base_speed):
        self.direction = direction
        
        # 速度会随着游戏进行而加快
        self.speed = random.randint(base_speed, base_speed + 2)
        
        # 加载警察图像
        if direction == "left":
            self.images = self.load_images("251019Halloween/image/Police/PoliceLeft")
            self.x = SCREEN_WIDTH  # 从右侧进入
        else:  # right
            self.images = self.load_images("251019Halloween/image/Police/PoliceRight")
            self.x = -POLICE_SIZE  # 从左侧进入
            
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        
        # 创建碰撞矩形（比图像小一点点）
        collision_size = int(POLICE_SIZE * COLLISION_RATIO)
        self.rect = pygame.Rect(
            self.x + (POLICE_SIZE - collision_size) // 2,
            self.y + (POLICE_SIZE - collision_size) // 2,
            collision_size,
            collision_size
        )
        
        self.to_destroy = False
        self.image_index = 0
        self.animation_timer = 0
        self.animation_delay = 150  # 毫秒
        
    def load_images(self, folder_path):
        images = []
        if os.path.exists(folder_path):
            for filename in sorted(os.listdir(folder_path)):
                if filename.endswith(('.png', '.jpg', '.jpeg')):
                    img_path = os.path.join(folder_path, filename)
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (POLICE_SIZE, POLICE_SIZE))
                    images.append(img)
        return images
        
    def update(self):
        if self.direction == "left":
            self.x -= self.speed
        else:
            self.x += self.speed
            
        # 更新碰撞矩形位置（保持居中）
        collision_size = int(POLICE_SIZE * COLLISION_RATIO)
        self.rect.x = self.x + (POLICE_SIZE - collision_size) // 2
        self.rect.y = self.y + (POLICE_SIZE - collision_size) // 2
        
        # 更新动画
        self.animation_timer += 16  # 假设60FPS
        if self.animation_timer >= self.animation_delay:
            self.animation_timer = 0
            if self.images:
                self.image_index = (self.image_index + 1) % len(self.images)
        
        # 检查是否超出屏幕
        if self.x < -100 or self.x > SCREEN_WIDTH + 100:
            self.to_destroy = True
            
    def draw(self, screen):
        if self.images:
            screen.blit(self.images[self.image_index], (self.x, self.y))
        else:
            # 如果没有图片，使用默认图形
            pygame.draw.rect(screen, RED, (self.x, self.y, POLICE_SIZE, POLICE_SIZE))

# 游戏状态管理器
class GameStateManager:
    def __init__(self):
        self.game_over = False
        self.survival_time = 0
        self.score = 0  # 分数属性
        self.police_list = []
        self.treasure_box = TreasureBox()  # 宝箱
        self.last_spawn_time = 0
        self.fail_reason = ""
        self.police_base_speed = 2  # 警察基础速度，会随着游戏进行而增加
        self.speed_increase_timer = 0
        
    def spawn_police(self, current_time):
        # 只在夜晚生成警察
        if time_manager.state == TimeState.NIGHT:
            # 每2-3秒生成一次
            if current_time - self.last_spawn_time > random.randint(2000, 3000):
                self.last_spawn_time = current_time
                # 随机生成4-5个警察
                for _ in range(random.randint(4, 5)):
                    # 警察从两侧随机刷新
                    direction = random.choice(["left", "right"])
                    self.police_list.append(Police(direction, self.police_base_speed))
    
    def update_police(self):
        for police in self.police_list:
            police.update()
            
        # 移除超出屏幕的警察
        self.police_list = [p for p in self.police_list if not p.to_destroy]
    
    def update_survival_time(self, dt):
        # 只在夜晚累计生存时间和分数
        if time_manager.state == TimeState.NIGHT and not self.game_over:
            self.survival_time += dt / 1000  # 转换为秒
            # 每秒加1分
            self.score += dt / 1000
            
            # 增加警察速度的计时器
            self.speed_increase_timer += dt
            if self.speed_increase_timer >= 15000:  # 每15秒增加一次速度
                self.speed_increase_timer = 0
                self.police_base_speed += 1  # 增加基础速度
    
    def update_treasure_box(self, dt):
        # 更新宝箱状态
        self.treasure_box.update(dt)
    
    def check_fail_conditions(self, ghost):
        if self.game_over:
            return
            
        # 条件1: 白天移动
        if time_manager.state == TimeState.MORNING and ghost.is_moving:
            self.game_over = True
            self.fail_reason ="BE DISCOVERED"
            return
            
        # 条件2: 与警察碰撞
        for police in self.police_list:
            if ghost.rect.colliderect(police.rect):
                self.game_over = True
                self.fail_reason =  "YOU GET KILLED"
                return
    
    def check_treasure_collection(self, ghost):
        # 检查鬼魂是否收集到宝箱
        if ghost.rect.colliderect(self.treasure_box.rect):
            self.score += 5  # 收集宝箱加5分
            self.treasure_box.respawn()  # 立即生成新宝箱
    
    def draw(self, screen):
        # 绘制宝箱
        self.treasure_box.draw(screen)
        
        # 绘制警察
        for police in self.police_list:
            police.draw(screen)
            
        # 绘制生存时间和分数
        font = pygame.font.SysFont(None, 36)
        time_text = font.render(f"Survival: {int(self.survival_time)} sec", True, WHITE)
        score_text = font.render(f"Score: {int(self.score)}", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - 200, 100))
        screen.blit(score_text, (20, 20))  # 在左上角显示分数
        
        # 绘制游戏结束画面
        if self.game_over:
            # 半透明覆盖层
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            # 游戏结束文字
            font_large = pygame.font.SysFont(None, 72)
            font_small = pygame.font.SysFont(None, 48)
            
            game_over_text = font_large.render("GAME OVER", True, RED)
            reason_text = font_small.render(self.fail_reason, True, WHITE)
            score_final_text = font_small.render(f"Final Score: {int(self.score)}", True, GREEN)
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
            screen.blit(reason_text, (SCREEN_WIDTH//2 - reason_text.get_width()//2, SCREEN_HEIGHT//2))
            screen.blit(score_final_text, (SCREEN_WIDTH//2 - score_final_text.get_width()//2, SCREEN_HEIGHT//2 + 60))

# 开始界面 - 修改后的版本，背景透明度为70%
def draw_start_screen(screen, clicked):
    # 创建一个半透明覆盖层（70%透明度）
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(110) 
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    # 绘制游戏标题
    title_font = pygame.font.SysFont(None, 100)
    title_text = title_font.render("GHOST SURVIVAL", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//3))
    screen.blit(title_text, title_rect)
    
    # 绘制游戏介绍（使用较小的字体）
    intro_font = pygame.font.SysFont(None, 30)
    intro_lines = [
        "You are a ghost wandering in the city, surviving by following the day-night rules:",
        "you must remain still during the day and can only move freely at night,",
        "but be careful of the patrolling police. The day-night cycle will get",
        "faster and faster - the longer you survive, the higher your score.",
        "Treasure boxes allow you to gain extra points quickly."
    ]
    
    # 计算介绍文字的总高度，以便垂直居中
    intro_height = len(intro_lines) * 40  # 每行40像素高度
    intro_start_y = SCREEN_HEIGHT//2 - intro_height//2
    
    # 绘制每一行介绍文字，全部居中
    for i, line in enumerate(intro_lines):
        intro_text = intro_font.render(line, True, WHITE)
        intro_rect = intro_text.get_rect(center=(SCREEN_WIDTH//2, intro_start_y + i * 40))
        screen.blit(intro_text, intro_rect)
    
    # 创建大字体
    font = pygame.font.SysFont(None, 60)
    
    # 根据是否点击选择颜色
    color = GREEN if clicked else WHITE
    
    # 绘制开始按钮
    start_text = font.render("GAME START", True, color)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + intro_height//2 + 80))
    screen.blit(start_text, start_rect)
    
    # 绘制提示文字
    hint_font = pygame.font.SysFont(None, 36)
    hint_text = hint_font.render("Click anywhere to start", True, WHITE)
    hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, start_rect.bottom + 50))
    screen.blit(hint_text, hint_rect)

# 创建游戏对象
ghost = Ghost(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 5)
# 修改：游戏开始时为夜晚
time_manager = TimeStateManager()
game_manager = GameStateManager()

# 游戏主循环
clock = pygame.time.Clock()
running = True
current_screen = GameScreen.START
start_clicked = False
click_timer = 0

while running:
    # 计算时间增量
    dt = clock.tick(60)
    
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and current_screen == GameScreen.GAME_OVER:
                # 重新开始游戏
                ghost = Ghost(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 5)
                time_manager = TimeStateManager()
                game_manager = GameStateManager()
                current_screen = GameScreen.PLAYING
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 开始界面点击
            if current_screen == GameScreen.START:
                start_clicked = True
                click_timer = 0
    
    # 更新游戏状态
    if current_screen == GameScreen.START:
        # 开始界面
        if start_clicked:
            click_timer += dt
            # 显示绿色文字一段时间后进入游戏
            if click_timer >= 500:  # 500毫秒后进入游戏
                current_screen = GameScreen.PLAYING
                start_clicked = False
        
    elif current_screen == GameScreen.PLAYING:
        # 游戏进行中
        # 获取按键状态
        keys = pygame.key.get_pressed()
        ghost.stop_moving()
        
        if not game_manager.game_over:
            if keys[pygame.K_LEFT]:
                ghost.move("left")
            elif keys[pygame.K_RIGHT]:
                ghost.move("right")
            elif keys[pygame.K_UP]:
                ghost.move("up")
            elif keys[pygame.K_DOWN]:
                ghost.move("down")
        
        # 更新游戏状态
        if not game_manager.game_over:
            ghost.update_animation(dt)
            time_manager.update(dt)
            game_manager.spawn_police(pygame.time.get_ticks())
            game_manager.update_police()
            game_manager.update_survival_time(dt)
            game_manager.update_treasure_box(dt)  # 新增：更新宝箱状态
            game_manager.check_treasure_collection(ghost)
            game_manager.check_fail_conditions(ghost)
            
            # 检查游戏是否结束
            if game_manager.game_over:
                current_screen = GameScreen.GAME_OVER
    
    # 绘制
    if current_screen == GameScreen.START:
        # 绘制开始界面
        draw_start_screen(screen, start_clicked)
    elif current_screen == GameScreen.PLAYING:
        # 绘制游戏画面
        time_manager.draw(screen)
        ghost.draw(screen)
        game_manager.draw(screen)
    elif current_screen == GameScreen.GAME_OVER:
        # 绘制游戏结束画面
        time_manager.draw(screen)
        ghost.draw(screen)
        game_manager.draw(screen)
    
    # 更新显示
    pygame.display.flip()

# 退出游戏
pygame.quit()
sys.exit()