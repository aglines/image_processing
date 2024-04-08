from PIL import Image
import os
from project_data import processing_folder, tools_folder, output_folder
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def fix_mark(processing_folder, tools_folder, output_folder, img_flip_counter, skipped_not_square, skipped_no_watermark, total_processed):
    """Function batch processes images in a folder, applying a watermark to each, based on image size.
        Output images have PNG info removed, are assigned a UUID, and are saved in a different folder.
    """

    for basefile in os.listdir(processing_folder):
        base_image = Image.open(processing_folder + "/" + basefile)
        
        # For log readability, replace long filename with shorter version
        # Very little risk for filename collision in this context
        basefile_short = basefile[:15]

        # Image must be square; if not, skip it
        dimensions = base_image.size
        if dimensions[0] != dimensions[1]:
            logger.warning(f"Not a square image. Size {str(dimensions[0])}x{str(dimensions[1])}. Skipping file {basefile_short}")
            skipped_not_square += 1
            continue
        else: image_copy = base_image.copy()

        # Watermark must be the right size for each base image
        try:
            watermark_path = tools_folder + f"/watermark_{dimensions[0]}.png"
            watermark = Image.open(watermark_path)
        except FileNotFoundError:
            logger.warning(f"Need watermark for size {dimensions[0]}.  Skipping file {basefile_short}")
            skipped_no_watermark += 1
            continue

        logger.info(f"Processing started for file {basefile_short}")

        try:
            # Flip the img every so often
            if img_flip_counter == 3:
                image_copy = image_copy.transpose(Image.FLIP_LEFT_RIGHT)
                img_flip_counter = 1
                logger.info(f"Flipped file {basefile_short}")
            else: img_flip_counter += 1

            position = (0,0)
            # This method blends the watermark into the image, using the 3rd argument 
            image_copy.paste(watermark,position,watermark)

            # Filename usually contains the prompt that created the image
            new_uuid = str(uuid.uuid4())

            # Image info contains potentially sensitive data, remove it
            image_copy.info = {}

            # Save image, including metadata like dimension and processing stage it's currently in
            image_copy.save(output_folder + "/" + new_uuid + "_" + str(dimensions[0]) + "_mark.png")

            base_image.close()
            image_copy.close()
            watermark.close()
            logger.info(f"Processing done for file {basefile_short} . Saved as file {new_uuid}")
            total_processed += 1

        except Exception as e:
            logger.exception(f"Error processing file {basefile_short}")

    logger.info(f"Job done. Total: {total_processed}.\nSkipped as not square: {skipped_not_square}.\nSkipped as needs watermark {skipped_no_watermark}.")
    return

if __name__ == "__main__":
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    logging.basicConfig(filename=f'../image_processing/arkiv/app_{now_str}.log',
     filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
     level=logging.INFO)
    
    img_flip_counter = 1  # flip the image horizontally every N times
    skipped_not_square = 0
    skipped_no_watermark = 0
    total_processed = 0
    fix_mark(processing_folder, tools_folder, output_folder, img_flip_counter, skipped_not_square, skipped_no_watermark, total_processed)
    print(f"Job done. Log file ends in : {now_str}")