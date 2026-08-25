import mutagen.mp3
from mutagen.mp3 import MP3
# from mutagen.mp4 import MP4
from os import listdir
from os.path import isfile, join
import sys

def parse():
    if len(sys.argv) != 3:  # python main.py music all.txt
        print("usage: " + __file__ + " \"directory name\"")
        return

    directory = sys.argv[1]
    fileNames = [f for f in listdir(directory) if isfile(join(directory, f))]

    outputFileName = sys.argv[2]
    with open(outputFileName, "w") as f:
        newLine = ''
        for fileName in fileNames:
            filePath = directory + "\\" + fileName
            print("file: " + filePath)
            try:
                audio = MP3(filePath)
            except mutagen.mp3.HeaderNotFoundError:
                print("ERROR: file: " + filePath + " is not mp3")
                continue
            # title = audio.tags.get("TIT2")
            # author = audio.tags.get("TPE1")
            # newLine += author + " - " + title
            print(audio.tags.get("TIT2"))
            print(audio.tags.get("TPE1"))


if __name__ == '__main__':
    parse()
