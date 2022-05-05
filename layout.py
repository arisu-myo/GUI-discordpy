import PySimpleGUI as sg


# def layout_setting():
#     default_button = ("Arial", 10)
def soft_title():
    return "DisBOT(free) Ver 0.1.0"


class LayoutGUI:

    def make_login():
        # left = 10
        # right = 10
        # top = 100
        # bottom = 100
        button_obj = [
            [
                sg.Button(
                    "ログイン",
                ),
                sg.Button(
                    "サインアップ"
                )
            ]
        ]

        layout = [
            [sg.Text("ログインしてください。")],
            [sg.Text("ユーザーネーム:", pad=((0, 0), (15, 0)))],
            [sg.Input(key="-UserName-")],
            [sg.Text("パスワード:", pad=((0, 0), (10, 0)))],
            [sg.Input(key="-PassWord-", password_char="●")],
            [sg.Column(button_obj, justification="right", pad=((0, 0), (10, 0)))],
            [sg.Button("画面サイズ")]
        ]
        return sg.Window(
            soft_title(), layout, font=("Arial", 12),
            size=(380, 260), resizable=True, finalize=True)

    def make_signup():

        button_obj = [
            [
                sg.Button("登録"),
                sg.Button("戻る")
            ]
        ]

        layout = [
            [sg.Text("この画面はユーザーを登録する画面です")],
            [sg.Text("ユーザーネーム")],
            [sg.Input(key="-UserName-")],
            [sg.Text("パスワード")],
            [sg.Input(key="-PassWord1-", password_char="*")],
            [sg.Text("パスワード(確認)")],
            [sg.Input(key="-PassWord2-", password_char="*")],
            [sg.Column(
                button_obj,
                justification="right",
                pad=((0, 0), (10, 0))
            )]
        ]
        return sg.Window(
            soft_title(), layout, font=("Arial", 12),
            size=(300, 300), resizable=True, finalize=True)

    def make_main():
        layout = [
            [sg.Text("メインの画面のつもりです")],
            [sg.Output(
                size=(100, 15),
                background_color="#000",
                text_color="#008000"
            )],
            [
                sg.Button("設定", font=("Arial", 10)),
                sg.Button("BOTを起動", font=("Arial", 10))
            ]
        ]
        return sg.Window(
            soft_title(), layout, font=("Arial", 12),
            size=(640, 400), resizable=True, finalize=True
        )
