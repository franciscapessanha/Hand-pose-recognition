import numpy as np

def concatenate_frames(frame1, frame2): # Concatenates frames horizontally
  return np.concatenate((frame1, frame2), axis=1)