import os

if __name__ == '__main__':
    os.system("pytest -s --alluredir=report --asyncio-mode=auto")
    os.system("allure serve report")
