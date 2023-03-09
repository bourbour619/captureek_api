from django.core.files.storage import FileSystemStorage
from django.conf import settings
from uuid import uuid4
from os import path


def upload_file(file):
    name, extension = path.splitext(file.name)
    name = uuid4().hex[0:6]
    fss = FileSystemStorage(location='media/uploads' )
    f = fss.save(f'{name}{extension}', file)
    uri = fss.url(f)
    return f'http://localhost:8000{uri}'
