import argparse
import datetime
import os
import sys
from argparse import ArgumentParser
from pathlib import Path
import re

from jinja2 import Environment, FileSystemLoader
from imgkit import from_file
from mutagen.easyid3 import EasyID3
import yaml

from tksugar import Generator

with open("config.yml", "r", encoding="utf-8") as f:
  config = yaml.safe_load(f)
  for n, v in config["path"].items():
    config["path"][n] = Path(os.path.expandvars(v))

TODAY = datetime.date.today()
MP3DIR = Path(config["path"]["basefolder"])
THEME_TEXT_DEF = config["themes"]["dailythemes"]
THEME_MODE_DEF = config["themes"]["modethemes"]

parser = ArgumentParser()
parser.add_argument("--theme", default=THEME_TEXT_DEF[TODAY.weekday()], help="テーマを変更する。" )
parser.add_argument("--title", help="タイトル。未指定時はファイルからの取得を試みる。")
parser.add_argument("--date", default=TODAY, type=lambda s: datetime.datetime.strptime(s, "%Y/%m/%d"), help="yyyy/mm/dd形式の日付。指定がない場合は今日の日付。")
parser.add_argument("--mode", help="モードの値。未指定時モード無し")
parser.add_argument("--gui", action="store_true" , help="GUIで各種パラメータを入力する。")
parser.add_argument("--file", help="この値は無視されます")
parser.add_argument("--bgm", help="この値は無視されます")
parser.add_argument("--outfile", default="0000out", help="出力ファイル(拡張子なし)。")
args = parser.parse_args()

fnpattern = "%Y-%m-%d"
if args.mode:
  fnpattern += f"_{args.mode}"
  if args.theme == THEME_TEXT_DEF[TODAY.weekday()]:
    args.theme = THEME_MODE_DEF[args.mode]
elif args.theme == THEME_TEXT_DEF[TODAY.weekday()] and args.date != TODAY:
  args.theme = THEME_TEXT_DEF[args.date.weekday()]

fnpattern += ".mp3"
mp3path = MP3DIR / args.date.strftime(fnpattern)
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
  man.vars["theme"].set(args.theme[(args.date.day - 1) // 7] if type(args.theme) is list else args.theme)
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
  'theme': args.theme[(args.date.day - 1) // 7] if type(args.theme) is list else args.theme,
  'title': args.title,
  'mode': args.mode
}
out = Path(__file__).parent / "html" / "out.html"
with open(out, mode="w", encoding="utf-8") as f:
  f.write(template.render(data))

w = 0
h = 0
with open(out.with_name("main.css"), mode="r", encoding="utf-8") as f:
  css = f.read()
  if (m := re.search(r"body[^}]*?width: (\d+)px", css, re.DOTALL)) != None:
    w = m[1]
  if (m := re.search(r"body[^}]*?height: (\d+)px", css, re.DOTALL)) != None:
    h = m[1]

if w == 0 or h == 0:
  raise Exception("Unknown Size!")

from_file(str(out), str(MP3DIR / f'{args.outfile}.png'), options={
  "width": w,
  "height": h,
  "enable-local-file-access": ""
})

