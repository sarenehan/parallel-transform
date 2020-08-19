import traceback
from multiprocessing import cpu_count, Pool


class TransformFunc(object):
    def __init__(self, transform_func, log_func):
        self.transform_func = transform_func
        self.log_func = log_func

    def __call__(self, idx, row, *args):
        try:
            return (idx, self.transform_func(row, *args))
        except Exception:
            self.log_func(traceback.format_exc())
            return (idx, None)


class Parallelizer(object):
    def __init__(
            self,
            list_to_transform,
            transform_func,
            processes=cpu_count(),
            verbose=True,
            min_log_frequency=1000,
            log_func=print,
            *args):
        self.log_func = log_func
        self.total_processes = 0
        self.min_log_frequency = min_log_frequency
        self.completed_processes = 0
        self.list_to_transform = list_to_transform
        self.args = args
        self.transform_func = TransformFunc(transform_func, log_func)
        self.results = []
        self.verbose = verbose
        self.processes = processes

    def add(self, pool, idx, row):
        pool.apply_async(
            func=self.transform_func,
            args=(idx, row, *self.args),
            callback=self.complete)

    def set_log_frequency(self):
        frequency = max(int(len(self.list_to_transform) / 20), 1)
        self.log_frequency = (
            self.min_log_frequency if frequency > self.min_log_frequency
            else frequency
        )

    def complete(self, result):
        self.results.append(result)
        self.completed_processes += 1
        if not self.completed_processes % self.log_frequency:
            percentage = self.completed_processes / self.total_processes
            percentage = '{:.1%}'.format(round(percentage, 2))
            if self.verbose:
                self.log_func('Progress: {} ({} of {})'.format(
                    percentage,
                    self.completed_processes,
                    self.total_processes))

    def run(self):
        self.total_processes = len(self.list_to_transform)
        self.set_log_frequency()
        with Pool(processes=self.processes) as pool:
            for idx, row in enumerate(self.list_to_transform):
                self.add(pool, idx, row)
            pool.close()
            pool.join()
        self.results.sort(key=lambda x: x[0])
        self.results = [result[1] for result in self.results]
        if self.verbose:
            self.log_func('Finished parallelizing')


def transform_list_parallel(
        list_to_transform,
        transform_func,
        *transform_args,
        verbose=True,
        processes=-1,
        min_log_frequency=1000,
        logger=None,
        log_func='info'):
    if logger is None:
        log_func = print
    else:
        log_func = getattr(logger, log_func)
    if cpu_count() == 1:
        return [
            transform_func(row, *transform_args)
            for row in list_to_transform
        ]
    if processes == -1:
        processes = cpu_count()
    paralellizer = Parallelizer(
        list_to_transform,
        transform_func,
        processes,
        verbose,
        min_log_frequency,
        log_func,
        *transform_args)
    paralellizer.run()
    return paralellizer.results
