import pygame
import random
import sys
#初始化
pygame.init()
# 定义游戏的基本属性
TITLE = '羊了个羊'
WIDTH = 600
HEIGHT = 720
FPS = 60
game_started = False
game_failed = False  # 游戏失败标志
countdown_time = 60  # 倒计时时间（秒），设置为480秒
time_left = countdown_time  # 剩余时间
#定义卡牌的相关属性
T_WIDTH = 60
T_HEIGHT = 66
#创建牌库和牌堆
tiles = []
Cardslot = pygame.Rect((80, 600), (T_WIDTH * 6, T_HEIGHT))
Cardslots = []

font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
#道具的创建
CLEAR_ITEM_IMAGE = pygame.image.load('picture/clear_item.png')  
CLEAR_ITEM_RECT = pygame.Rect((WIDTH - 200, 400), (100, 100))  
has_clear_item = True  # 代表玩家拥有清空道具的标志
# 加载背景和遮罩图像以及难度选择按钮
background = pygame.image.load('picture/back.png')
mask = pygame.image.load('picture/mask.png')
end = pygame.image.load('picture/end.png')
win = pygame.image.load('picture/win.png')
Modese_lection=pygame.image.load('picture/Mode_selection.png')
normal_button = pygame.image.load('picture/normal_button.png')
hard_button = pygame.image.load('picture/hard_button.png')
# 自定义牌类的一些基本属性
class CustomTile():
    def __init__(self, image, rect, tag, layer, visible):
        self.image = image 
        self.rect = rect
        self.tag = tag #标记
        self.layer = layer#层数
        self.visible = visible#是否可见
# 难度设置
DIFFICULTY = None
# 难度选择界面
def difficulty_select():
    global DIFFICULTY
    Modese_lection_rect = Modese_lection.get_rect(center=(WIDTH // 2, HEIGHT // 2 -150))
    normal_rect = normal_button.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    hard_rect = hard_button.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))

    DIFFICULTY = None  # 初始化难度为空字符串
    #绘制难度选择界面
    while DIFFICULTY not in ['normal', 'hard']:
        screen.blit(background, (0, 0))  
        screen.blit(Modese_lection, Modese_lection_rect)  
        screen.blit(normal_button, normal_rect)  
        screen.blit(hard_button, hard_rect)  
        pygame.display.update()  # 更新屏幕显示
        #难度选择
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if normal_rect.collidepoint(mouse_x, mouse_y):
                        DIFFICULTY = 'normal'
                    elif hard_rect.collidepoint(mouse_x, mouse_y):
                        DIFFICULTY = 'hard'
    return DIFFICULTY
#更新游戏状态
def update():
    global time_left, game_failed, game_started
    if game_started and not game_failed and not tiles:  # 如果游戏开始，没有失败，并且没有牌了（游戏成功）
        game_failed = True  # 设置游戏失败标志为True，这样时间就不会更新了
    if game_started and not game_failed:
        time_left -= 1 / 60
        if time_left <= 0:
            time_left = 0
            game_failed = True
# 游戏帧绘制函数
def draw():
    screen.blit(background, (0, 0))
    #将下层的牌遮挡起来实现分层消除
    for tile in tiles:
        screen.blit(tile.image, tile.rect)
        if tile.visible == 0:
            screen.blit(mask, tile.rect)
    #创建牌堆列表
    for i, tile in enumerate(Cardslots):
        tile.rect.left = Cardslot.x + i * T_WIDTH
        tile.rect.top = Cardslot.y
        screen.blit(tile.image, tile.rect)
    #游戏结果的绘制
    if len(Cardslots) >= 6:
        screen.blit(end, (53, 0))
    if game_failed:
        screen.blit(end, (53, 0))
    if not tiles:
        screen.blit(win, (53, 0))
    if has_clear_item:
        screen.blit(CLEAR_ITEM_IMAGE, CLEAR_ITEM_RECT)

    # 绘制倒计时
    time_text = f"Time Left: {int(time_left)}"
    text_surface = font.render(time_text, True, (255, 0, 0))  # 渲染文本
    text_rect = text_surface.get_rect(center=(120, 100))  # 获取文本的矩形区域
    screen.blit(text_surface, text_rect)  # 将渲染的文本绘制到屏幕上

    pygame.display.flip()

# 游戏主循环
def main():
    global game_started
    difficulty_select()  # 调用难度选择界面
    game_started = True  # 游戏开始
    ts = list(range(1, 6)) * 6
    random.shuffle(ts)
    n = 0
    for k in range(4):  # 4层
        row = 4 - k
        col = 4 - k
        for i in range(row):  # 获取每行的牌
            for j in range(col):#获取每列的牌
                t = ts[n]  # 获取所有的牌
                n += 1
                tile_image = pygame.image.load(f'picture/tile{t}.png')  # 加载图片
                tile_image = pygame.transform.scale(tile_image, (T_WIDTH, T_HEIGHT))
                tile_rect = tile_image.get_rect()
                #将牌置于牌库
                tile_rect.topleft = (200 + (k * 0.5 + j) * T_WIDTH, 100 + (k * 0.5 + i) * T_HEIGHT * 0.9)
                tile = CustomTile(tile_image, tile_rect, t, k, 1 if k == 3 else 0)
                tiles.append(tile)
    has_clear_item = True  # 玩家开始时拥有清空道具
    running = True
    while running:
        update()  # 更新游戏状态
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_down(event.pos)
        draw()
        clock.tick(FPS)
    pygame.quit()

# 游戏逻辑以及鼠标交互
def on_mouse_down(pos):
    global Cardslots, has_clear_item
    if len(Cardslots) >= 6 or not tiles:
        return
    #检测是否使用道具
    if has_clear_item and CLEAR_ITEM_RECT.collidepoint(pos):
        has_clear_item = False  # 消耗道具
        # 将卡槽里的牌放到牌堆的上方
        bottom_Cardslot_start_y = 516 - T_HEIGHT  # 牌堆的上方起始y坐标
        for i, tile in enumerate(Cardslots):
            tile.visible = 1  # 重置状态为可点击
            # 计算应该放置的位置（底部牌堆的上方）
            new_x = 190 + i * T_WIDTH
            new_y = bottom_Cardslot_start_y + (i // 7) * T_HEIGHT
            tile.rect.topleft = (new_x, new_y)
            tiles.append(tile)  # 加入到tiles列表（即未消除的牌库）
        Cardslots.clear()  # 清空卡槽
        return
    #检测牌是否位于顶部，如果是则将他从顶部移动到卡槽
    for tile in reversed(tiles):  
        if tile.visible == 1 and tile.rect.collidepoint(pos):
            tile.visible = 2
            tiles.remove(tile)
            Cardslots.append(tile)
            # 根据难度检查是否可以消除
            if DIFFICULTY == 'normal':
                # 普通模式下，需要两张相同且相邻的卡片
                if len(Cardslots) >= 2:
                    tiles1 = Cardslots[-2]
                    if len([t for t in Cardslots if t.tag == tile.tag]) >= 2 and tiles1.tag == tile.tag:
                        Cardslots.pop(-1)
                        Cardslots.pop(-1)
            elif DIFFICULTY == 'hard':
                # 困难模式下，需要三张相同且相邻的卡片
                if len(Cardslots) >= 3:
                    tiles2 = Cardslots[-2]
                    tiles3 = Cardslots[-3]
                    if len([t for t in Cardslots if t.tag == tile.tag]) >= 3 and tiles2.tag == tile.tag and tiles3.tag == tile.tag:#判断3张牌相同且相邻
                        Cardslots.pop(-1)
                        Cardslots.pop(-1)
                        Cardslots.pop(-1)
            for down in tiles:
                if down.layer == tile.layer - 1 and down.rect.colliderect(tile.rect):
                    for up in tiles:
                        if up.layer == down.layer + 1 and up.rect.colliderect(down.rect):
                            break
                    else:
                        down.visible = 1
            return

main()