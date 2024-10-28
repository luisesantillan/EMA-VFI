import cv2
import torch
import sys
import numpy as np
sys.path.append('.')
import config as cfg
from Trainer import Model
from benchmark.utils.padder import InputPadder

class Interpolator:
    def __init__(self):
        cfg.MODEL_CONFIG['LOGNAME'] = 'ours_small_t'
        cfg.MODEL_CONFIG['MODEL_ARCH'] = cfg.init_model_config(
            F = 16,
            depth = [2, 2, 2, 2, 2]
        )
        self.model = Model(-1)
        self.model.load_model()
        self.model.eval()
        if torch.cuda.is_available():
            self.model.device()

    def interpolate_frames(self, image1_path, image2_path, n_frames=1):
        """
        Generate multiple interpolated frames between two input images
        
        Args:
            image1_path: Path to first image
            image2_path: Path to second image
            n_frames: Number of frames to generate between the input images
            
        Returns:
            list: List of interpolated frames in RGB format
        """
        I0 = cv2.imread(image1_path)
        I2 = cv2.imread(image2_path)

        I0_ = (torch.tensor(I0.transpose(2, 0, 1)).cpu() / 255.).unsqueeze(0) if torch.cuda.is_available() else (torch.tensor(I0.transpose(2, 0, 1)).cuda() / 255.).unsqueeze(0)
        I2_ = (torch.tensor(I2.transpose(2, 0, 1)).cpu() / 255.).unsqueeze(0) if torch.cuda.is_available() else (torch.tensor(I2.transpose(2, 0, 1)).cuda() / 255.).unsqueeze(0)

        padder = InputPadder(I0_.shape, divisor=32)
        I0_, I2_ = padder.pad(I0_, I2_)

        # Generate time steps for n frames
        time_steps = [(i+1)*(1./(n_frames+1)) for i in range(n_frames)]
        
        # Generate all intermediate frames
        preds = self.model.multi_inference(I0_, I2_, TTA=False, time_list=time_steps, fast_TTA=False)
        
        # Convert predictions to RGB frames
        frames = []
        for pred in preds:
            frame = (padder.unpad(pred).detach().cpu().numpy().transpose(1, 2, 0) * 255.0).astype(np.uint8)[:, :, ::-1]
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
        return frames

# Example usage
if __name__ == "__main__":
    interpolator = Interpolator()
    # Generate 7 intermediate frames (total sequence will be 9 frames including originals)
    frames = interpolator.interpolate_frames('example/img1.jpg', 'example/img8.jpg', n_frames=7)
    
    # Save all frames
    for i, frame in enumerate(frames):
        cv2.imwrite(f'example/interpolated_frame_{i+1}.jpg', frame)
