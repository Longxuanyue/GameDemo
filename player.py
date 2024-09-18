import re
import random
import bcrypt
import json
import time
import os

#父类：用户类
class Person:
    
    #构造函数：定义账号、密码（原码）、密码（哈希加密）、用户名
    def __init__(self):
        self.AccountNumber = ""
        self.OriginalPassword = ""
        self.HashPassword = ""
        self.name = ""

    #方法：邮箱账号判断（V1.0）
    #通过构建正则表达式进行对输入的邮箱账号判断格式是否正确
    #当前缺陷：只能判断格式，不能判断是否为存在的邮箱账号
    def isValidEmail(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None
    
    #方法：登录（V1.0）
    def Login(self):
        #账密输入
        inputAccountNumber = input("请输入账号：")
        inputPassword = input("请输入密码：")

        #获得到输入的账号和密码后，首先对密码进行哈希运算，得到哈希值
        #随后扫描resource/Players.json表中第一列是否存在匹配的AccountNumber，若匹配，则进行对比输入的密码哈希与储存的密码哈希
        with open("resource/Players.json", "r") as infile:
            players = json.load(infile)
            for player in players:
                accountNumber = player["AccountNumber"]
                hashed_password = player["HashPassword"]
                if accountNumber == inputAccountNumber:
                    #哈希验证
                    if bcrypt.checkpw(inputPassword.encode(), hashed_password.encode()):
                        self.AccountNumber = inputAccountNumber
                        self.OriginalPassword = inputPassword
                        self.HashPassword = hashed_password
                        self.name = player["name"]
                        self.LoadGame()
                        return True
                    else:
                        print("账号或密码错误！")
                        return False
        print("该账号未注册！")
        return False

    #方法：账密信息查看（返还账号和密码原码）
    def Check(self):
        print("账号：", self.AccountNumber)
        print("密码：", self.OriginalPassword)

    #方法：密码更改
    #通过对原密码的验证再进行密码更改，更改后的密码原码保存在Players类中，密码哈希加密保存在resource/Players.json中
    def ChangePassword(self):
        inputOriginalPassword = input("请输入原密码：")
        if not bcrypt.checkpw(inputOriginalPassword.encode(), self.HashPassword.encode()):
            print("原密码错误！")
            return

        newPassword = input("请输入新密码：")
        self.OriginalPassword = newPassword
        hashed_password = bcrypt.hashpw(newPassword.encode(), bcrypt.gensalt())
        self.HashPassword = hashed_password.decode()

        with open("resource/Players.json", "r") as infile:
            players = json.load(infile)
            for player in players:
                if player["AccountNumber"] == self.AccountNumber:
                    player["HashPassword"] = self.HashPassword
                    break

        with open("resource/Players.json", "w") as outfile:
            json.dump(players, outfile)

        print("密码修改成功！")

#子类：玩家类
#暂无新定义的属性
#待增加属性：存活剧情角色、剧情存档
class Players(Person):
    def __init__(self):
        super().__init__()
        self.game_save = {}
        self.characters = []

    #方法：用户名更改
    #将新输入的用户名代替对应账号的原有用户名
    def ChangeName(self):
        newName = input("请输入新的用户名：")
        self.name = newName

        with open("resource/Players.json", "r") as infile:
            players = json.load(infile)
            for player in players:
                if player["AccountNumber"] == self.AccountNumber:
                    player["name"] = self.name
                    break

        with open("resource/Players.json", "w") as outfile:
            json.dump(players, outfile)

        print("用户名修改成功！")

    #方法：注册
    #输入待注册的账号，并通过正则表达式进行判断是否符合邮箱格式。再通过resource/Players.json判断是否是已注册的账号
    #如果该账号未注册，则为它随机生成10位密码，并输入用户名
    #注册完毕后展示账户信息，并将其保存在resource/Players.json中（保存的是密码哈希计算结果）
    def Register(self):
        while True:
            email = input("请输入邮箱账号：")
            if self.isValidEmail(email):
                with open("resource/Players.json", "r") as infile:
                    players = json.load(infile)
                    for player in players:
                        if player["AccountNumber"] == email:
                            print("该账号已注册！")
                            break
                    else:
                        self.AccountNumber = email
                        break
            else:
                print("请输入正确的邮箱账号！")

        characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        randomPassword = "".join(random.choice(characters) for _ in range(10))
        self.OriginalPassword = randomPassword
        self.HashPassword = bcrypt.hashpw(randomPassword.encode(), bcrypt.gensalt()).decode()
        self.name = input("请输入用户名：")

        player = {
            "AccountNumber": self.AccountNumber,
            "HashPassword": self.HashPassword,
            "name": self.name
        }

        with open("resource/Players.json", "r") as infile:
            players = json.load(infile)
            players.append(player)

        with open("resource/Players.json", "w") as outfile:
            json.dump(players, outfile)

        print("注册成功！")
        print("账号：", self.AccountNumber)
        print("密码：", self.OriginalPassword)
        print("用户名：", self.name)

        input("按回车键返回")

    def Check(self):
        super().Check()
        print("用户名：", self.name)

    def ReadSave(self):
        filename = f"resource/data/{self.name}.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.game_save = json.load(file)
        if self.game_save:
            print("请选择存档点：")
            for index, save in self.game_save.items():
                if "chapter" in save and "line" in save:
                    chapter = save["chapter"]
                    line = save["line"]
                    print(f"{index}. 存档点 {chapter}章 {line}行")
                else:
                    print(f"{index}. 存档点 格式错误")
            n = input("请输入存档点的序号：")
            if n in self.game_save:
                selected_save = self.game_save[n]
                print("Loading...")
                time.sleep(1)
                print(f"读取存档点 第{selected_save['chapter']}章 {selected_save['line']}行")
                time.sleep(1)
                os.system("cls")
                self.display_story(selected_save['chapter'], selected_save['line'])
            else:
                print("无效的存档点序号！")
                return
        else:
            print("无存档点！")
            time.sleep(2)

    def Start(self):
        print("剧情章节目录：")
        print("1.时间海篇")
        print("2.煌焱篇")
        print("3.维多利亚篇")
        print("4.极北之地篇")
        print("5.南方联盟篇")
        print("6.万灵域篇")
        print("7.瑞兽系列外传")
        print("---  New Chapters waiting to be updated...  ---")
        print("0.退出")
        chapter = int(input("请输入章节号："))
        print("Loading...")
        time.sleep(2)
        print(f"开始剧情：第{chapter}章")
        time.sleep(1)
        os.system("cls")

        match chapter:
            case 0:
                print("退出游戏")
                return
            case 1:
                self.display_story(chapter,1)

    def display_story(self, chapter, line):
        file_name = f"word/第{chapter}章.txt"
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='gb18030', errors='ignore') as f:
                lines = f.readlines()
                line_count = len(lines)
                if line > line_count:
                    line = 0
                for i in range(line-1, line_count):
                    if i != line:
                        os.system("cls")
                    line_text = lines[i].replace('{person.name}', self.name)
                    print(line_text.strip())
                    line += 1
                    if i == line_count - 1:
                        input("剧情已结束，按回车键返回章节目录")
                        break
                    choice = input("回车：继续    s：存档    q：退出\n")
                    if choice == "s":
                        self.save_save_point(chapter, i + 1)
                        print("存档成功！")
                        input("按回车键继续")
                    elif choice == "q":
                        break
                    os.system("cls")
        else:
            print(f"The file {file_name} does not exist.")


    def get_save_point(self,chapter):
        # 从游戏存档中获取保存的存档点
        if chapter in self.game_save:
            return self.game_save[chapter]['line']
        else:
            return 0

    def save_save_point(self, chapter, line):
        save_point = {"chapter": chapter, "line": line}
        index = str(len(self.game_save) + 1)
        self.game_save[index] = save_point

        filename = f"resource/data/{self.name}.json"
        with open(filename, 'w') as file:
            json.dump(self.game_save, file)

    def DeleteSave(self):
        filename = f"resource/data/{self.name}.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                self.game_save = json.load(file)
        if not self.game_save:
            print("没有存档点")
            return
        
        if self.game_save:
            print("请选择要删除的存档点：")
            for index, save in self.game_save.items():
                chapter = save['chapter']
                line = save['line']
                print(f"{index}. 存档点 第{chapter}章 第{line}行")
            n = input("请输入要删除的存档点的序号：")
            if n in self.game_save:
                delete_confirm = input("确定要删除该存档点吗？(Y/N)：")
                if delete_confirm.lower() == "y":
                    deleted_save = self.game_save.pop(n)
                    with open(filename, 'w') as file:
                        json.dump(self.game_save, file)
                    print("存档点删除成功！")

                    new_game_save = {}
                    for index, save in enumerate(self.game_save.values(), start=1):
                        new_game_save[str(index)] = save
                    self.game_save = new_game_save
                else:
                    print("取消删除存档点！")
            else:
                print("无效的存档点序号！")
                return
        else:
            print("无存档点！")

    def SaveGame(self, chapter, line):  
        filename = f"resource/data/{self.name}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                self.game_save = json.load(file)
        else:
            self.game_save = {}

        max_index = max([int(index) for index in self.game_save.keys()]) if self.game_save else 0
        new_index = str(max_index + 1)
        new_save = {'chapter': chapter, 'line': line}
        self.game_save[new_index] = new_save
        
        with open(filename, 'w') as file:
            json.dump(self.game_save, file)

    def LoadGame(self):
        # 加载游戏存档文件
        filename = f"resource/data/{self.name}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                self.game_save = json.load(file)