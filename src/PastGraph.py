from typing import Any
from src.transition import birthdeath 

#fp('config/birth_death/over2022')
class pastgraph:
    def __init__(self, mark) -> None:
        pass     #mark -> under/over; '\\under/over\\'
        self.bd = birthdeath.birthdeath('\\'.join(mark + '\\')) 
        print('\\'.join(mark + '\\'))
        
    def print(self):
        pass

    def get_plot(self, year):
        return self.bd.get_data(year)

        #return self.plot

        
        
        
    

if __name__ == "__main__":
    pass
        
