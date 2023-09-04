from PIL import Image
import sys

import codecs
import pyocr
import pyocr.builders

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[0]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.

txt = tool.image_to_string(
    Image.open('scan1.jpg'),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
# txt is a Python string
f = open("images\scan1.txt", "w", encoding="utf8")
f.write(txt)
f.close()

line_and_word_boxes = tool.image_to_string(
    Image.open('scan1.jpg'),
    lang=lang,
    builder=pyocr.builders.WordBoxBuilder()
)
print(line_and_word_boxes[0].confidence)


tool = pyocr.get_available_tools()[0]
builder = pyocr.builders.LineBoxBuilder()

line_boxes = tool.image_to_string(
    Image.open('scan1.jpg'),
    lang=lang,
    builder=builder
)
# list of LineBox (each box points to a list of word boxes)

with codecs.open("toto.xml", 'w', encoding='utf-8') as file_descriptor:
    builder.write_file(file_descriptor, line_boxes)

with codecs.open("toto.json", 'w', encoding='utf-8') as file_descriptor:
    builder.write_file(file_descriptor, line_boxes)
# toto.html is a valid XHTML file
