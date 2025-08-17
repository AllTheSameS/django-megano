import os
from megano.settings import MEDIA_ROOT

def delete_avatar(path: str):
    dir, filename = path.split("/")
    os.remove(os.path.join(MEDIA_ROOT, dir, filename))
