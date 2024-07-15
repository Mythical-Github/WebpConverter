from PIL import Image
import imageio.v2 as imageio
import numpy as np
import os
import sys

def check_webp_format(file_path):
    try:
        with Image.open(file_path) as img:
            if img.format != 'WEBP':
                print(f"{file_path} is not a WebP file.")
                return
            
            base_name = os.path.splitext(file_path)[0]

            if img.n_frames > 1:
                print(f"{file_path} is an animated WebP (video) with {img.n_frames} frames.")
                frames = []
                for frame in range(img.n_frames):
                    img.seek(frame)
                    frames.append(np.array(img.convert("RGB")))
                
                output_path = f"{base_name}.mp4"
                imageio.mimsave(output_path, frames, fps=24)
                print(f"Converted {file_path} to {output_path}.")
            else:
                print(f"{file_path} is a single frame WebP (image).")
                output_path = f"{base_name}.png"
                img.save(output_path, "PNG")
                print(f"Converted {file_path} to {output_path}.")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    if hasattr(sys, 'frozen'):
        executable_path = os.path.dirname(sys.executable)
    else:
        executable_path = os.path.dirname(os.path.abspath(__file__))
    
    if len(sys.argv) < 2:
        print(f"Usage: {sys.executable} <path_to_webp_file> [<path_to_webp_file> ...]")
    else:
        for file_path in sys.argv[1:]:
            check_webp_format(file_path)
