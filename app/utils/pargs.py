import argparse

parser = argparse.ArgumentParser(description='Parser para tener control sobre que fechas y rango horarios correr las api call.')
parser.add_argument('-d', '--dates', nargs='+', type=str)
parser.add_argument('-t', '--time', nargs='+', type=int)

def get_pargs():
    args = parser.parse_args()
    dates = args._get_kwargs()[0][1]
    times = args._get_kwargs()[1][1]
    return (dates, times)


