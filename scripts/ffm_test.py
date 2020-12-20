from converter import Converter

# ffmpegPath = r'D:\Libraries\ffmpeg-4.3.1-2020-11-19-full_build\bin\ffmpeg.exe'
# ffprobePath = r'D:\Libraries\ffmpeg-4.3.1-2020-11-19-full_build\bin\ffprobe.exe'

# conv = Converter(ffmpegPath, ffprobePath)

conv = Converter()

info = conv.probe('test.mp4')

convert = conv.convert('test.mp4', '.output.mp4', {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
    'video': {
        'codec': 'hevc',
        'width': 720,
        'height': 400,
        'fps': 60
    }})

for timecode in convert:
    print(f'\rConverting ({timecode:.2f}) ...')
