from django.shortcuts import render
import os, re, time, json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator , PageNotAnInteger, EmptyPage
from . import fileInfoGetService as fs
from . import getVideoFirstFrame as gVF

# Create your views here.

def searchSXHB(request):  #查询上新海报系列二维码链接
    haibaoSearchName = request.GET.get('haibao_name')
    print(haibaoSearchName)
    videoNameList = []
    videoUrlList = []
    videoFrameImgUrlList = []
    if request.method == "GET":
        getsearchSXHB = getSXHB( haibaoSearchName )
        for fileindex, fileurl, filename, fn, fntype, fileServerPath, filetype, functionindex in getsearchSXHB:  # 此步会将zip迭代光，zip为迭代器属性
            if fntype == 'mp4':
                video = fileServerPath
                frameImgName = fn.split('.')[-2]  # 取视频的前缀名
                img = "/mnt/videoFrame/{}.jpg".format(frameImgName)
                imgExist = os.path.exists(img)
                if imgExist is False:
                    try:
                        gVF.getFrames(video, img)
                    except Exception as e:
                        print(e)
                else:
                    print('{}.jpg 视频预览文件已存在'.format(frameImgName))
                videoNameList.append(fn)
                videoUrlList.append(fileurl)
                videoFrameImgUrlList.append("/videoFrame/{}.jpg".format(frameImgName))
        videoData = zip(videoNameList, videoUrlList, videoFrameImgUrlList)
        getsearchSXHB = getSXHB( haibaoSearchName )  # 重新获取zip      
        getsearchSXHBData = { 'AllData': getsearchSXHB, 'haibao_name': haibaoSearchName, 'videoData': videoData }
        try:
            return render(request, 'photo/showsearchhaibao.html', getsearchSXHBData)
        except:
            pass


def getSXHB(haibao_name):  #查询上新海报海报内容数据
    haibao_name = haibao_name
    SXHBPoolNum = 5
    typeword = '上新海报'
    typewordlikelist = ['shangxinhaibao']
    serverRootPath = '/mnt/shangxinhaibao'
    PcRootPath = '\\\\172.18.99.210\\品牌部\\5.淘系上新设计\\上新开屏海报+周一例会海报\\周一例会海报'
    SXHBGetInfoService = fs.fileInfoGetService(RedisPoolNum = SXHBPoolNum, keyword = haibao_name, typeword = typeword,
                                        typewordlikelist = typewordlikelist, serverRootPath = serverRootPath, PcRootPath = PcRootPath)
    SXHBresaultsData = SXHBGetInfoService.resaultsfiledata()
    try:
        SXHBresaultPD = len(SXHBresaultsData['fileurllist'])
    except:
        SXHBresaultPD = 'OK Getch It'
    SXHBfileindexlist = SXHBresaultsData['fileindexlist']
    SXHBfileurllist = SXHBresaultsData['fileurllist']
    SXHBtypewordlikeresaultslist = SXHBresaultsData['typewordlikeresaultslist']                 
    SXHBfnlist = SXHBresaultsData['fnlist']
    SXHBfntypelist = SXHBresaultsData['fntypelist']
    SXHBfiletypelist = SXHBresaultsData['filetypelist']
    SXHBfileServerPathList = SXHBresaultsData['fileServerPathList']
    SXHBresaultsData['resaultPD'] = SXHBresaultPD
    SXHBFunctionIndex = SXHBresaultsData['functionIndex']
    FunctionIndexSum = SXHBFunctionIndex
    FunctionIndexSumList = []
    for FunctionIndex in range(1, FunctionIndexSum + 1):
        FunctionIndexSumList.append(FunctionIndex)
    print('FunctionIndexSumList', len(FunctionIndexSumList))
    Allfileindexlist = SXHBfileindexlist
    print('Allfileindexlist',len(Allfileindexlist))
    Allfileurllist = SXHBfileurllist
    print('Allfileurllist',len(Allfileurllist))
    Alltypewordlikeresaultslist = SXHBtypewordlikeresaultslist
    print('Alltypewordlikeresaultslist',len(Alltypewordlikeresaultslist))
    Allfnlist = SXHBfnlist
    print('Allfnlist',len(Allfnlist))
    Allfntypelist = SXHBfntypelist
    print('Allfntypelist',len(Allfntypelist))
    AllfileServerPathList = SXHBfileServerPathList
    print('AllfileServerPathList',len(AllfileServerPathList))
    Allfiletypelist = SXHBfiletypelist
    print('Allfiletypelist',len(Allfiletypelist))
    filetypeSet = list(set(Allfiletypelist))
    print('filetypeSet',filetypeSet)
    AllData = zip(Allfileindexlist, Allfileurllist, Alltypewordlikeresaultslist, Allfnlist, Allfntypelist, AllfileServerPathList, Allfiletypelist, FunctionIndexSumList)
    return AllData