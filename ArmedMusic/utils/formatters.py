import json
import subprocess

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ''
    time_list = []
    time_suffix_list = ['s', 'ᴍ', 'ʜ', 'ᴅᴀʏs']
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ', '
    time_list.reverse()
    ping_time += ':'.join(time_list)
    return ping_time

def convert_bytes(size: float) -> str:
    if not size:
        return ''
    power = 1024
    t_n = 0
    power_dict = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        t_n += 1
    return '{:.2f} {}B'.format(size, power_dict[t_n])

async def int_to_alpha(user_id: int) -> str:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    text = ''
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text

async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    user_id = ''
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id

def time_to_seconds(time):
    stringt = str(time)
    return sum((int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':')))))

def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (seconds // (3600 * 24), seconds // 3600 % 24, seconds % 3600 // 60, seconds % 3600 % 60)
        if d > 0:
            return '{:02d}:{:02d}:{:02d}:{:02d}'.format(d, h, m, s)
        elif h > 0:
            return '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        elif m > 0:
            return '{:02d}:{:02d}'.format(m, s)
        elif s > 0:
            return '00:{:02d}'.format(s)
    return '-'

def speed_converter(seconds, speed):
    if str(speed) == str('0.5'):
        seconds = seconds * 2
    if str(speed) == str('0.75'):
        seconds = seconds + 50 * seconds // 100
    if str(speed) == str('1.5'):
        seconds = seconds - 25 * seconds // 100
    if str(speed) == str('2.0'):
        seconds = seconds - 50 * seconds // 100
    collect = seconds
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (seconds // (3600 * 24), seconds // 3600 % 24, seconds % 3600 // 60, seconds % 3600 % 60)
        if d > 0:
            convert = '{:02d}:{:02d}:{:02d}:{:02d}'.format(d, h, m, s)
            return (convert, collect)
        elif h > 0:
            convert = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
            return (convert, collect)
        elif m > 0:
            convert = '{:02d}:{:02d}'.format(m, s)
            return (convert, collect)
        elif s > 0:
            convert = '00:{:02d}'.format(s)
            return (convert, collect)
    return '-'

def clean_query(query: str) -> str:
    """
    Remove URLs and links from search query text.
    Specifically removes telegram and other HTTP/HTTPS URLs.
    """
    import re
    if not query:
        return query
    # Remove HTTP/HTTPS URLs
    query = re.sub(r'https?://\S+', '', query)
    # Remove t.me links
    query = re.sub(r't\.me/\S+', '', query)
    # Remove extra whitespace
    query = ' '.join(query.split())
    return query.strip()

def remove_emoji(text: str) -> str:
    """
    Remove emoji characters from text.
    """
    import re
    if not text:
        return text
    # Remove emoji by filtering out Unicode ranges commonly used for emoji
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # country flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(r'', text).strip()

def check_duration(file_path):
    command = ['ffprobe', '-loglevel', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_path]
    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    _json = json.loads(out)
    if 'format' in _json:
        if 'duration' in _json['format']:
            return float(_json['format']['duration'])
    if 'streams' in _json:
        for s in _json['streams']:
            if 'duration' in s:
                return float(s['duration'])
    return 'Unknown'
formats = ['webm', 'mkv', 'flv', 'vob', 'ogv', 'ogg', 'rrc', 'gifv', 'mng', 'mov', 'avi', 'qt', 'wmv', 'yuv', 'rm', 'asf', 'amv', 'mp4', 'm4p', 'm4v', 'mpg', 'mp2', 'mpeg', 'mpe', 'mpv', 'm4v', 'svi', '3gp', '3g2', 'mxf', 'roq', 'nsv', 'flv', 'f4v', 'f4p', 'f4a', 'f4b']
