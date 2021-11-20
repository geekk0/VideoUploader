import os

from VideoUploader import settings

source_path = os.path.join(settings.BASE_DIR, 'Original')
web_path = os.path.join(settings.BASE_DIR, 'Web')

cycle = True

while cycle:

    for files in os.walk(source_path):
        for file in files[2]:
            if not os.path.isfile(os.path.join(web_path, file[:-3]+'mp4')):
                try:
                    os.system('ffmpeg -i '+'"'+os.path.join(source_path, file)+'"'+' -vf scale=480:360 '+'"'
                              +os.path.join(web_path, file[:-3])+'mp4'+'"')
                except:
                    print('не могу конвертировать')
