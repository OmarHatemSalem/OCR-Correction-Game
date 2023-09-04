from pathlib import Path
import asyncio

import aiopytesseract


# list all available languages by tesseract installation

async def get_languages() -> asyncio.coroutine:
  await aiopytesseract.languages()

asyncio.run(get_languages())

# await aiopytesseract.get_languages()


# # tesseract version
# await aiopytesseract.tesseract_version()
# await aiopytesseract.get_tesseract_version()


# # tesseract parameters
# await aiopytesseract.tesseract_parameters()


# # confidence only info
# await aiopytesseract.confidence("scan1.jpg")


# # deskew info
# await aiopytesseract.deskew("scan1.jpg")


# # extract text from an image: locally or bytes
# await aiopytesseract.image_to_string("scan1.jpg")
# await aiopytesseract.image_to_string(
# 	Path("scan1.jpg").read_bytes(), dpi=220, lang='eng+por'
# )


# # box estimates
# await aiopytesseract.image_to_boxes("scan1.jpg")
# await aiopytesseract.image_to_boxes(Path("scan1.jpg"))


# # boxes, confidence and page numbers
# await aiopytesseract.image_to_data("scan1.jpg")
# await aiopytesseract.image_to_data(Path("scan1.jpg"))


# # information about orientation and script detection
# await aiopytesseract.image_to_osd("scan1.jpg")
# await aiopytesseract.image_to_osd(Path("scan1.jpg"))


# # generate a searchable PDF
# await aiopytesseract.image_to_pdf("scan1.jpg")
# await aiopytesseract.image_to_pdf(Path("scan1.jpg"))


# # generate HOCR output
# await aiopytesseract.image_to_hocr("scan1.jpg")
# await aiopytesseract.image_to_hocr(Path("scan1.jpg"))


# # multi ouput
# async with aiopytesseract.run(
# 	Path('scan1.jpg').read_bytes(),
# 	'output',
# 	'alto tsv txt'
# ) as resp:
# 	# will generate (output.xml, output.tsv and output.txt)
# 	print(resp)
# 	alto_file, tsv_file, txt_file = resp