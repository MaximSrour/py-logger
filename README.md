# Python Logger

This is a simple logger for python. It was created because I was writing code on a plane and didn't know 'logging' was a standard library. It's not as good as the standard library, but it's good enough for me. The reason this still exists is because I may as well learn how to make a python package.

This has not be uploaded to PyPI, but it can be installed using pip:

```bash
pip install git+https://github.com/MaximSrour/logger.git#egg=logger
```

## Usage

```python
from logger import Logger

if __name__ == '__main__':
    logger = Logger.init()

Logger.log_info("Something happened")
```

The reason for the main code to initialise the logger is so that any other packages that use the logger will save their logs to the same file. This way, running your main program will cause all logs to be saved into the same file, whereas if you are testing a package, the logs will be saved to a different file.

It is still a work in progress, and I doubt this will ever be uploaded to PyPI.