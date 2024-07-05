import pygame
import random

class Settings:
  """全設定を格納するクラス"""

  def __init__(self):
    self.maze_w = 15 # 迷路の列数
    self.maze_h = 11 # 迷路の行数
    self.tile_w = 32 # 1マスの大きさ

    # 色の設定
    self.black = (0, 0, 0)
    self.red = (255, 0, 0)
    self.white = (255,255,255)
    self.brown = (115, 66, 41)
    self.orange = (233,168, 38)
    self.maze_color = [self.white, self.brown, self.orange]

    self.hs = self.load_high_score()
    self.high_score = self.change_time(self.hs)

  def make_maze(self):
    """迷路を自動的に生成する"""
    self.px = 1 # プレイヤーのx座標
    self.py = 1 # プレイヤーのy座標
    self.course_index = 2# プレイヤーの向き（初期値：南）

    tbl = [[0,-1],[1,0],[0,1],[-1,0]]
    # 迷路を初期化
    self.maze = []
    for y in range(0, self.maze_h):
        row = []
        for x in range(0, self.maze_w):
            row.append(0)
        self.maze.append(row)

    # 周囲を壁で囲む
    for x in range(0, self.maze_w):
        self.maze[0][x] = 1
        self.maze[self.maze_h-1][x] = 1
    for y in range(0, self.maze_h):
        self.maze[y][0] = 1
        self.maze[y][self.maze_w-1] = 1

    # 棒倒し法で迷路を生成★
    for y in range(2, self.maze_h-2, 2):
        for x in range(2, self.maze_w-2, 2):
            if  y == 2:
                d = [0,1,2,3]
            else:
                d = [1,2,3]

            while True:
                r = random.choice(d)
                if self.maze[y+tbl[r][1]][x+tbl[r][0]] != 1:
                    break
                d.remove(r)

            self.maze[y][x] = 1
            self.maze[y+tbl[r][1]][x+tbl[r][0]] = 1

    # ゴールを右下に設定
    self.maze[self.maze_h-2][self.maze_w-2] = 2

    # スタート時間を保存
    self.start_time = pygame.time.get_ticks()


  def load_high_score(self): # ハイスコアを読み込む
    try:
      with open("high_score.txt", "r") as file:
        return int(file.read().strip())
    except:
      return 0


  def check_high_score(self): # ハイスコアの保存
    end_time = pygame.time.get_ticks() - self.start_time
    if end_time < self.hs or not self.hs:
      self.high_score = end_time
      with open("high_score.txt", "w") as file:
        file.write(str(end_time))
        return "ハイスコア更新！\n"
    else:
      return ""


  def change_time(self, s):
    """時間の表示を整える"""
    if s > 0:
      minutes = int(s // 60000)
      seconds = int((s % 60000) // 1000)
      milliseconds = int(s % 1000)

      return f"{minutes:02} : {seconds:02} : {milliseconds:03}"
    else:
      return "-"