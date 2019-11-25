from proxypool.api import app
from proxypool.schedule import Schedule

def main():
    # 运行一个调度器
    s = Schedule()
    s.run()
    # 运行flask
    app.run()




if __name__ == '__main__':
    main()

