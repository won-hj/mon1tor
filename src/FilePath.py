from configparser import ConfigParser

class path:
    def __init__(self) -> None:
        pass
        self.parser = ConfigParser()
        self.config = '../config/config.ini'
        self.parser.read(self.config, encoding='utf-8')

    #folder = {'birthover' : 1, 'birthunder' : 2, 'workover' : 3, 'workunder' : 4}
    folder = { 1 : 'birthover', 2 : 'birthunder', 3 : 'workover', 4 : 'workunder'}

    def get_parser(self):
        return self.parser

    def get_path(self, num):
        return self.parser.get('config', self.folder[num])


if __name__ == "__main__":
    #print(path.get_path())
    p = path()
    print(p.get_path(1))
