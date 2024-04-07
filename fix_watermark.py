from PIL import Image
import os
from project_data import processing_folder, tools_folder, output_folder
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def fix_mark(processing_folder, tools_folder, output_folder, img_flip_counter):
    """Function batch processes images in a folder, applying a watermark to each, based on image size.
        Output images have PNG info removed, are assigned a UUID, and are saved in a different folder.
    """

    for basefile in os.listdir(processing_folder):
        base_image = Image.open(processing_folder + "/" + basefile)
        dimensions = base_image.size

        # Image must be square; if not, skip it
        if dimensions[0] != dimensions[1]:
            logger.warning(f"Not a square image. Skipping file {basefile}")
            continue
        else: image_copy = base_image.copy()

        # Watermark must be the right one for each base image
        try:
            watermark_path = tools_folder + f"/watermark_{dimensions[0]}.png"
            watermark = Image.open(watermark_path)
        except FileNotFoundError:
            logger.warning(f"Need watermark for size {dimensions[0]}.  Skipping image {basefile}")
            continue

        logger.info(f"Initial checks OK. Processing started for image {basefile}")

        try:
            # Flip the img every so often
            if img_flip_counter == 3:
                image_copy = image_copy.transpose(Image.FLIP_LEFT_RIGHT)
                img_flip_counter = 1
                logger.info(f"Flipped image: {basefile}")
            else: img_flip_counter += 1

            position = (0,0)
            # This method blends the watermark into the image, using the 3rd argument 
            image_copy.paste(watermark,position,watermark)
            new_uuid = str(uuid.uuid4())
            # Erases potentially sensitive PNG info
            image_copy.info = {}
            image_copy.save(output_folder + "/" + new_uuid + "_marked.png")

            base_image.close()
            image_copy.close()
            watermark.close()
            logger.info(f"Processing done, saved as {new_uuid}, for file {basefile}")

        except Exception as e:
            logger.exception(f"Error processing image: {basefile}")
    return

if __name__ == "__main__":
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename=f'../image_processing/arkiv/app_{now_str}.log',
     filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
     level=logging.INFO)
    
    img_flip_counter = 1  # flip the image every N times (TBD)

    fix_mark(processing_folder, tools_folder, output_folder, img_flip_counter)

    print(f"Image processing completed. Log file name ends in : {now_str}")