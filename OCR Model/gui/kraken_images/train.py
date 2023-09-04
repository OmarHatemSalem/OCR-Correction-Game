from kraken.lib.train import RecognitionModel, KrakenTrainer

from pytorch_lightning.callbacks import Callback
from PIL import Image


from kraken import blla
from kraken.lib import vgsl, models

from kraken import serialization
from kraken import rpred
import glob


def main():
    # img = "..\\ocr-post-correction\\dataset\\images\\auc_aco000136_000023_d.jpg"
    # im = Image.open(img)

    # model_path = "C:\\Python310\\Lib\\site-packages\\kraken\\blla.mlmodel"
    # model = vgsl.TorchVGSLModel.load_model(model_path)

    # baseline_seg = blla.segment(im, model=model)

    rec_model_path = "C:\\Python310\\Lib\\site-packages\\kraken\\arabic_best.mlmodel"
    # model = models.load_any(rec_model_path)

    # # single model recognition
    # pred_it = rpred.rpred(model, im, baseline_seg)
    # # for record in pred_it:
    # #         print(record)

    # records = [record for record in pred_it]
    # records[0].prediction = 'k'

    # print(records[0].display_order)

    # alto = serialization.serialize(records, image_name=img, image_size=im.size, template='alto')
    # with open('output_2.xml', 'w', encoding="utf-8") as fp:
    #         fp.write(alto)




    ground_truth = glob.glob('.\\*.xml')
    training_files = ground_truth[:250] # training data is shuffled internally
    evaluation_files = ground_truth[250:]
    model = RecognitionModel(training_data=training_files, model=rec_model_path, evaluation_data=evaluation_files, format_type='xml')# ''', augment=True''')
    trainer = KrakenTrainer(enable_progress_bar=True)
    trainer.fit(model)


if __name__ == "__main__":
    main()