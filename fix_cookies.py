with open('cookies/youtube_cookies.txt', 'r') as f:
    lines = f.readlines()

with open('cookies/youtube_cookies.txt', 'w') as f:
    for line in lines:
        if line.startswith('.'):
            line = line[1:]
        f.write(line)