import logging
import os
from dotenv import load_dotenv
import csv
from src.config.aws_config import create_s3_client
from src.use_cases.optimize_image import compress_image
from src.config.aws_config import upload_to_s3

load_dotenv()

s3 = create_s3_client()
supported_extensions = ["png", "jpg", "jpeg", "heic"]
logging.basicConfig(filename='upload_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def verify_file_uploaded(file_path, log_file_path='logs/output_file_path.csv'):
    with open(log_file_path, 'r') as log_file:
        return any(file_path in line for line in log_file)

def verify_supported_file(file_path, supported_extensions):
    file_extension = file_path.lower().split('.')[-1]

    # Check if the file extension is in the array of supported extensions
    return file_extension in supported_extensions

def process_and_upload_to_s3(folder_path, file_name, output_log_file, errors_log_file):
    file_path = folder_path + file_name
    # if not verify_supported_file(file_path, supported_extensions):
    #     errors_log_file.write(f"{file_name},Unsupported file type\n")
    #     errors_log_file.flush()
    #     return

    try:
        is_file_uploaded = verify_file_uploaded(file_name)
        if is_file_uploaded:
            return

        compressed_image_path = compress_image(file_path)
        image_link = upload_to_s3(s3, compressed_image_path)

        # print(image_link)
        # print(f"File    {compressed_image_path} has been uploaded to S3")
        # logging.info(f"File {compressed_image_path} has been uploaded to S3")

        os.remove(compressed_image_path)

        output_log_file.write(f"{file_name}\n")
        output_log_file.flush()  # Flush the buffer to ensure immediate write to the file

    except Exception as e:
        errors_log_file.write(f"{file_name},{str(e)}\n")
        errors_log_file.flush()

if __name__ == "__main__":
    logs_folder_path = 'logs/'
    input_csv_path = logs_folder_path+'input_file_path.csv'
    output_csv_path = logs_folder_path+'output_file_path.csv'
    errors_csv_path = logs_folder_path+'errors.csv'
    images_folder_path = 'raw_images/'

    with open(output_csv_path, 'a') as output_log_file, open(errors_csv_path, 'a') as errors_log_file:
        csv_file = open(input_csv_path, 'r')
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            image_name = row['file_path']
            process_and_upload_to_s3(folder_path=images_folder_path, file_name=image_name, output_log_file=output_log_file, errors_log_file=errors_log_file)

        csv_file.close()
