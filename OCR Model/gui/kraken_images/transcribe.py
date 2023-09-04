from PIL import Image


from kraken import blla
from kraken.lib import vgsl

from kraken.lib import models
from kraken import rpred


import functools

import os
from tqdm import tqdm
import cv2 
import numpy as np
import json

def get_square(lower, upper):
     index_min = np.argmin(np.array([x[1] for x in lower]))
     index_max = np.argmax(np.array([y[1] for y in upper]))
#      b=max([x[1] for x in lower])
#      c=min([y[1] for y in upper])
#      d=max([y[0] for y in upper])
     pos = [tuple(lower[index_min]), tuple(upper[index_max])]
     return pos

def get_line(rline):
     a = min([x[0] for x in rline])
     b = min([x[1] for x in rline])
     c = max([x[0] for x in rline])
     d = max([x[1] for x in rline])

     return [(a,b), (c,d)]




def transcribe(img, output_folder):
        im = Image.open(img)

        model_path = "C:\\Python310\\Lib\\site-packages\\kraken\\blla.mlmodel"
        model = vgsl.TorchVGSLModel.load_model(model_path)

        baseline_seg = blla.segment(im, model=model)

        # print(time.clock() - start)

        # alto = serialization.serialize_segmentatioLib\n(baseline_seg, image_name=im.filename, image_size=im.size, template='alto')
        # with open('segmentation_output.xml', 'w') as fp:
        #         fp.write(alto)

        rec_model_path = "C:\\Python310\\Lib\\site-packages\\kraken\\arabic_best.mlmodel"
        rec_model = models.load_any(rec_model_path)

        pred_it = rpred.rpred(rec_model, im, baseline_seg)

        records = [record for record in pred_it]
        records_pred = [x.prediction for x in records]
        records_cut = [x.cuts for x in records]
        records_conf = [x.confidences for x in records]
        # print(records_pred)

        # print(records_cut[0])
        # print(records_conf[0])
        #print(records[0].line)
        record_lines = []
        for line in records:
              pts = get_line(line.line)
              record_lines.append(pts) 
          #     image = cv2.rectangle(image, pts[0], pts[1], (255,0,0), 2)

                
     #    cv2.namedWindow("output", cv2.WINDOW_NORMAL) 
     #    cv2.imshow('output', image)
     #    cv2.waitKey(0)
        
        records_words = []
        char_dict = {}
        for j in range(len(records)):
             for i in range(len(records[j].prediction)):
                  char_dict["prediction"] = records[j].prediction[i]
                  char_dict["confidence"] = records[j].confidences[i]
                  char_dict["cuts"] = records[j].cuts[i]
                  
                  if (j==0): char_dict["lines"] = [record_lines[j][0], record_lines[j+2][1]]
                  elif (j==len(records)-1): char_dict["lines"] = [record_lines[j-2][0], record_lines[j][1]]
                  else: char_dict["lines"] = [record_lines[j-1][0], record_lines[j+1][1]]

                  
                  records_words.append(char_dict)
                  char_dict = {}

             records_words.append({ 
             "prediction": "\n",
             "confidence": 1.0,
             "cuts": []
             })


        # jsonString = json.dumps(records_words)
        # jsonFile = open("data.json", "w")
        # jsonFile.write(jsonString)
        # jsonFile.close()


        word_dict = {
             "prediction": "",
             "confidence": 1.0,
             "cuts": []
        }

        previous_cut = records_words[0]["cuts"]
        newLine = True
        records_boxes = []
        for j in range(len(records_words)):
             if records_words[j]["prediction"] == ' ':
                  records_boxes.append(word_dict)
                  word_dict["cuts"] = get_square(records_words[j]["cuts"], previous_cut)
                  word_dict = {
                        "prediction": "",
                        "confidence": 1.0,
                        "cuts": []
                  }
                  previous_cut = records_words[j]["cuts"]

             elif records_words[j]["prediction"] == '\n':
                  records_boxes.append(word_dict)
                  word_dict["cuts"] = get_square(word_dict["cuts"], previous_cut)
                  word_dict = {
                        "prediction": "",
                        "confidence": 1.0,
                        "cuts": []
                  }
                  if j < len(records_words)-1: previous_cut = records_words[j+1]["cuts"]
                  else: previous_cut = word_dict["cuts"]
             else:
                  word_dict["prediction"] += records_words[j]["prediction"] 
                  word_dict["confidence"] = min(word_dict["confidence"], records_words[j]["confidence"]) 
                  word_dict["cuts"] = records_words[j]["cuts"]
                  word_dict["lines"] = records_words[j]["lines"]


        red = (0, 0, 255)
        blue = (255, 0, 0)
        thickness = 2
        window_name = 'Image'

        counter = 0
        for box in tqdm(records_boxes):
               if box["confidence"] < 0.75:
                    box["corrected"] = False
                    image = cv2.imread(img)
                    # image = cv2.rectangle(image, box["lines"][0], box["lines"][1], blue, thickness)
                    image = cv2.rectangle(image, box["cuts"][0], box["cuts"][1], red, thickness)
                    image = image[box["lines"][0][1]:box["lines"][1][1], box["lines"][0][0]:box["lines"][1][0]]
                    if (counter == 0):
                         cv2.imshow(window_name, image)
                         cv2.waitKey(0)
                    if not os.path.exists(output_folder):
                              os.makedirs(output_folder)

                    filename, _ = os.path.splitext(img.split("\\")[-1])

                    cv2.imwrite("".join([output_folder, "\\", filename, str(counter), "_correction.jpg"]), image)
                    counter += 1


def processBook(input_folder):
        output_folder = input_folder.split("\\")[:-1]
        output_folder.append("txt_kraken")
        output_folder = functools.reduce(lambda x,y: x+"\\"+y, output_folder)
        output_folder += "\\"

        imgs = [] 
        for filename in os.listdir(input_folder):
                f = os.path.join(input_folder, filename)
                if os.path.isfile(f):
                        imgs.append(f)



        for img in tqdm(imgs):
                transcribe(img, output_folder)


def update_dataset(txt_obj, idx):

     fileObject = open("data.json", "r")
     jsonContent = fileObject.read()
     aList = json.loads(jsonContent) if jsonContent else []
     title = aList[idx]["directory"]+txt_obj["name"]+'.json' 

     fileObject1 = open(title, "r")
     jsonContent1 = fileObject1.read()
     aList1 = json.loads(jsonContent1) if jsonContent1 else []

     id = txt_obj["id"]
     aList1[id] = txt_obj


     jsonString = json.dumps(aList1)
     jsonFile = open(title, "w")
     jsonFile.write(jsonString)
     jsonFile.close()