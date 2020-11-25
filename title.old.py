# 手書きしようとしてたときのもの。いちおうとっておきます。
from pathlib import Path
import datetime
import os

from PIL import Image, ImageDraw, ImageFont

SIZE = (750, 820) # 画像サイズ
BAR_RATIO = 4.0 # 上下バーの割合
TEXT_ADJAST_Y = 20 # 上下のテキストアジャスト
TEXT_ADJAST_X = 20 # 左右のテキストアジャスト
FONT_NAME = "keifont" # フォント
THEME_TEXT = {
  0: "プログラミング",
  1: "SBC.Web配信",
  2: "フリートーク",
  3: "きまぐれライブ",
  4: "今週一週間の予定",
  5: "SBC.について",
  6: "きまぐれライブ",
}

# カラー
COLOR_BASE = (255, 238, 223)
COLOR_SUB = (223, 240, 255)
COLOR_SUB2 = (240, 255, 223)

# 自動計算
ABOVE_FRAME = ((0, 0), (SIZE[0], SIZE[1] / BAR_RATIO))
BOTTOM_FRAME = ((0, SIZE[1] - SIZE[1] / BAR_RATIO), (SIZE[0], SIZE[1]))
DATE = datetime.date.today()

def draw_layout():
  draw.rectangle(ABOVE_FRAME, fill=COLOR_SUB)
  draw.line(((0, ABOVE_FRAME[1][1]), ABOVE_FRAME[1]), fill=(255, 255, 255), width=10)
  draw.rectangle(BOTTOM_FRAME, fill=COLOR_SUB2)
  draw.line(((0, BOTTOM_FRAME[0][1]), (BOTTOM_FRAME[1][0], BOTTOM_FRAME[0][1])), fill=(255, 255, 255), width=10)

def draw_daytitle(theme):
  t = "{0}曜日".format("月火水木金土日"[DATE.weekday()])
  dt= DATE.strftime('%Y/%m/%d')
  font = get_font(FONT_NAME, 60)
  w, h = draw.textsize(t, font=font)
  minfont = get_font(FONT_NAME, 20)
  mw, mh = draw.textsize(dt, font=minfont)
  lfont = get_font(FONT_NAME, 80)
  lw, lh = draw.textsize(theme, font=lfont)
  draw.text(
    (
      ABOVE_FRAME[0][0] + TEXT_ADJAST_X,
      ABOVE_FRAME[1][1] / 2 - h / 2 - mh - 10 + TEXT_ADJAST_Y),
    dt, font=minfont, fill=(0, 0, 0))
  draw.text(
    (
      ABOVE_FRAME[0][0] + TEXT_ADJAST_X,
      ABOVE_FRAME[1][1] / 2 - h / 2 + TEXT_ADJAST_Y),
    t, font=font, fill=(0, 0, 0))
  draw.text(
    (
      ABOVE_FRAME[0][0] + TEXT_ADJAST_X + w + 10,
      ABOVE_FRAME[1][1] / 2 - lh / 2 - 10 + TEXT_ADJAST_Y),
    theme, font=lfont, fill=(0, 0, 0))

def draw_title():
  pass

def draw_sitetitle():
  pass

def get_font(name, SIZE):
  datafont = Path(os.path.expandvars(f"%LOCALAPPDATA%\Microsoft\Windows\Fonts\{name}.ttf"))
  winfont = Path(os.path.expandvars(f"%windir%\Fonts\{name}.ttf"))
  if datafont.exists():
    return ImageFont.truetype(str(datafont), SIZE)
  elif winfont.exists():
    return ImageFont.truetype(str(winfont), SIZE)
  else:
    raise FileNotFoundError()

if __name__ == "__main__":
  img  = Image.new('RGB', SIZE, COLOR_BASE)
  draw = ImageDraw.Draw(img)

  draw_layout()
  draw_daytitle(THEME_TEXT[1])
  draw_title()
  draw_sitetitle()

  img.save("title.png")
