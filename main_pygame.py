import cfg
import sys
import time
import pygame
import be
import main_cli
from components import *
from tkinter import messagebox


def get_new_difficulty():
    '''获取难度'''
    rows,cols,mines=show_difficulty_dialog(cfg.GAME_MATRIX_SIZE[1],cfg.GAME_MATRIX_SIZE[0],cfg.NUM_MINES)
    cfg.GAME_MATRIX_SIZE = cols,rows
    cfg.NUM_MINES = mines
    cfg.SCREENSIZE = (cfg.GAME_MATRIX_SIZE[0] * cfg.GRIDSIZE + cfg.BORDERSIZE * 2, (cfg.GAME_MATRIX_SIZE[1] + 2) * cfg.GRIDSIZE + cfg.BORDERSIZE)
    return rows,cols,mines


def playmusic(path,loops=0):
    if not path:
        return
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops=loops)


def end(game:be.Game):
    if game.successful:
        # messagebox.showinfo("扫雷","游戏胜利！")
        pass
    else:
        playmusic(cfg.BGM_FAILED_PATH, -1)


def main():
    '''主函数'''
    # 游戏初始化
    get_new_difficulty()
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('扫雷')
    # 导入所有图片
    images = {}
    for key, value in cfg.IMAGE_PATHS.items():
        if key in ['face_fail', 'face_normal', 'face_success']:
            image = pygame.image.load(value)
            images[key] = pygame.transform.smoothscale(image, (int(cfg.GRIDSIZE*1.25), int(cfg.GRIDSIZE*1.25)))
        else:
            image = pygame.image.load(value).convert()
            images[key] = pygame.transform.smoothscale(image, (cfg.GRIDSIZE, cfg.GRIDSIZE))
    # 载入字体
    font = pygame.font.Font(cfg.FONT_PATH, cfg.FONT_SIZE)
    # 导入并播放背景音乐
    playmusic(cfg.BGM_PATH,-1)
    # 实例化游戏地图
    minesweeper_map = MinesweeperMap(cfg, images)
    minesweeper_map.game.end_callback=end
    minesweeper_map.game.update_callback=main_cli.render
    position = (cfg.SCREENSIZE[0] - int(cfg.GRIDSIZE * 1.25)) // 2, (cfg.GRIDSIZE * 2 - int(cfg.GRIDSIZE * 1.25)) // 2
    emoji_button = EmojiButton(images, position=position)
    textsize = font.size(str(cfg.NUM_MINES))
    remaining_mine_board = TextBoard(str(cfg.NUM_MINES), font, (cfg.SCREENSIZE[0]*.25-textsize[0]*.5, (cfg.GRIDSIZE*2-textsize[1])//2-2), cfg.RED)
    textsize = font.size('000')
    time_board = TextBoard('000', font, (cfg.SCREENSIZE[0]*.75-textsize[0]*.5, (cfg.GRIDSIZE*2-textsize[1])//2-2), cfg.RED)
    time_board.is_start = False
    # 游戏主循环
    clock = pygame.time.Clock()
    while True:
        screen.fill(cfg.BACKGROUND_COLOR)
        # --按键检测
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                mouse_pressed = pygame.mouse.get_pressed()
                minesweeper_map.update(mouse_pressed=mouse_pressed, mouse_pos=mouse_pos, type_='down')
            elif event.type == pygame.MOUSEBUTTONUP:
                minesweeper_map.update(type_='up')
                if emoji_button.rect.collidepoint(pygame.mouse.get_pos()):
                    # 新游戏
                    return
        # --更新时间显示
        if minesweeper_map.gaming:
            if not time_board.is_start:
                start_time = time.time()
                time_board.is_start = True
            time_board.update(str(int(time.time() - start_time)).zfill(3))
        # --更新剩余雷的数目显示
        remianing_mines = max(cfg.NUM_MINES - minesweeper_map.flags, 0)
        remaining_mine_board.update(str(remianing_mines).zfill(2))
        # --更新表情
        if minesweeper_map.game.failed:
            # 失败
            emoji_button.setstatus(status_code=1)
        elif minesweeper_map.game.successful:
            emoji_button.setstatus(status_code=2)
        # --显示当前的游戏状态地图
        minesweeper_map.draw(screen)
        emoji_button.draw(screen)
        remaining_mine_board.draw(screen)
        time_board.draw(screen)
        # --更新屏幕
        pygame.display.update()
        clock.tick(cfg.FPS)

'''run'''
if __name__ == '__main__':
    while True:
        main()
