import os, sys
sys.path.append('.')
from interpolate import Interpolator
import cv2
from natsort import natsorted
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Interpolate frames')

input_source = parser.add_mutually_exclusive_group(required=True)
input_source.add_argument('--input_video', type=str, required=False, help='Path to input video file')
input_source.add_argument('--input_folder', type=str, required=False, help='Path to input frames folder')
output = parser.add_mutually_exclusive_group(required=True)
output.add_argument('--output_folder', type=str, required=False, help='Path to output frames folder')
output.add_argument('--output_video', type=str, required=False, help='Path to output video file')
parser.add_argument('--n', type=int, default=1)

args = parser.parse_args()

def batch_interpolate(input_folder, output_folder, n_frames=1, input_video=None, output_video=None):
    if input_video is not None:
        temp_folder = "temp_frames"
        if os.path.exists(temp_folder):
            erase = 'y'
            if erase == 'y':
                os.system(f"rm -rf {temp_folder}")
            else:
                print("Exiting...")
                return
        os.makedirs(temp_folder, exist_ok=True)
        import subprocess
        subprocess.run([
            'python', 'video_to_folder.py',
            '--video', input_video,
            '--folder', temp_folder
        ])
        input_folder = temp_folder

    if output_video is not None:
        output_folder = "temp_interpolated_frames"
        if os.path.exists(output_folder):
            erase = 'y'
            if erase == 'y':
                os.system(f"rm -rf {output_folder}")
            else:
                print("Exiting...")
                return
        os.makedirs(output_folder, exist_ok=True)

    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files = natsorted(image_files)
    
    interpolator = Interpolator()
    frame_count = 0
    
    with tqdm(total=(len(image_files)-1)*(n_frames+2), desc="Processing frames") as pbar:
        for i in range(len(image_files) - 1):
            img1_path = os.path.join(input_folder, image_files[i])
            img2_path = os.path.join(input_folder, image_files[i+1])
            
            # Write first frame only once
            if i == 0:
                original = cv2.imread(img1_path)
                output_path = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
                cv2.imwrite(output_path, original)
                frame_count += 1
                pbar.update(1)
            
            # Get and write interpolated frames immediately
            for frame in interpolator.interpolate_frames(img1_path, img2_path, n_frames):
                output_path = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
                cv2.imwrite(output_path, frame)
                frame_count += 1
                pbar.update(1)
            
            # Write second frame
            original = cv2.imread(img2_path)
            output_path = os.path.join(output_folder, f'frame_{frame_count:04d}.png')
            cv2.imwrite(output_path, original)
            frame_count += 1
            pbar.update(1)
    
    if output_video is not None:
        import subprocess
        subprocess.run([
            'python', 'folder_to_video.py',
            '--folder', output_folder,
            '--video', output_video
        ])

    return frame_count

if __name__ == "__main__":
    n_frames = args.n
    input_folder = args.input_folder if args.input_folder is not None else None
    output_folder = args.output_folder if args.output_folder is not None else None
    input_video = args.input_video if args.input_video is not None else None
    output_video = args.output_video if args.output_video is not None else None
    total_frames = batch_interpolate(input_folder, output_folder, n_frames, input_video, output_video)
    print(f"Processing complete!")
