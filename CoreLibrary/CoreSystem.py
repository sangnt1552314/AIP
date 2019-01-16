import os
from assignment_webapp import settings
from django.core.files.storage import FileSystemStorage

def uploadImage(file):
    imageUploadPath = os.path.join(settings.STATIC_DIR, 'images')
    url = os.path.join(settings.STATIC_URL, 'images')
    fs = FileSystemStorage(location=imageUploadPath, base_url=url)
    filename = fs.save(file.name, file)
    return filename

def deleteImage(image_path, image_name):
    if os.path.exists(os.path.join(image_path, image_name)):
        os.remove(os.path.join(image_path, image_name))
    if os.path.exists(os.path.join(image_path, 'edge_map.png')):
        os.remove(os.path.join(image_path, 'edge_map.png'))
    if os.path.exists(os.path.join(image_path, 'line.png')):
        os.remove(os.path.join(image_path, 'line.png'))
    if os.path.exists(os.path.join(image_path, 'rotated.png')):
        os.remove(os.path.join(image_path, 'rotated.png'))
    if os.path.exists(os.path.join(image_path, 'thres.png')):
        os.remove(os.path.join(image_path, 'thres.png'))

