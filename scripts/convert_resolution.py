from converter import Converter
import sys

PROGRESS_LOADER = ['-', '\\', '|', '/']
EMOTES = ['└|∵|┐ ( ͡°ᴥ ͡° ʋ)', '┌|∵|┘ (ʋ  ͡°ᴥ ͡°)']

VIDEO_OUTPUT_CONFIG = {
    'low': {
        'codec': 'h264',
        'width': 256,
        'height': 144,
        'fps': 60
    },
    'mid': {
        'codec': 'h264',
        'width': 640,
        'height': 360,
        'fps': 60
    },
    'high': {
        'codec': 'h264',
        'width': 1280,
        'height': 720,
        'fps': 60
    },

}



OUTPUT_CONFIG = {
    'format': 'mp4',
    'audio': {
        'codec': 'aac',
        'samplerate': 11025,
        'channels': 2
    },
}


def get_info(conv, file_name):
    info = conv.probe(file_name)
    if video in info:
        print('1')
        print(info.video.video_width, info.video.video_height)
        return info.video.video_width / info.video.video_height
    else:
        for stream in info.streams:
            if width in stream:
                print('2')
                print(stream.width, stream.height)
                return stream.width / stream.height


# def get_resolutions(file_name):
#     conv = Converter()
#     print('Checking input video aspect ratio.')
#     info = conv.probe(file_name)
#     print(info)
#     # asp_ratio = info.video.video_width / info.video.video_height
#     # if asp_ratio != (16 / 9):
#     #     print(f'Input resolution of {info.video.video_width}x{info.video.video_height} is not 16:9. Skipping.')
#     #     return
#
#     for res in VIDEO_OUTPUT_CONFIG:
#         i = 0
#         output_file_name = '.'.join(file_name.split('.')[:-1]) + '_' + res + '.mp4'
#         OUTPUT_CONFIG['video'] = VIDEO_OUTPUT_CONFIG[res]
#         convert = conv.convert(file_name, output_file_name, OUTPUT_CONFIG)
#         print('Converting to', res, 'res.')
#         for timecode in convert:
#             print(f'\rConverting {timecode * 100:.1f}% * {PROGRESS_LOADER[i % 4]} * {EMOTES[i % 2]}  ', end='',
#                   flush=True)
#             i += 1
#         print('\rConversion completed.                                   ')
#         print('Writing to file:', output_file_name)


if __name__ == '__main__':
    file = 'test.mkv'

    if len(sys.argv) > 1:
        file = sys.argv[1]

    print('\nCurrent file:', file)

    ext = file.split('.')[-1]
    if ext.lower() not in ['mkv', 'mp4']:
        print(file, 'does not seem to be a video. Skipping.')
    else:
        conv = Converter()
        asp = get_info(conv, file)
        print('Aspect:', asp)
        # get_resolutions(file)
