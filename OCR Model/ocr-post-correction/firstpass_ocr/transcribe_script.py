'''
parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="Path of a single input image for processing.")
    parser.add_argument(
        "--image_folder",
        help="Path of a folder that contains many images for processing.",
    )
    parser.add_argument("--output_folder", help="Output folder for the OCR text.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Enable for JSON output format which includes OCR text and bounding boxes. Default is plain text format.",
    )
'''

import os

image_src = "..\\..\\images"
image_tgt = "..\\..\\images_text"

transcribe = "python transcribe_image.py --image_folder %s --output_folder %s " % (image_src, image_tgt)

os.system(transcribe)