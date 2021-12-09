import argparse
# import pdb
import time

from Track_Entry import run

import os.path

# import pickle

## Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--datasetfolder", type=str,
                    help="Input string of dataset folder name. Assumed directory structure is './datasetfolder/(set of images)'",
                    default="BF")
parser.add_argument("-c", "--YeastBaseFolder", type=str, help="Input string of Code directory.",
                    default=r".")  # c:\wisoft\dlls\yeast\code
parser.add_argument("-p", "--make_plot", type=bool,
                    help="Boolean variable to choose whether fluorescence plots are desired", default=False)
parser.add_argument("-s", "--save_experiment", type=bool,
                    help="Boolean variable to choose whether to save a file containing all TImelapse info",
                    default=False)

parser.add_argument("-l", "--save_labels", type=bool,
                    help="Boolean variable to choose whether to save a file containing all TImelapse info",
                    default=True)
parser.add_argument("-t", "--save_track", type=bool,
                    help="Boolean variable to choose whether to save a file containing tracked info", default=False)
parser.add_argument("-r", "--save_pred", type=bool,
                    help="Boolean variable to choose whether to save a file containing segmentation", default=False)
parser.add_argument("-i", "--save_img", type=bool,
                    help="Boolean variable to choose whether to save a file containing the original image",
                    default=False)
parser.add_argument("-o", "--save_overlay", type=bool,
                    help="Boolean variable to choose whether to save a file containing the original image",
                    default=False)

args = parser.parse_args()

from Globals import debug
datasetfolder = args.datasetfolder
makePlots = args.make_plot
saveExp = args.save_experiment
# new args
YeastBaseFolder = args.YeastBaseFolder
save_Labels = args.save_labels
save_Track = args.save_track
save_pred = args.save_pred
save_img = args.save_img
save_overlay = args.save_overlay
if debug:
    with open('prms.txt', 'w') as f:
        f.write("YeastBaseDir " + YeastBaseFolder)
        f.write("\n\rDS " + datasetfolder)
modal_name = 'YNModelParams.pt'
old_path = './Published/'

model_dir = os.path.join(YeastBaseFolder, 'model')
if debug:
    print("wd:" + os.getcwd())
    print("modelDir:" + model_dir)

if os.path.isdir(model_dir):
    model_path = os.path.join(model_dir, modal_name)
elif os.path.isdir(old_path):
    model_path = os.path.join(old_path, model_dir)

if not os.path.isfile(model_path):
    print(r'file model not existing' + model_path)
    exit - 100

if os.path.isdir(datasetfolder):
    if not str.endswith(datasetfolder, '/') and not str.endswith(datasetfolder, '\\'):
        datasetfolder = datasetfolder + '/'
else:
    datasetfolder = './Images/' + datasetfolder + '/'

if not os.path.isdir(datasetfolder):
    print(r'couldn\'t find ds folder at: ' + datasetfolder)
    exit - 101
tl = run(datasetfolder, model_path, saveLabels=save_Labels, saveImage=save_img, saveTrack=save_Track,
         savePred=save_pred,
         saveOverlay=save_overlay, Plot=makePlots, saveExp=saveExp)
# tl = makeTimelapse('./Published/Images/Z2/', model_path, False)
print('done')
