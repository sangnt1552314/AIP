import os
from django.shortcuts import render
from AIP import forms
from CoreLibrary import CoreSystem, CoreImage, CoreText
from assignment_webapp import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = forms.Upload(request.POST, request.FILES)
        if form.is_valid():
            image_name = CoreSystem.uploadImage(request.FILES['image'])
            write_path = os.path.join(settings.STATIC_DIR, 'images')
            src_path = os.path.join(write_path, image_name)
            D = CoreImage.info(src_path)[-1]
            content = {'image_name': image_name, 'D': D}
            return render(request, 'AIP/show.html', context=content)
    else:
        form = forms.Upload()
    return render(request, 'AIP/index.html', {'form': form})

def about(request):
    return render(request, 'AIP/about.html')

def show(request):
    if request.method == 'POST':
        form = forms.Upload(request.POST, request.FILES)
        if form.is_valid():
            image_name = CoreSystem.uploadImage(request.FILES['image'])
            write_path = os.path.join(settings.STATIC_DIR, 'images')
            src_path = os.path.join(write_path, image_name)
            D = CoreImage.info(src_path)[-1]
            content = {'image_name': image_name, 'D': D}
            return render(request, 'AIP/show.html', context=content)
    else:
        form = forms.Upload()
    return render(request, 'AIP/show.html', {'form': form})

def faq(request):
    return render(request, 'AIP/faq.html')

def canny(request):
    if request.method == 'POST':
        image_name = request.POST.get('image_name')
        min = int(request.POST.get('min_threshold'))
        max = int(request.POST.get('max_threshold'))
        D = int(request.POST.get('D'))

        write_path = os.path.join(settings.STATIC_DIR, 'images')
        src_path = os.path.join(write_path, image_name)
        CoreImage.Canny(src_path, write_path, min, max)

        exists = os.path.isfile(os.path.join(write_path, 'edge_map.png'))
        if exists:
            hadEdgeMap = True
        else:
            hadEdgeMap = False
        content = {'image_name': image_name, 'hadEdgeMap': hadEdgeMap, 'min': min, 'max': max, 'D': D}
        return render(request, 'AIP/show.html', context=content)
    else:
        form = forms.Upload()
        return render(request, 'AIP/show.html', {'form': form})

def hough(request):
    if request.method == 'POST':
        image_name = request.POST.get('image_name')
        M = int(request.POST.get('M'))
        N = int(request.POST.get('N'))
        K = int(request.POST.get('K'))
        min = int(request.POST.get('min'))
        max = int(request.POST.get('max'))
        D = int(request.POST.get('D'))

        write_path = os.path.join(settings.STATIC_DIR, 'images')
        src_path = os.path.join(write_path, image_name)

        edge_map = CoreImage.Canny(src_path, write_path, min, max)

        CoreImage.DetectLine(src_path, write_path, edge_map, M, N, K)
        exists = os.path.isfile(os.path.join(write_path, 'line.png'))
        if exists:
            hadLine = True
        else:
            hadLine = False

        content = {'image_name': image_name, 'hadEdgeMap': True,
                   'min': min, 'max': max, 'hadLine': hadLine,
                   'M': M, 'N': N, 'K': K, 'D': D}
        return render(request, 'AIP/show.html', context=content)
    else:
        form = forms.Upload()
        return render(request, 'AIP/show.html', {'form': form})

def extract(request):
    if request.method == 'POST':
        image_name = request.POST.get('image_name')
        M = int(request.POST.get('M'))
        N = int(request.POST.get('N'))
        K = int(request.POST.get('K'))
        min = int(request.POST.get('min'))
        max = int(request.POST.get('max'))
        D = int(request.POST.get('D'))
        hadEdgeMap = True
        hadLine = True
        write_path = os.path.join(settings.STATIC_DIR, 'images')
        src_path = os.path.join(write_path, "rotated.png")

        google_text = CoreText.google_ocr(src_path)[-1]
        ocr_simple_text = CoreText.simple_img2text(src_path)
        ocr_text = CoreText.img2text(src_path, write_path)

        content = {'image_name': image_name, 'hadEdgeMap': hadEdgeMap,
                   'min': min, 'max': max, 'hadLine': hadLine,
                   'M': M, 'N': N, 'K': K, 'D': D,
                   'google_text': google_text, 'ocr_simple_text': ocr_simple_text,
                   'ocr_text': ocr_text}
        return render(request, 'AIP/show.html', context=content)

def reset(request):
    if request.method == 'POST':
        image_name = request.POST.get('image_name')
        image_path = os.path.join(settings.STATIC_DIR, 'images')
        CoreSystem.deleteImage(image_path, image_name)
        return HttpResponseRedirect(reverse('AIP:index'))
