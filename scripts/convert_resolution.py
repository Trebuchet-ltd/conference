from converter import Converter

PROGRESS_LOADER = ['-', '\\', '|', '/']
EMOTES = ['└|∵|┐ ( ͡°ᴥ ͡° ʋ)', '┌|∵|┘ (ʋ  ͡°ᴥ ͡°)']

VIDEO_OUTPUT_CONFIG = {
    '144p': {
        'codec': 'h264',
        'width': 256,
        'height': 144,
        'fps': 60
    },
    '360p': {
        'codec': 'h264',
        'width': 640,
        'height': 360,
        'fps': 60
    },
    '720p': {
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


def get_resolutions(file_name):
    print('Converting file:', file_name)
    for res in VIDEO_OUTPUT_CONFIG:
        prev = 0
        i = 0
        conv = Converter()
        output_file_name = file_name.split('.')[0] + '_' + res + '.mp4'
        OUTPUT_CONFIG['video'] = VIDEO_OUTPUT_CONFIG[res]
        convert = conv.convert(file_name, output_file_name, OUTPUT_CONFIG)
        print('Converting to resolution:', res)
        for timecode in convert:
            if timecode - prev >= 0.01:
                print(f'\rConverting {timecode * 100:.0f}% * {PROGRESS_LOADER[i % 4]} * {EMOTES[i % 2]}  ', end='',
                      flush=True)
            prev = timecode
            i += 1
        print('\rWriting to file:', output_file_name)
        print('Completed.')


if __name__ == '__main__':
    get_resolutions('test.mkv')
