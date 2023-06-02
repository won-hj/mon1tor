#from configparser import ConfigParser
import sys
import configparser as c
import os

class path:
    def __init__(self, cwd) -> None:
        pass
        self.cwd = cwd
        try:
            self.parser = c. ConfigParser()
            self.config = os.getcwd() + cwd #'./../config/config.ini'
            self.parser.read(self.config, encoding='utf-8')

        except c. ConfigParser.NoSectionError:
            sys.stderr.write("Could not open %s\n" % self.settingsFilename)
            sys.stderr.write("Exiting...\n")
            sys.exit(1)

    #folder = {'birthover' : 1, 'birthunder' : 2, 'workover' : 3, 'workunder' : 4}
    folder = { 1 : 'birthover', 2 : 'birthunder', 3 : 'workover', 4 : 'workunder'}

    def get_parser(self):
        return self.parser
    
    def get_path(self,num):
        path = self.parser.get('config', self.folder[num])
        return path
    
    def get_configpath(self):
        return self.config

    def get_now(self):
        return os.getcwd() +':'+ self.cwd
    

if __name__ == "__main__":
    p = path('./../config/config.ini')
    for i in range(1, 5):
        print(p.get_path(i))

    import os
    print(os.getcwd()+'\n'+p.get_now())