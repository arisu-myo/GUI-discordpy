import hashlib
import os
import joblib
import PySimpleGUI as sg


class CipherMixin:
    def __init__(self):
        pass

    def encode_sha256(self, content):
        sha256 = hashlib.sha256(f"{content}".encode()).hexdigest()
        return str(sha256)

    def encode_md5(self, content):
        sha128 = hashlib.md5(f"{content}".encode()).hexdigest()
        return str(sha128)

    def create_filename(self, user: str, password: str):
        """ユーザー情報を含んだ文字列を返す"""
        content = f"{user}{password}"
        sha256 = self.encode_sha256(content)
        md5 = self.encode_md5(sha256)
        return str(md5)


class User(CipherMixin):

    def __init__(self):
        super().__init__()
        self.user_data = {}
        self.temp_data = {
            "cast": "さとうささら",
            "valume": 100,
            "tonescale": 0,
            "file_name": "output.wav",
            "file_path": os.getcwd(),
            "speed": 50,
            "emotions": "普通",
            "emotions_value": 100,
            "tone": 0,
            "alpha": 0,
            "remove_emoji": "",
            "remove_picture": "",
            "remove_command": "",
            "remove_mention": "",
            "remove_url": "",
            "token": ""
        }

    def login(self, user, password):
        file_name = self.create_filename(user, password)

        if not os.path.exists(f"./users/{file_name}"):
            return self.user_data

        self.user_data = self.load(file_name)
        return self.user_data

    def signup(self, user, password):
        file_name = self.create_filename(user, password)

        if os.path.exists(f"./users/{file_name}"):
            yn = sg.popup_yes_no(
                "すでに存在するユーザーです。\nユーザーを上書きしますか？",
                no_titlebar=True, keep_on_top=True,)

            if yn == "No":
                return 1

        success = self.seve(file_name, self.temp_data)
        return success

    def file_path(self, name):
        """要らないと思う・・・"""
        file_name = f"{name}.py"
        return file_name

    def load_data(self):
        pass

    def seve(self, file_name, obj):

        try:
            with open(f"./users/{file_name}", "wb")as file:
                joblib.dump(obj, file, compress=5)

            file.close()
        except Exception as error:
            print(f"{error}")
            return 1

        return 0

    def load(self, file_name):
        try:
            with open(f"./users/{file_name}", "rb")as file:
                load_data = joblib.load(file)
        except Exception as error:
            print(f"{error}")
            return {}

        return load_data


class UserData:
    def __init__(self, data: dict, user: str, pw: str):
        self.datas = data
        self.status = self.status()
        self.filename = User().create_filename(user, pw)

    def __getitem__(self, key):
        return self.datas[key]

    def set_data(self, key, value):
        self.datas[key] = value
        User().seve(self.filename, self.datas)

    def status(self):
        if len(self.datas) == 0:
            return 1
        elif len(self.datas) >= 1:
            return 0
        else:
            return -1


if __name__ == '__main__':

    token = "NzcwMDY2MTY5NzkzMDg1NDcw.GDdamN.3RmR8lenzAZxEujMPi_W6thaxY5SvEizHNDjHQ"
    user = User()
    data = user.login("", "")
    userdata = UserData(data, "", "")

    print(userdata["token"])
    userdata.set_data("token", token)
    print(userdata["token"])
