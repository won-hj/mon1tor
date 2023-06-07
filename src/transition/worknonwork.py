#2013-2022 그래프 출력
from typing import Any
from FilePath import *


'''
    1. 언더 오버 따로따로
    2. 구분만 하고 한꺼번에 
'''
class WorkBase:
    def __getattribute__(self, __name: str) -> Any:
        pass
    
    def __sizeof__(self) -> int:
        pass


