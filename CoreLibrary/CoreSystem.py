import os
from assignment_webapp import settings
from django.core.files.storage import FileSystemStorage

def uploadImage(file):
    imageUploadPath = os.path.join(settings.STATIC_DIR, 'images')
    url = os.path.join(settings.STATIC_URL, 'images')
    fs = FileSystemStorage(location=imageUploadPath, base_url=url)
    filename = fs.save(file.name, file)
    return filename
