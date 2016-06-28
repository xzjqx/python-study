import md5
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()
filename = args.file
m = md5.new()
m.update(filename)
with open(filename, 'rb') as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        m.update(data)
print m.hexdigest()
