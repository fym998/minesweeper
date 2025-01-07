import random
from .mine import Mine
import be

'''扫雷地图'''


class MinesweeperMap():
    def __init__(self, cfg, images, **kwargs):
        self.cfg = cfg
        # 游戏状态
        self.game: be.Game = be.Game(
            cfg.GAME_MATRIX_SIZE[1], cfg.GAME_MATRIX_SIZE[0], cfg.NUM_MINES)
        self.mines_matrix = []
        for j in range(cfg.GAME_MATRIX_SIZE[1]):  # 16
            mines_line = []
            for i in range(cfg.GAME_MATRIX_SIZE[0]):  # 30
                position = i * cfg.GRIDSIZE + \
                    cfg.BORDERSIZE, (j + 2) * cfg.GRIDSIZE
                mines_line.append(
                    Mine(images=images, position=position, cell=self.game.get_cell(j, i)))
            self.mines_matrix.append(mines_line)

        # 记录鼠标按下时的位置和按的键
        self.mouse_pos = None
        self.mouse_pressed = None

    def draw(self, screen):
        '''画出当前的游戏状态图'''
        for row in self.mines_matrix:
            for item in row:
                item.draw(screen, self.game)

    @property
    def status_code(self):
        if self.game.ongoing:
            return 0
        elif self.game.ended:
            return 1
        elif self.game.not_started:
            return -1

    def update(self, mouse_pressed=None, mouse_pos=None, type_='down'):
        '''根据玩家的鼠标操作情况更新当前的游戏状态地图'''
        assert type_ in ['down', 'up']
        # 记录鼠标按下时的位置和按的键
        if type_ == 'down' and mouse_pos is not None and mouse_pressed is not None:
            self.mouse_pos = mouse_pos
            self.mouse_pressed = mouse_pressed
        # 鼠标点击的范围不在游戏地图内, 无响应
        if self.mouse_pos[0] < self.cfg.BORDERSIZE or self.mouse_pos[0] > self.cfg.SCREENSIZE[0] - self.cfg.BORDERSIZE or \
           self.mouse_pos[1] < self.cfg.GRIDSIZE * 2 or self.mouse_pos[1] > self.cfg.SCREENSIZE[1] - self.cfg.BORDERSIZE:
            return
        # 鼠标点击在游戏地图内, 代表开始游戏(即可以开始计时了)
        # 如果不是正在游戏中, 按鼠标是没有用的
        if self.game.ended:
            return
        # 鼠标位置转矩阵索引
        coord_x = int((self.mouse_pos[0] -
                   self.cfg.BORDERSIZE) // self.cfg.GRIDSIZE)
        coord_y = int(self.mouse_pos[1] // self.cfg.GRIDSIZE - 2)
        mine_clicked = self.mines_matrix[coord_y][coord_x]
        # 鼠标按下
        if type_ == 'down':
            if self.mouse_pressed[0]:
                self.mines_matrix[coord_y][coord_x].down()
                if self.mouse_pressed[2]:
                    # --鼠标左右键同时按下
                    for i,j in self.game.get_adjacent_coords(coord_y,coord_x):
                        self.mines_matrix[i][j].down()
        # 鼠标释放
        else:
            self.mines_matrix[coord_y][coord_x].up()
            # --鼠标左键
            if self.mouse_pressed[0] and not self.mouse_pressed[2]:
                self.game.lclick(coord_y,coord_x)
            # --鼠标右键
            elif self.mouse_pressed[2] and not self.mouse_pressed[0]:
                self.game.rclick(coord_y,coord_x)
            # --鼠标左右键同时按下
            elif self.mouse_pressed[0] and self.mouse_pressed[2]:
                self.game.lrclick(coord_y,coord_x)
                

    @property
    def gaming(self):
        '''是否正在游戏中'''
        return self.status_code == 0
    
    @property
    def flags(self):
        '''被标记为雷的雷数目'''
        return self.game.num_flags
    
    @property
    def openeds(self):
        '''已经打开的雷的数目'''
        return self.game.num_uncovered
