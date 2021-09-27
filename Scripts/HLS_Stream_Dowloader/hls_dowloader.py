import sys, os, asyncio, shutil
import wget
from ffmpeg import FFmpeg

# Func calls wget to download the file given in url arg
def webget(url):
    wget.download(url)

# Fuc calls ffmpeg to transcode .m3u8 to .mp4
def transcode(ffmpeg):
    @ffmpeg.on('stderr')
    def on_stderr(line):
        print(line)

    @ffmpeg.on('progress')
    def on_progress(progress):
        print(progress)

    @ffmpeg.on('completed')
    def on_completed():
        print('\nCompleted')

    @ffmpeg.on('error')
    def on_error(code):
        print('Error:', code)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(ffmpeg.execute())
    loop.close()


def parse_m3u8_url(input_url):
    parse_url = input_url.split('/')
    input_m3u8 = parse_url[len(parse_url) - 1]

    base_url = input_url[:-len(input_m3u8)]

    if '?' in input_m3u8:
        input_m3u8 = input_m3u8.split('?')[0]

    return base_url, input_m3u8


def create_manifest(input_m3u8):
    with open(f'./{input_m3u8}', 'r') as f:
        file = f.readlines()

    manifest = []
    for el in file:
        el = el[:-1]
        if 'http' in el and '?' in el and '=' in el:
            manifest.append(el)

        elif 'https' in el:
            el = el.split('/')
            el = el[len(el)-1]
            manifest.append(el)

        else:
            manifest.append(el)

    with open('./manifest.m3u8', 'a') as f:
        for elm in manifest:
            f.write(elm+'\n')


def cleanup_working_dir(input_m3u8, storage_folder):
    try:
        # Create folder given in arg
        os.mkdir(storage_folder)

    except FileExistsError:
        print('\nWARNING: Output folder exists')

    cwd = os.getcwd()
    files = os.listdir()

    print(f'\nMESSAGE: Cleaning up and Packaging things nicely')
    os.mkdir(f'{storage_folder}/{storage_folder}')

    for f in files:
        # Logic for moving the output file
        if f[-3:] == 'mp4':
            original = f'{cwd}/{f}'
            target = f'{cwd}/{storage_folder}'

            # Moving the output file
            print(f'\nMESSAGE: Moving {input_m3u8} to {storage_folder}')
            shutil.move(original,target)

        if f[-4:] == 'm3u8':
            original = f'{os.getcwd()}/{f}'
            target = f'{os.getcwd()}/{storage_folder}/{storage_folder}'
            shutil.move(original,target)

        if f[-2:] == 'ts':
            original = f'{os.getcwd()}/{f}'
            target = f'{os.getcwd()}/{storage_folder}/{storage_folder}'
            shutil.move(original,target)


# Read cli args : 'hls-downloader.py ["m3u8_url"] ["mp4_output_name"] ["storage_folder"]'
input_url = sys.argv[1]
output_filename = sys.argv[2]
storage_folder = "./site/media"

base_url, input_m3u8 = parse_m3u8_url(input_url)

# Call wget to download files
if input_m3u8 in os.listdir():
    print(f'WARNING: {input_m3u8} already exists')

else:
    print(f'MESSAGE: Downloading m3u8 file')
    webget(input_url)

print(f'\nMESSAGE: Creating manifest.m3u8')
create_manifest(input_m3u8)

print(f'\nMESSAGE: Reading {input_m3u8}')

data = None

if 'movcloud' in input_url:
    with open('playlist.m3u8', 'r') as f:
        data = f.read()

elif 'manifest.m3u8' in os.listdir():
    with open('manifest.m3u8', 'r') as f:
        data = f.read()

if data != None:
    contents = data.split('\n')
    print(f'\nMESSAGE: Attempting to download items from {input_m3u8}')
    for item in contents:
        if item in os.listdir():
            continue

        if 'http' in item and '?' in item and '=' in item:
            webget(item)

        if 'movcloud' in item:
            item_sp = item.split('/')

            if item_sp[len(item_sp)-1] in os.listdir():
                continue
            else:
                webget(item)

        else:
            stxt = item[0:5]
            entxt = item[-2:]
            if stxt == 'https':
                l = item.split('/')
                name = item[len(l)-1]
                webget(item)

            elif entxt == 'ts':
                cut = slice(0,-len(input_m3u8))
                webget(input_url[cut] + item)

# Configuring ffmpeg
## ffmpeg -i "./folder/file.m3u8" -c copy file.mp4
_ffmpeg = FFmpeg().option('n').input('./manifest.m3u8').output(output_filename,{'c': 'copy'})

print(f'\n\nMESSAGE: Running command: ffmpeg -i ./manifest.m3u8 -c copy {output_filename}')
transcode(_ffmpeg)

cleanup_working_dir(input_m3u8, storage_folder)
