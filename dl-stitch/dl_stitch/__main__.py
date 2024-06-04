from twitchdl.commands import download
from twitchdl import console
import argparse
import subprocess

twitchDlParser = console.get_parser()
parser = argparse.ArgumentParser()

parser.add_argument("url", type=str, help="Twitch clip or highlight url/s")
parser.add_argument(
    "timestamps", nargs="+", type=str, help="Timestamps for each section wanted"
)
parser.add_argument(
    "-o", "--output", action="store", dest="output", help="Output file name"
)

# ! Script params
args = parser.parse_args()
url = args.url
timestamps = args.timestamps
output = args.output

# print(args)


def main():
    for i, timestamp in enumerate(timestamps):
        args = twitchDlParser.parse_args(
            ["download"]
            + [url.split("/videos/")[1].split("?")[0]]
            + ["-f", "mp4"]
            + ["-o", f"{i}.mp4"]
            + ["-q", "source"]
            + convertToArgsArray(timestamp)
        )
        print("ARGS:", args)
        download(args)

    # Create a list of files to concat
    textFileCommand = (
        "(echo file "
        + " & echo file ".join([f"{i}.mp4" for i, _ in enumerate(timestamps)])
        + ")> files.txt"
    )
    print("textFileCommand", textFileCommand)
    subprocess.run(textFileCommand, shell=True)

    ffmpegCommand = f"ffmpeg -f concat -safe 0 -i files.txt -c copy {output}.mp4"
    print("ffmpegCommand", ffmpegCommand)
    subprocess.run(ffmpegCommand, shell=True)

    print("---DONE---")


def convertToArgsArray(args: str):
    return args.split(" ") if args else []
