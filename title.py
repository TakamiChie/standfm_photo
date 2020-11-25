import argparse
import datetime
import os
from argparse import ArgumentParser
from pathlib import Path
import tkinter

from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
import chromedriver_binary
from mutagen.easyid3 import EasyID3

THEME_TEXT = {
  0: "プログラミング",
  1: "SBC.Web配信",
  2: "フリートーク",
  3: "きまぐれライブ",
  4: "今週一週間の予定",
  5: "SBC.について",
  6: "きまぐれライブ",
}
TODAY = datetime.date.today()
MP3DIR = Path(os.environ["OneDriveConsumer"]) / "stand.fm"

parser = ArgumentParser()
parser.add_argument("--theme", default=THEME_TEXT[TODAY.weekday()], help="テーマを変更する。" )
parser.add_argument("--title", help="タイトル。未指定時はファイルからの取得を試みる。")
parser.add_argument("--date", default=TODAY, type=lambda s: datetime.datetime.strptime(s, "%Y/%m/%d"), help="yyyy/mm/dd形式の日付。指定がない場合は今日の日付。")
args = parser.parse_args()

mp3path = MP3DIR / args.date.strftime("%Y-%m-%d.mp3")
title = "名称未設定"
if args.title:
  title = args.title
elif mp3path.exists():
  tags = EasyID3(str(mp3path))
  title = tags.get("title", [title]).pop()

env = Environment(loader=FileSystemLoader('html'))
template = env.get_template('base.html')
data = {
  'day' : args.date.strftime("%Y/%m/%d"),
  'week': "{0}曜日".format("月火水木金土日"[args.date.weekday()]),
  'theme': args.theme,
  'title': title
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
