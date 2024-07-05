import pygame
from tkinter import Tk
from tkinter import messagebox
import accessible_output2.outputs.auto
import sys

class Move:
  """プレイヤーの移動を管理するクラス"""

  def __init__(self, main):
    self.course = ["北", "東", "南", "西"]
    self.settings = main.settings

    self.channel_w = pygame.mixer.Channel(0)
    self.channel_m = pygame.mixer.Channel(1)

    # Pygameの効果音オブジェクトを作成
    self.sound_aisle = pygame.mixer.Sound("audio/aisle.wav")
    self.sound_wall = pygame.mixer.Sound("audio/wall.wav")
    self.wind_sound = pygame.mixer.Sound("audio/wind.wav")

    self.reader = accessible_output2.outputs.auto.Auto()

  def check_key(self, key):
    """プレイヤーの移動を確認"""

    if key == pygame.K_ESCAPE: # 終了
      sys.exit()
    elif key == pygame.K_LEFT:
        self.settings.course_index = (self.settings.course_index + 1) % 4
    elif key == pygame.K_RIGHT:
        self.settings.course_index = (self.settings.course_index - 1 + 4) % 4
    elif key == pygame.K_DOWN:
        self.settings.course_index = (self.settings.course_index + 2) % 4
    elif key == pygame.K_UP:
        self.moving()   
    elif key == pygame.K_z:
      self.navigation()
    elif key == pygame.K_x:
      self.reader.speak(f"現在{self.course[self.settings.course_index]}向きです",interrupt=True)
    elif key == pygame.K_c:
      elapsed_time = pygame.time.get_ticks() - self.settings.start_time
      minutes = elapsed_time // 60000
      seconds = elapsed_time % 60000 // 1000
      milliseconds = elapsed_time % 1000
      self.reader.speak(f"現在、{minutes}分{seconds}秒{milliseconds}経過",interrupt=True)


    else:
        return -1

    self.play_Wind_sound()

  def moving(self):
    """プレイヤーの移動"""
    x, y = self.settings.px, self.settings.py
    if self.settings.course_index == 0: # 北
      y -= 1
    elif self.settings.course_index == 1: # 東
      x -= 1
    elif self.settings.course_index == 2: # 南
      y += 1
    elif self.settings.course_index == 3: # 西
      x += 1

    if self.settings.maze[y][x] == 2: # ゴールに到達したか判定
      message = self.settings.check_high_score()
      ret = messagebox.askyesno(f"{message}ゴール", "宝を見つけた\nもう一度遊ぶ？")
      if ret == False: sys.exit()
      self.settings.make_maze()                    
    elif self.settings.maze[y][x] == 1: # 壁
      self.channel_m.play(self.sound_wall)
    elif self.settings.maze[y][x] == 0: # 移動
      self.settings.px, self.settings.py = x, y
      self.channel_m.play(self.sound_aisle)


  def play_Wind_sound(self):
    """左右に通路がある場合には風の音声を再生"""
    # 方角を確認
    if self.settings.course_index == 0: # 北
      left_x = self.settings.px - 1
      left_y = self.settings.py
      right_x = self.settings.px + 1
      right_y = self.settings.py
    elif self.settings.course_index == 1: # 東
      left_x = self.settings.px
      left_y = self.settings.py + 1
      right_x = self.settings.px
      right_y = self.settings.py - 1
    elif self.settings.course_index == 2: # 南
      left_x = self.settings.px + 1
      left_y = self.settings.py
      right_x = self.settings.px - 1
      right_y = self.settings.py
    elif self.settings.course_index == 3: # 西
      left_x = self.settings.px
      left_y = self.settings.py - 1
      right_x = self.settings.px
      right_y = self.settings.py + 1

    right = 0.0
    left = 0.0
    # 通路があるか判定
    if self.settings.maze[right_y][right_x] == 0:
      right = 1.0
    if self.settings.maze[left_y][left_x] == 0:
      left = 1.0

    self.channel_w.set_volume(left, right) # スピーカーの音量値を設定

    if left == 0.0 and right == 0.0 and self.channel_w.get_busy():
      self.channel_w.stop()
    elif not self.channel_w.get_busy():
      self.channel_w.play(self.wind_sound, loops=-1)


  def navigation(self):
    """ゴールまでの距離をアナウンスする"""
    distance_x = self.settings.maze_w - self.settings.px # x軸上の距離
    distance_y = self.settings.maze_h - self.settings.py # y軸上の距離

    self.reader.speak(f"宝は 東に{distance_x}メートル。南に{distance_y}メートルのところにあります",interrupt=True)


