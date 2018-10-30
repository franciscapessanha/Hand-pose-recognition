import sys
from helpers import is_int
from video_labeling import label_video

def handle_arguments():
  if len(sys.argv) == 1:
    label_video(0)
  elif len(sys.argv) == 2:
    if is_int(sys.argv[1]):
      label_video(int(sys.argv[1]))
    else:
      if sys.argv[1].endswith('.mp4'):
        label_video(sys.argv[1])

if __name__ == "__main__":
  handle_arguments()

