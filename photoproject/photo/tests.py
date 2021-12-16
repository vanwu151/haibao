from django.test import TestCase
import os, re, time, json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator , PageNotAnInteger, EmptyPage
import getVideoFirstFrame

video = "/mnt/shangxinhaibao/12.3 大娱乐家系列/12.3 大娱乐家系列（主题视频）2.mp4"
img = "/mnt/shangxinhaibao/12.3 大娱乐家系列/test.jpg"
getVideoFirstFrame.getFrames(video, img)
