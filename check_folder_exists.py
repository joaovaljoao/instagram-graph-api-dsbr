from pathlib import Path
import errno

def checar_pasta(pasta):
    if not pasta.exists():
        try:
            Path.mkdir(pasta)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise