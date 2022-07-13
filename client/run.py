from client import Application
from environs import Env


def run():
    env = Env()
    env.read_env()

    config = {
        'nickname': env.str('NICKNAME'),
        'url': env.str('URL', default='http://localhost:5000'),
        'dev': env.bool('DEV', default=False),
    }

    print('Initializing client...')

    Application(config.get('nickname'), config.get('url'), config.get('dev')).mainloop()


if __name__ == '__main__':
    run()
