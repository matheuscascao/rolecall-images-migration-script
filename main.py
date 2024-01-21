import logging
import os
from dotenv import load_dotenv
from src.config.aws_config import create_s3_client
from src.use_cases.optimize_image import compress_image
from src.config.aws_config import upload_to_s3

load_dotenv()

s3 = create_s3_client()
supported_extensions = ["png", "jpg", "jpeg"]
logging.basicConfig(filename='upload_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def is_file_uploaded(file_path):
    with open('upload_log.txt', 'r') as log_file:
        return any(file_path in line for line in log_file)

def is_supported_file(file_path, supported_extensions):
    # Extract the file extension from the file path
    file_extension = file_path.lower().split('.')[-1]

    # Check if the file extension is in the array of supported extensions
    if file_extension in supported_extensions:
        return True
    else:
        return False

def process_and_upload_to_s3(local_folder_name):
    for file in os.listdir(local_folder_name):
        file_path = os.path.join(local_folder_name, file)
        
        if not is_supported_file(file_path, supported_extensions):
            print(f"File {file_path} is not supported")
            continue

        # if is_file_uploaded(file_path):
        #     continue
        
        compressed_image_path = compress_image(file_path)
        image_link = upload_to_s3(s3, compressed_image_path)

        print(image_link)

        # print(f"File {compressed_image_path} has been uploaded to S3")
        # logging.info(f"File {compressed_image_path} has been uploaded to S3")

        os.remove(compressed_image_path)

        # with open('upload_log.txt', 'a') as log_file:
        #     log_file.write(f"{file_path}\n")


if __name__ == "__main__":
    process_and_upload_to_s3("raw_images")