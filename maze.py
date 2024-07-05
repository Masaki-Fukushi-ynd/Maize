import pygame
from tkinter import Tk
from tkinter import messagebox
import sys

from settings import Settings
from move import Move


class Maze:
  def __init__(self):
    pygame.init()
    self.settings = Settings()
    self.move = Move(self)

    pygame.display.set_caption("maze game")
    self.screen = pygame.display.set_mode((self.settings.tile_w * self.settings.maze_w, self.settings.tile_w * self.settings.maze_h))


    self.font = pygame.font.SysFont(None, 24) # フォントとサイズ

    self.player_img = pygame.image.load("point.png") # プレイヤーアイコン
    self.settings.make_maze()


  def main(self):
    while True:
      # ゲームのメインループ
      self._check_events()
      self._update_screen()

  def _check_events(self):
    """イベント処理"""
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        self.move.check_key(event.key)

  def _update_screen(self):
    """画面上の画像を更新し、新しい画面に切り替える"""
    self.screen.fill(self.settings.white)

    # 迷路を描画する
    for y in range(0, self.settings.maze_h):
      for x in range(0, self.settings.maze_w):
        v = self.settings.maze[y][x]
        xx = self.settings.tile_w * x
        yy = self.settings.tile_w * y
        # タイルの種類によって指定の色で塗りつぶす
        pygame.draw.rect(self.screen,
          self.settings.maze_color[v],
          (xx, yy, xx + self.settings.tile_w, yy + self.settings.tile_w))


    # プレイヤーアイコンの方向と位置を指定
    angle = self.settings.course_index * 90
    position = [(self.settings.px * self.settings.tile_w) + self.settings.tile_w/2, 
      (self.settings.py * self.settings.tile_w) + self.settings.tile_w/2]

    # プレイヤーアイコンの描画
    rotate_img = pygame.transform.rotate(self.player_img, angle)
    rect = rotate_img.get_rect(center=position)
    self.screen.blit(rotate_img, rect.topleft)

    # 経過時間を取得
    elapsed_time = self.settings.change_time(
      pygame.time.get_ticks() - self.settings.start_time)

    # テキストラベルの作成
    time_label = self.font.render(elapsed_time, True, (0, 0, 0))
    hs_label = self.font.render(self.settings.high_score, True, (0, 0, 0))


    # 画面に描画
    self.screen.blit(time_label, (10, 10))
    self.screen.blit(hs_label, (self.screen.get_width() - hs_label.get_width() -10 , 10))    

    pygame.display.update()


if __name__ == '__main__':
  # ゲームのインスタンスを作成し、ゲームを実行する
  maze_game = Maze()
  maze_game.main()
