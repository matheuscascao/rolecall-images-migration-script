from PIL import Image
import os
import tempfile

def compress_image(image_path: str) -> str:
    filepath = os.path.join(os.getcwd(), image_path)
    original_name = os.path.basename(filepath)
    original_name_without_extension, _ = os.path.splitext(original_name)

    image = Image.open(filepath)

    # Save compressed image to a temporary location without a random string
    temp_file = os.path.join(tempfile.gettempdir(), f"{original_name_without_extension}.webp")
    image.save(temp_file, "WEBP", optimize=True, quality=85)

    image.close()

    return temp_file