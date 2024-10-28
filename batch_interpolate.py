import os, sys
sys.path.append('.')
from interpolate import Interpolator
import cv2
from natsort import natsorted

def batch_interpolate(input_folder, output_folder, n_frames=1):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all image files and sort them naturally
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files = natsorted(image_files)
    
    # Initialize interpolator
    interpolator = Interpolator()
    
    # Final list to store all frames in order
    all_frames = []
    
    # Process each consecutive pair of frames
    for i in range(len(image_files) - 1):
        img1_path = os.path.join(input_folder, image_files[i])
        img2_path = os.path.join(input_folder, image_files[i+1])
        
        # Add original frame
        if i == 0:
            original = cv2.imread(img1_path)
            all_frames.append(original)
        
        # Get interpolated frames
        interpolated = interpolator.interpolate_frames(img1_path, img2_path, n_frames)
        all_frames.extend(interpolated)
        
        # Add the second original frame
        original = cv2.imread(img2_path)
        all_frames.append(original)
    
    # Save all frames
    from tqdm import tqdm

    for i, frame in tqdm(enumerate(all_frames), total=len(all_frames), desc="Saving frames"):
        output_path = os.path.join(output_folder, f'frame_{i:04d}.png')
        cv2.imwrite(output_path, frame)
    
    return len(all_frames)

if __name__ == "__main__":
    input_folder = "example"
    output_folder = "outputs"
    n_frames = 1  # Change this number if you want more interpolated frames between each pair
    
    total_frames = batch_interpolate(input_folder, output_folder, n_frames)
    print(f"Processing complete! Generated {total_frames} total frames in {output_folder}")