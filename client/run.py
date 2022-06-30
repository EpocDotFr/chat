import argparse


def run():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('nickname')
    arg_parser.add_argument('--url', default='http://localhost:5000')

    args = arg_parser.parse_args()

    print('Initializing client...')

if __name__ == '__main__':
    run()
