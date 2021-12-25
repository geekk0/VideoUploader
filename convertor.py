import os
import time

source_path = os.path.join(os.getcwd(), 'original')
web_path = os.path.join(os.getcwd(), 'web')

print(source_path)
print(web_path)

cycle = True

while cycle:

    for files in os.walk(source_path):
        for file in files[2]:
            if not os.path.isfile(os.path.join(web_path, file[:-3]+'mp4')):
                try:
                    os.system('ffmpeg -i '+'"'+os.path.join(source_path, file)+'"'+' -vf scale=480:360 '+'"'
                              +os.path.join(web_path, file[:-3])+'mp4'+'"')
                except:
                    pass
            time.sleep(0.1)
