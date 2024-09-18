import time
import os
from player import Players
from file_utils import check_players_json, read_players_data

#报错处理
def error():
    print("请输入正确的选项！")
    input("按回车键返回")

if __name__ == "__main__":
    check_players_json()
    person = Players()

    players_data = read_players_data()
    if not players_data:
        print("请先注册！")
        input("按回车键返回")

    while True:
        os.system("cls")
        print("GameDemo  V1.0")
        print("1.登录")
        print("2.注册")
        print("0.退出")
        n = int(input("请输入操作选项："))

        match n:
            case 0:
                break
            case 1:
                if person is None:
                    print("请先注册！")
                    input("按回车键返回")
                    continue
                
                if person.Login():
                    while True:
                        os.system("cls")
                        print(f"欢迎您，{person.name}！")
                        print("1.开始游戏")
                        print("2.读取存档")
                        print("3.删除存档")
                        print("4.获取最新公告")
                        print("5.修改账户信息")
                        print("0.退出游戏")
                        n = int(input("请输入操作选项："))
                        match n:
                            case 0:
                                print("感谢您的使用！")
                                break
                            case 1:
                                os.system("cls")
                                print("Loading...")
                                time.sleep(2)
                                os.system("cls")
                                person.Start()
                            case 2:
                                os.system("cls")
                                print("Loading...")
                                time.sleep(2)
                                os.system("cls")
                                person.ReadSave()
                                os.system("cls")
                            case 3:
                                os.system("cls")
                                print("Loading...")
                                os.system("cls")
                                person.DeleteSave()
                                time.sleep(1)
                            case 4:
                                os.system("cls")
                                print("最新公告如下：")
                                time.sleep(3)
                                input("按回车键返回")
                                continue
                            case 5:
                                while True:
                                    os.system("cls")
                                    print("修改账户信息")
                                    print("1.修改用户名")
                                    print("2.修改密码")
                                    print("3.查看当前账户信息")
                                    print("0.返回")
                                    n = int(input("请输入操作选项："))
                                    match n:
                                        case 0:
                                            break
                                        case 1:
                                            person.ChangeName()
                                            time.sleep(1)
                                        case 2:
                                            person.ChangePassword()
                                            time.sleep(1)
                                        case 3:
                                            person.Check()
                                            input("按回车返回上一级")
                                            continue
                                        case _:
                                            error()
                            case _:
                                error()    

            case 2:
                    player = Players()
                    player.Register()
                    person = player
            case _:
                error()