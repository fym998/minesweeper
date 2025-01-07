'''配置文件'''
import os


RES_ROOT="resources/"
IMAGE_ROOT=RES_ROOT+"MS-Texture/svg/"

'''图片素材路径'''
IMAGE_PATHS = {
    'down': (IMAGE_ROOT+'cells/WinmineXP/celldown.svg'),
    0: (IMAGE_ROOT+'cells/WinmineXP/celldown.svg'),
    1: (IMAGE_ROOT+'cells/WinmineXP/cell1.svg'),
    2: (IMAGE_ROOT+'cells/WinmineXP/cell2.svg'),
    3: (IMAGE_ROOT+'cells/WinmineXP/cell3.svg'),
    4: (IMAGE_ROOT+'cells/WinmineXP/cell4.svg'),
    5: (IMAGE_ROOT+'cells/WinmineXP/cell5.svg'),
    6: (IMAGE_ROOT+'cells/WinmineXP/cell6.svg'),
    7: (IMAGE_ROOT+'cells/WinmineXP/cell7.svg'),
    8: (IMAGE_ROOT+'cells/WinmineXP/cell8.svg'),
    'flag': (IMAGE_ROOT+'cells/WinmineXP/cellflag.svg'),
    'mine': (IMAGE_ROOT+'cells/WinmineXP/cellmine.svg'),
    'covered': (IMAGE_ROOT+'cells/WinmineXP/cellup.svg'),
    'suspected': (IMAGE_ROOT+'cells/WinmineXP/cellsuspected.svg'),
    'detonated': (IMAGE_ROOT+'cells/WinmineXP/blast.svg'),
    'falsemine': (IMAGE_ROOT+'cells/WinmineXP/falsemine.svg'),
    'face_fail': (IMAGE_ROOT+'faces/Winmine XP/lostface.svg'),
    'face_normal': (IMAGE_ROOT+'faces/Winmine XP/smileface.svg'),
    'face_success': (IMAGE_ROOT+'faces/Winmine XP/winface.svg'),
}
'''BGM路径'''
BGM_PATH = (RES_ROOT+'music/bgm.mp3')
BGM_FAILED_PATH = (RES_ROOT+'music/nande.mp3')
'''游戏相关参数'''
FPS = 40
GRIDSIZE = 64
NUM_MINES = 5
GAME_MATRIX_SIZE = (9, 9)
BORDERSIZE = GRIDSIZE / 8
SCREENSIZE = (GAME_MATRIX_SIZE[0] * GRIDSIZE + BORDERSIZE * 2, (GAME_MATRIX_SIZE[1] + 2) * GRIDSIZE + BORDERSIZE)
'''字体路径'''
FONT_PATH = (RES_ROOT+'font/digital-7-mono-3.ttf')
FONT_SIZE = int(GRIDSIZE * 1.25)
'''颜色'''
BACKGROUND_COLOR = (192, 192, 192)
RED = (200, 0, 0)