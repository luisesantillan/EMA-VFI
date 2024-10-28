import cv2
import os
import argparse
from natsort import natsorted

# Set up argument parser
parser = argparse.ArgumentParser(description='Create video from a folder of frames')
parser.add_argument('--folder', type=str, help='Path to the input folder containing frames', required=True)
parser.add_argument('--video', type=str, help='Path to the output video file', required=True)
parser.add_argument('--fps', type=float, help='Frames per second for output video', default=30.0)
args = parser.parse_args()

# Get paths from arguments
input_folder = args.folder
output_video = args.video
fps = args.fps

# Get list of frames sorted naturally
frames = natsorted([os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.startswith('frame_') and f.endswith('.png')])

if not frames:
    print("No frames found in the specified folder")
    exit(1)

# Read first frame to get dimensions
first_frame = cv2.imread(frames[0])
height, width, layers = first_frame.shape

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_writer = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# Write frames to video
frame_count = 0
for frame_path in frames:
    frame = cv2.imread(frame_path)
    video_writer.write(frame)
    frame_count += 1

# Release the video writer
video_writer.release()
print(f"Video created successfully with {frame_count} frames at {fps} FPS")