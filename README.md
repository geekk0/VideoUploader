# VideoUploader

![python version](https://img.shields.io/badge/python-3.9.5-brightgreen)
![languages](https://img.shields.io/github/languages/top/geekk0/VideoUploader)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3cc6c94a88dd41be9b84faf38e378752)](https://www.codacy.com/gh/geekk0/VideoUploader/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geekk0/BRIO_assistant&amp;utm_campaign=Badge_Grade)
![last-commit](https://img.shields.io/github/last-commit/geekk0/VideoUploader)

<br>Video files upload and preview service.

## Live demo
https://www.video-uploader.tk
## Description

With this site, user is allowed to upload video files to server "original" folder. Content-manager user has acceess to admin panel, where video preview, deleting files and author info are available.<br>
As video files may have different containers, there is script, converting them to mp4 for admin file preview in low res, to "web" folder as soon as file upload is finished.

## Features


- Multilanguage interface on user/admin(En/Ru)
- File size check on upload form (200 mb max).
- Server available free space check while upload (4000 mb max)
- User explaining messages of server limits and upload processing.

## Set up

This site runs on VDS, using NGINX with http_mp4_module enabled.<br>
Converting script "converter.py" is running on detached screen.<br>
Requirements.txt

