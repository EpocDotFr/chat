import argparse


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--host', default='localhost')
    arg_parser.add_argument('--port', type=int, default=5000)

    args = arg_parser.parse_args()

    print('Initializing server...')

if __name__ == '__main__':
    run()
