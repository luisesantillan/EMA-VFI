import cv2  # Import the OpenCV library
import os  # Import os for file handling
import argparse

# Set up argument parser
parser = argparse.ArgumentParser(description='Extract frames from a video file')
parser.add_argument('--video', type=str, help='Path to the input video file',required=True)
parser.add_argument('--folder', type=str, help='Path to the output folder for the frames',required=True)
args = parser.parse_args()

# Get video path from arguments
video_path = args.video
output_dir = args.folder

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the video file
video_capture = cv2.VideoCapture(video_path)

# Get frames per second (FPS) of the video
fps = video_capture.get(cv2.CAP_PROP_FPS)
print(f"Frames per second: {fps}")

# Initialize frame count
frame_count = 0

# Loop through the video frame-by-frame
while True:
    # Read the next frame
    success, frame = video_capture.read()
    
    # If the frame was not successfully read, break the loop (end of video)
    if not success:
        break
    
    # Define the output path for this frame as a PNG
    frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.png")
    
    # Save the frame as a PNG file
    cv2.imwrite(frame_filename, frame)
    
    # Increment the frame count
    frame_count += 1

# Release the video capture object
video_capture.release()
print(f"Total frames saved: {frame_count}")
