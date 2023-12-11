from concurrent.futures import ThreadPoolExecutor
from datetime import time
from functools import wraps

from schemas.datetime import Times, Dates, query_maker
from schemas.pandanura import PandAnura
from utils import log, get_pargs, query_maker, bqo
from utils.requests.api_v1 import fetch


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result
    return timeit_wrapper


def anura_extract() -> None:

    # Gets date and time if args were passed
    d, t = get_pargs()

    times = Times(*t) if t else Times()
    dats = Dates(*d) if d else Dates()
    
    # Makes queries for the request
    queries = query_maker(times, dats)

    regs = []

    with ThreadPoolExecutor(max_workers=5) as exec:
        for result in exec.map(fetch, queries):
            regs += result

    if len(regs) == 0:
        log.info(
        f'No hay registros de llamadas en este periodo. Finalizando..\n{"-"*60}'
        )
        quit()
    
    anura_df = PandAnura(regs).data
    print(anura_df)


    log.debug('Empezando insert.')
    try:
        bqo.export(anura_df)
        log.info(
            f'{len(anura_df)} Filas insertadas correctamente. Finalizando..\n{"-"*60}')
    
    except Exception as err:
        log.critical(f'No se pudo completar el insert: {err}.\n{"-"*60}')   


if __name__ == '__main__':
    anura_extract()