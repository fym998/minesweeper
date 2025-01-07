import pygame
import be

'''雷'''


class Mine(pygame.sprite.Sprite):
    def __init__(self, images, position, cell: be.Cell):
        pygame.sprite.Sprite.__init__(self)
        self.cell: be.Cell = cell
        # 导入图片
        self.images = images
        self.image = self.images['covered']
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.downed = False

    def down(self):
        # self.downed = True
        pass

    def up(self):
        # self.downed = False
        pass

    def draw(self, screen, game: be.Game):
        '''画到屏幕上'''
        if not game.failed:
            if self.cell.covered:
                self.image = self.images['covered'] if not self.downed else self.images['down']
                # self.image = self.images['covered'] if not self.cell.is_mine else self.images['mine']
            elif self.cell.uncovered:
                self.image = self.images[self.cell.adjacent_mines]
            elif self.cell.flagged:
                self.image = self.images['flag']
            elif self.cell.suspected:
                self.image = self.images['suspected'] if not self.downed else self.images['down']
        else:
            if self.cell.covered:
                self.image = self.images['covered'] if not self.cell.is_mine else self.images['mine']
            elif self.cell.uncovered:
                self.image = self.images[self.cell.adjacent_mines]
            elif self.cell.flagged:
                self.image = self.images['flag'] if self.cell.is_mine else self.images["falsemine"]
            elif self.cell.suspected:
                self.image = self.images['suspected']
            elif self.cell.detonated:
                self.image = self.images['detonated']
        # 绑定图片到屏幕
        screen.blit(self.image, self.rect)
        self.downed = False
