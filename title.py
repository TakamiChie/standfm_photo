import argparse
import datetime
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
import chromedriver_binary
from mutagen.easyid3 import EasyID3

from tksugar import Generator

THEME_TEXT = {
  0: "プログラミング",
  1: "SBC.Web配信",
  2: "フリートーク",
  3: "きまぐれライブ",
  4: "今週の予定",
  6: "きまぐれライブ",
}
TODAY = datetime.date.today()
MP3DIR = Path(os.environ["OneDriveConsumer"]) / "stand.fm"

parser = ArgumentParser()
parser.add_argument("--theme", default=THEME_TEXT[TODAY.weekday()], help="テーマを変更する。" )
parser.add_argument("--title", help="タイトル。未指定時はファイルからの取得を試みる。")
parser.add_argument("--date", default=TODAY, type=lambda s: datetime.datetime.strptime(s, "%Y/%m/%d"), help="yyyy/mm/dd形式の日付。指定がない場合は今日の日付。")
parser.add_argument("--gui", action="store_true" , help="GUIで各種パラメータを入力する。")
args = parser.parse_args()

mp3path = MP3DIR / args.date.strftime("%Y-%m-%d.mp3")
title = "名称未設定"
if args.title:
  title = args.title
elif mp3path.exists():
  tags = EasyID3(str(mp3path))
  title = tags.get("title", [title]).pop()
args.title = title

if args.gui:
  gen = Generator(file="gui.yml")
  gen.add_modules("tkcalendar")
  ok = False
  def button(obj, tag):
    global ok
    if tag.tag["tag"] == "OK":
      args.theme = man.vars["theme"].get()
      args.title = man.vars["title"].get()
      args.date = man.widgets["date"].widget.get_date()
      ok = True
    obj.tk.quit()
  man = gen.get_manager(commandhandler=button)
  man.widgets["date"].widget.set_date(args.date)
  man.vars["theme"].set(args.theme)
  man.vars["title"].set(args.title)
  man.mainloop()
  man.window.update()
  if not ok:
    sys.exit()
env = Environment(loader=FileSystemLoader('html'))
template = env.get_template('base.html')
data = {
  'day' : args.date.strftime("%Y/%m/%d"),
  'week': "{0}曜日".format("月火水木金土日"[args.date.weekday()]),
  'theme': args.theme,
  'title': args.title
}
out = Path(__file__).parent / "html" / "out.html"
with open(out, mode="w", encoding="utf-8") as f:
  f.write(template.render(data))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument("--window-size=750,820")
driver = webdriver.Chrome(options=options)
driver.get('file:///' + str(out))
driver.save_screenshot(str(MP3DIR / 'out.png'))
driver.quit()
out.unlink()
