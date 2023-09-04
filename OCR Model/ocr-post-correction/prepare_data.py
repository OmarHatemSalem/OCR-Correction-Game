'''
# --------------------- REQUIRED: Modify for each dataset and/or experiment ---------------------

# Set test source file (test_tgt is optional, can be used to compute CER and WER of the predicted output)
test_src="sample_dataset/postcorrection/training/test_src1.txt"

# Set experiment parameters
expt_folder="my_expt_singlesource/"

dynet_mem=1000 # Memory in MB available for testing

params="--pretrain_dec --pretrain_s2s --pretrain_enc --pointer_gen --coverage --diag_loss 2"
trained_model_name="my_trained_model"

# ------------------------------END: Required experimental settings------------------------------


# Load the trained model and get the predicted output on the test set (add --dynet-gpu for using GPU)
python postcorrection/multisource_wrapper.py \
--dynet-mem $dynet_mem \
--dynet-autobatch 1 \
--test_src1 $test_src \
$params \
--single \
--vocab_folder $expt_folder/vocab \
--output_folder $expt_folder \
--load_model $expt_folder"/models/"$trained_model_name \
--testing

python utils/prepare_data.py  \
--unannotated_src1 sample_dataset/text_outputs/uncorrected/src1_griko/  \
--unannotated_src2 sample_dataset/text_outputs/uncorrected/src2_italian/  \
--annotated_src1 sample_dataset/text_outputs/corrected/src1_griko/  \
--annotated_src2 sample_dataset/text_outputs/corrected/src2_italian/  \
--annotated_tgt sample_dataset/text_outputs/corrected/tgt_griko/  \
--output_folder sample_dataset/postcorrection
'''


import os

annot_src1=".\\dataset\\text_outputs\\corrected\\src1\\"
unannot_src1=".\\dataset\\text_outputs\\uncorrected\\src1\\"
annot_tgt=".\\dataset\\text_outputs\\corrected\\src1\\"

expt_folder=".\\dataset\\postcorrection\\"

dynet_mem=1000 

params="--pretrain_dec --pretrain_s2s --pretrain_enc --pointer_gen --coverage --diag_loss 2"
trained_model_name="my_trained_model"

prepare = "python utils/prepare_data.py  \
--unannotated_src1 %s  \
--annotated_src1 %s  \
--annotated_tgt %s  \
--output_folder %s" % (unannot_src1, annot_src1, annot_tgt, expt_folder)

os.system(prepare)