# from base64 import encode
# from pprint import pprint
# import time
import PySimpleGUI as sg
from layout import LayoutGUI
import datetime
from threading import Thread
from discordBOT import BOT

from User import User
user = User()


def event_time():
    now = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%m:%S : "))
    return now


class TestThread():
    def __init__(self):
        self.bot = BOT()
        self.thread = Thread(target=self.loop_event)

    def start(self):
        self.active = True
        self.thread.start()

    def kill(self):
        self.bot.end()

    def loop_event(self):
        token = "NzcwMDY2MTY5NzkzMDg1NDcw.X5YKAg.IMn3xg-NLWxF9htDIssAlMSTAtk"
        self.bot.start(token)


def event_signup(username, pw1, pw2):
    if not pw1 == pw2:
        sg.popup(
            "パスワードが一致しません確認してください。",
            keep_on_top=True)
        return

    status = user.signup(username, pw1)

    if status == 1:
        sg.popup(
            "ユーザー登録に失敗しました",
            keep_on_top=True
        )
        return

    sg.popup(
        "正常に登録しました。",
        keep_on_top=True
    )
    return


def event_login(username, pw):
    data = user.login(username, pw)
    if len(data) < 1:
        sg.popup("ログインに失敗しました。")
        return 1

    return 0


window = LayoutGUI.make_login()
test00 = TestThread()

while True:
    window.keep_on_top_set()
    window.keep_on_top_clear()
    event, values = window.read()
    # print(window.__dict__)

    print(f"イベント:{event}/値:{values}")

    if event == sg.WIN_CLOSED:
        break

    if event == "ログイン":
        username = values["-UserName-"]
        pw = values["-PassWord-"]
        status = event_login(username, pw)

        if status == 0:
            window_main = LayoutGUI.make_main()
            window.close()
            window = window_main
            print(f"{event_time()}ようこそユーザー樣")

    if event == "サインアップ":
        window_signup = LayoutGUI.make_signup()
        window.close()
        window = window_signup

    if event == "戻る":
        window_login = LayoutGUI.make_login()
        window.close()
        window = window_login

    if event == "登録":
        pw1 = values["-PassWord1-"]
        pw2 = values["-PassWord2-"]
        username = values["-UserName-"]
        event_signup(username, pw1, pw2)

    if event == "画面サイズ":
        print(window.size)

    if event == "BOTを起動":
        test00.start()

    if event == "設定":
        test00.kill()

window.close()
