import os
import subprocess
import sys

out_dir = "webp-files"
input_dir = ".\convert"
extensions = (".png", ".jpg", ".jpeg", ".tiff", ".webp")
images = []
failed_images = []
script_dir = os.path.dirname(os.path.realpath(__file__))
libwebp = os.path.join(script_dir, "libwebp", "libwebp-1.4.0", "bin", "cwebp.exe")

def find_image_dir():
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(extensions):
                images.append(file)
    print(images)
    return images

def convert(images, qaulity):
    for image in images:
        print(f"Converting {image}...")
        input_file = os.path.join(input_dir, image)
        output_file = os.path.join(out_dir, os.path.splitext(image)[0] + ".webp")
        try:
            result = subprocess.call(
                [libwebp, "-quiet", "-q", qaulity, input_file, "-o", output_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if result != 0:
                failed_images.append(image)
        except Exception as e:
            print(e)
        
def main():
    qaulity = "75"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        find_image_dir()
    else:
        find_image_dir()

    if len(sys.argv) > 1:
        qaulity = sys.argv[1]
        convert(images, qaulity)
    else:
        convert(images, qaulity)

    converted = os.listdir(out_dir)
    failed = len(failed_images)
    print(f"Converted {len(converted)} image(s) to WebP format.")

    if failed > 0:
        print(f"Failed to convert {failed} image(s):")
        for fail in failed_images:
            print(f"- {fail}")
    exit()
    
main()