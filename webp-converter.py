import os
import subprocess
import sys
import platform

out_dir = "webp-files"
input_dir = "convert"
extensions = (".png", ".jpg", ".jpeg", ".tiff", ".webp")
images = []
failed_images = []
script_dir = os.path.dirname(os.path.realpath(__file__))

current_os = platform.system()
if current_os == "Windows":
    libwebp = os.path.join(script_dir, "libwebp", "libwebp-1.4.0", "bin", "cwebp.exe")
elif current_os == "Darwin":
    libwebp = "cwebp"
else:
    libwebp = "cwebp"

def find_image_dir():
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith(extensions):
                images.append(os.path.join(root, file))
    print(f"Found {len(images)} image(s) for conversion.")
    return images

def convert(images, quality):
    for image in images:
        print(f"Converting {image}...")
        input_file = image
        output_file = os.path.join(out_dir, os.path.splitext(os.path.basename(image))[0] + ".webp")
        try:
            result = subprocess.call(
                [libwebp, "-quiet", "-q", str(quality), input_file, "-o", output_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if result != 0:
                failed_images.append(image)
        except Exception as e:
            print(f"Error converting {image}: {e}")

def main():
    quality = 75  
    
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    find_image_dir()
    
    if len(sys.argv) > 1:
        try:
            quality = int(sys.argv[1])
            if not (0 <= quality <= 100):
                raise ValueError
        except ValueError:
            print("Quality must be an integer between 0 and 100.")
            sys.exit(1)
    
    convert(images, quality)
    
    converted = os.listdir(out_dir)
    failed = len(failed_images)
    print(f"Converted {len(converted)} image(s) to WebP format.")
    
    if failed > 0:
        print(f"Failed to convert {failed} image(s):")
        for fail in failed_images:
            print(f"- {fail}")
    
    sys.exit(0)

if __name__ == "__main__":
    main()
