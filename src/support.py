from pathlib import Path
import errno
from datetime import datetime


class SuppportFunctions:

    def __init__(self) -> None:

        pass
        
    def create_folder_exists(folder):
        if not folder.exists():
            try:
                Path.mkdir(folder)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise


    def epoch_to_dt(expires_in):
        epoch_expiration_date = datetime.now().timestamp() + int(expires_in)
        return str(datetime.utcfromtimestamp(epoch_expiration_date))