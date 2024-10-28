import os, sys
sys.path.append('.')
from interpolate import Interpolator
import cv2
from natsort import natsorted
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Interpolate frames')
parser.add_argument('--input_folder', type=str, required=True)
parser.add_argument('--output_folder', type=str, required=True)
parser.add_argument('--n', type=int, default=1)
args = parser.parse_args()

def batch_interpolate(input_folder, output_folder, n_frames=1):
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
            for frame in interpolator.interpolate_frames_generator(img1_path, img2_path, n_frames):
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
    
    return frame_count

if __name__ == "__main__":
    input_folder = args.input_folder
    output_folder = args.output_folder
    n_frames = args.n
    
    total_frames = batch_interpolate(input_folder, output_folder, n_frames)
    print(f"Processing complete! Generated {total_frames} total frames in {output_folder}")