import ffmpeg

def mp3_to_m4a(mp3_file):
    '''
        reference:
        - https://pypi.org/project/ffmpeg-python/
        - https://qiita.com/satoshi2nd/items/4f6814b795a772af4af0
        - https://self-development.info/ffmpeg-python%E3%81%AB%E3%82%88%E3%82%8Awav%E3%82%92mp3%E3%81%AB%E5%A4%89%E6%8F%9B%E3%81%99%E3%82%8B%E3%80%90python%E3%80%91/
    '''
    stream = ffmpeg.input(mp3_file)
    stream = ffmpeg.output(stream, mp3_file.replace(".mp3", ".m4a"))
    ffmpeg.run(stream)

