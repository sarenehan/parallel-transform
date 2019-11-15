# parallel-transform
A implementation of asynchronous multiprocessing with progress logging.

# Installation
```bash
pip install parallel-transform
```

# Functions:
transform_list_parallel(
        list_to_transform,
        transform_func,
        *transform_args,
        verbose=True,
        processes=-1,
        min_log_frequency=1000,
        logger=None,
        log_func='info')

The elements in `list_to_transform` will be transformed based on the `transform_func` function, with the list element as the first arg, and `*transform_args` as the remaining args. If verbose is set to true, the progress every 5% or `min_log_frequency` processes will be logged, whichever is less. An optional logger can be passed; if no logger is passed, the logs will go to std out.

The order of the list_to_transform is maintained.
