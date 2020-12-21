from converter import Converter

# ffmpegPath = r'D:\Libraries\ffmpeg-4.3.1-2020-11-19-full_build\bin\ffmpeg.exe'
# ffprobePath = r'D:\Libraries\ffmpeg-4.3.1-2020-11-19-full_build\bin\ffprobe.exe'

# conv = Converter(ffmpegPath, ffprobePath)

conv = Converter()

file_name = 'test.mkv'

info = conv.probe(file_name)

convert = conv.convert(file_name, 'output.mp4', {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 640,
        'height': 480,
        'fps': 60
    }})

prev = 0
print(info)
print('Starting conversion.')
i = 0
progress = ['-', '\\', '|', '/']
emotes = ['└|∵|┐', '┌|∵|┘']
for timecode in convert:
    if timecode - prev >= 0.01:
        print(f'\rConverting {timecode * 100:.0f}% * {progress[i % 4]} * {emotes[i%2]} ( ͡°ᴥ ͡° ʋ) ', end='', flush=True)
    prev = timecode
    i += 1

print('Completed.')
