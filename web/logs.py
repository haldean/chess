import datetime
import traceback

log_file = "/var/log/chess/access.log"
error_file = "/var/log/chess/error.log"

def wrap(func):
    def _wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            with open(error_file, "a") as f:
                f.write("Exception at %s\n" % datetime.datetime.now())
                traceback.print_exc(file=f)
            raise
    _wrapped.__name__ = func.__name__
    return _wrapped
