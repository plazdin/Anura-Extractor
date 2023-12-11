from datetime import date, datetime

import pandas as pd


class Dates:

    start: str
    finish: str

    def __init__(self, start: str = None, finish: str = None):
        if start == None:
            start = date.today().strftime('%Y-%m-%d')
        self.start = start
        self.finish = finish if finish else start


    def get_dates(self) -> list:
        '''Returns a range of dates from INIT_DATE & END_DATE'''
        return([str(n).split(
            ' ', maxsplit=1)[0] for n in pd.date_range(
                self.start, self.finish, freq='D')])


class Times:
    
    init: int
    finish: int

    def __init__(self, init: int = None, finish: int = None):
        if init == None:
            init = datetime.now().hour - 1
        
        elif init == -1:
            init = 23
        
        self.init = init
        self.finish = finish if finish else init

    def _list(self):
        return self.__dict__.values()
        

def query_maker(times: Times, dates: Dates) -> list[dict]:
    '''
    Makes a list of queries for anura api.\n
    Params:
    -------
    - times: a list of ints or digits that represents hours.
    - dates: a list of dates in "%Y%m%d" format.
    '''
    queries = list()

    for date in dates.get_dates():
        for hour in range(times.init, times.finish + 1):
            strhour = str(hour).rjust(2, '0')
            queries.append({
                'startDate': f'{date} {strhour}:00:00',
                'endDate':f'{date} {strhour}:59:59.999'
                })
    
    return queries