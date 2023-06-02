from configparser import ConfigParser

parser = ConfigParser()
config = '../config/config.ini'
parser.read(config, encoding='utf-8')

#folder = {'birthover' : 1, 'birthunder' : 2, 'workover' : 3, 'workunder' : 4}
folder = { 1 : 'birthover', 2 : 'birthunder', 3 : 'workover', 4 : 'workunder'}

def get_parser():
    return parser

def get_path(num):
    return parser.get('config', folder[num])

if __name__ == "__main__":
    print(get_path(1))
