from io import BytesIO
import os
import re
import subprocess
import zipfile

import requests


downloadUrl = "http://dl.stickershop.LINE.naver.jp/products/0/0/1/23303/iphone/stickerpack@2x.zip"
args = [
    'ffmpeg',
    '-i', 'pipe:',
    '-vf', 'scale=512:512:force_original_aspect_ratio=decrease:flags=lanczos',
    '-pix_fmt', 'yuva420p',
    '-c:v', 'libvpx-vp9',
    '-cpu-used', '5',
    '-minrate', '50k',
    '-b:v', '350k',
    '-maxrate', '450k', '-to', '00:00:02.900', '-an', '-y', '-f', 'webm', 'pipe:1'
]


imgsZip = requests.get(downloadUrl)
with zipfile.ZipFile(BytesIO(imgsZip.content)) as archive:
    files = [file for file in archive.infolist() if re.match(
        "animation@2x\/\d+\@2x.png", file.filename)]
    for entry in files:
        fileName = entry.filename.replace(
            "animation@2x/", "").replace(".png", "")
        rootPath = 'D:\\' + os.path.join("Projects", "ffmpeg", "Temp")
        # original file
        apngFile = os.path.join(rootPath, fileName+'.png')
        # output file
        webmFile = os.path.join(rootPath, fileName+'.webm')
        # output info
        infoFile = os.path.join(rootPath, fileName+'info.txt')

        with archive.open(entry) as file, open(apngFile, 'wb') as output_apng, open(webmFile, 'wb') as output_webm, open(infoFile, 'wb') as output_info:
            p = subprocess.Popen(args, stdin=subprocess.PIPE,
                                 stdout=subprocess.PIPE, stderr=output_info)
            outputBytes = p.communicate(input=file.read())[0]

            output_webm.write(outputBytes)
            file.seek(0)
            output_apng.write(file.read())
