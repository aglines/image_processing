from PIL import Image
import os
from project_data import processing_folder, tools_folder, output_folder
import uuid

def fix_mark(processing_folder, tools_folder, output_folder, img_flip_counter):
    """Function batch processes images in a folder, applying a watermark to each, based on image size.
        Output images have PNG info removed, are assigned a UUID, and are saved in a different folder.
    """

    for basefile in os.listdir(processing_folder):
        base_image = Image.open(processing_folder + "/" + basefile)
        dimensions = base_image.size

        # Image must be square; if not, skip it
        if dimensions[0] != dimensions[1]:
            print(f"Not a square image: {basefile}. Skipping.")
            continue
        else: image_copy = base_image.copy()

        # Watermark must be the right one for each base image
        try:
            watermark_path = tools_folder + f"/watermark_{dimensions[0]}.png"
            watermark = Image.open(watermark_path)
        except:
            print(f"Watermark not found for {basefile}, need watermark for {dimensions[0]}. Skipping.")
            continue
        
        # Flip the img every so often
        if img_flip_counter == 3:
            image_copy = image_copy.transpose(Image.FLIP_LEFT_RIGHT)
            img_flip_counter = 1
        else: img_flip_counter += 1


        position = (0,0)
        # This method blends the watermark into the image, using the 3rd argument 
        image_copy.paste(watermark,position,watermark)

        new_uuid = str(uuid.uuid4())

        # Erase the PNG info
        image_copy.info = {}
        image_copy.save(output_folder + "/" + new_uuid + "_marked.png")

        base_image.close()
        image_copy.close()
        watermark.close()
    return

if __name__ == "__main__":
    #logging

    img_flip_counter = 1  # flip the image every N times (TBD)

    fix_mark(processing_folder, tools_folder, output_folder, img_flip_counter)

    print("done")
    
