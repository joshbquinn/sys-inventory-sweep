import platform
import windows_system as ws
import linux_system as ls


def check_system():

    if platform.system() == 'Windows':
        ws.main()
    elif platform.system() == 'Linux':
        ls.main()
    else:
        print("OS not identified")


def main():
    check_system()


if __name__ == '__main__':
    main()
