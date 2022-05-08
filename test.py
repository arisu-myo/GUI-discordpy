# from base64 import encode
# from pprint import pprint
# import time
import ctypes
import ctypes.wintypes
import time
import PySimpleGUI as sg
from layout import LayoutGUI
import datetime
from threading import Thread
import discordBOT
# from discordBOT import BOT
from User import User, UserData
user = User()


def GetLocation(TargetWindowTitle: str):
    TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
    Rectangle = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
    return (Rectangle.left, Rectangle.top, )  # Rectangle.right, Rectangle.bottom)


def event_time():
    now = str(datetime.datetime.now().strftime("%Y/%m/%d %H:%m:%S : "))
    return now


class SubThread():
    def __init__(self):
        self.event_count = 0
        self.end_flg = False

    def start(self, contents):
        self.thread = Thread(
            target=self.loop_event,
            args=(contents["token"],)
        )
        self.thread.start()

    def close(self):
        # discordBOT.end()
        discordBOT.end()
        print(f"{event_time()}終了中ですしばらくお待ちください...")
        while True:
            if self.end_flg:
                break

    def loop_event(self, token):
        discordBOT.start(token)
        print(f"{event_time()}内部クリーンの為ソフトを終了します...")
        time.sleep(1.5)
        self.end_flg = True


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
    userdata = UserData(data, username, pw)
    if userdata.status == 1 or userdata.status == -1:
        sg.popup("ログインできませんでした。")
        return userdata

    return userdata


window = LayoutGUI.make_login((-1132, 423))
st = SubThread()
ud = None

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
        status_obj = event_login(username, pw)

        if status_obj.status == 0:
            ud = status_obj
            location = GetLocation(window.Title)
            window_main = LayoutGUI.make_main(location)
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
        print(GetLocation(window.Title))

    if event == "BOTを起動":
        st.start(ud)

    if event == "終了":
        st.close()
        break


window.close()
