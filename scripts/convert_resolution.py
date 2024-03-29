from converter import Converter
from fractions import Fraction
import sys
import logging

logging.basicConfig(filename='logs.txt', filemode='a', format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

PROGRESS_LOADER = ['-', '\\', '|', '/']
EMOTES = ['└|∵|┐ ( ͡°ᴥ ͡° ʋ)', '┌|∵|┘ (ʋ  ͡°ᴥ ͡°)']

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
    if info.video.video_width is not None:
        logging.info(f'Resolution: {info.video.video_width}x{info.video.video_height} '
                     f'\tAspect Ratio: {Fraction(info.video.video_width, info.video.video_height)}')
        return info.video.video_width / info.video.video_height
    else:
        for stream in info.streams:
            if stream.type == 'video':
                logging.info(f'Resolution: {stream.video_width}x{stream.video_height} '
                             f'\tAspect Ratio: {Fraction(stream.video_width, stream.video_height)}')
                return stream.video_width / stream.video_height


def get_output_config(aspect_ratio):
    video_output_config = {
        'low': {
            'codec': 'h264',
            'width': int(144 * aspect_ratio),
            'height': 144,
            'fps': 60
        },
        'mid': {
            'codec': 'h264',
            'width': int(360 * aspect_ratio),
            'height': 360,
            'fps': 60
        },
        'high': {
            'codec': 'h264',
            'width': int(720 * aspect_ratio),
            'height': 720,
            'fps': 60
        },

    }
    #
    # if 1.7 > aspect_ratio > 1.4:
    #     video_output_config['low']['width'] = int(200 * aspect_ratio)
    #     video_output_config['low']['height'] = 200
    #     video_output_config['mid']['width'] = int(400 * aspect_ratio)
    #     video_output_config['mid']['height'] = 400
    #     video_output_config['high']['width'] = int(800 * aspect_ratio)
    #     video_output_config['high']['height'] = 800

    return video_output_config


def get_resolutions(file_name):
    conv = Converter()
    logging.info('Checking input video aspect ratio.')
    asp_ratio = get_info(conv, file_name)
    config = get_output_config(asp_ratio)
    for res in config:
        i = 0
        last_log_progress = 0
        output_file_name = '.'.join(file_name.split('.')[:-1]) + '_' + res + '.mp4'
        OUTPUT_CONFIG['video'] = config[res]
        logging.info(f'Converting to {res}, res. [{config[res]["width"]}x{config[res]["height"]}]')
        convert = conv.convert(file_name, output_file_name, OUTPUT_CONFIG)
        for time_code in convert:
            print(f'\rConverting {time_code * 100:.1f}% * {PROGRESS_LOADER[i % 4]} * {EMOTES[i % 2]}  ', end='',
                  flush=True)
            if time_code * 100 - last_log_progress >= 5:
                logging.info(f'Progress: {time_code * 100:.1f}%')
                last_log_progress = time_code * 100
            i += 1
        logging.info('\rConversion completed.                                   ')
        logging.info(f'Writing to file: {output_file_name}')


if __name__ == '__main__':
    file = 'test.mkv'

    if len(sys.argv) > 1:
        file = sys.argv[1]

    logging.info('')
    logging.info('---------------------------------------------')
    logging.info(f'Current file: {file}')

    ext = file.split('.')[-1]
    if ext.lower() not in ['mkv', 'mp4', 'mov', 'webex']:
        logging.info(f'{file} does not seem to be a video. Skipping.')
    else:
        get_resolutions(file)
