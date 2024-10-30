This is my personal use fork of EMA-VFI. If you want to use it, clone the repository and run the script like this:

```bash
cd EMA-VFI
python batch_interpolate.py --input_folder /content/EMA-VFI/example --output_video /content/output.mp4 --n 8
```

You are able to pass it an input folder or video, and output to a folder or video. N is the number of in between frames to generate.
It should automatically detect if you have a GPU, otherwise it will use CPU. Have fun!
