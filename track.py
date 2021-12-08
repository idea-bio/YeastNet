import argparse
import pdb
from Utils.makeTimelapse import makeTimelapse
from Utils.TestPerformance import makeResultsCSV, getMeanAccuracy
from Utils.plotFLTrack import plotFlTrack 
import os.path
import pickle

## Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("-f","--datasetfolder", type=str, help="Input string of dataset folder name. Assumed directory structure is './datasetfolder/(set of images)'", default="BF")
parser.add_argument("-p","--make_plot", type=bool, help="Boolean variable to choose whether fluorescence plots are desired", default=False)
parser.add_argument("-s","--save_experiment", type=bool, help="Boolean variable to choose whether to save a file containing all TImelapse info", default=False)

parser.add_argument("-l","--save_labels", type=bool, help="Boolean variable to choose whether to save a file containing all TImelapse info", default=False)
parser.add_argument("-t","--save_track", type=bool, help="Boolean variable to choose whether to save a file containing tracked info", default=False)
parser.add_argument("-r","--save_pred", type=bool, help="Boolean variable to choose whether to save a file containing segmentation", default=True)
parser.add_argument("-i","--save_img", type=bool, help="Boolean variable to choose whether to save a file containing the original image", default=False)
parser.add_argument("-o","--save_overlay", type=bool, help="Boolean variable to choose whether to save a file containing the original image", default=False)

args = parser.parse_args()

datasetfolder = args.datasetfolder
makePlots = args.make_plot
saveExp = args.save_experiment
#new args
save_Labels = args.save_labels
save_Track = args.save_track
save_pred = args.save_pred
save_img = args.save_img
save_overlay = args.save_overlay

modal_name='YNModelParams.pt'
old_path = './Published/'
model_dir = r'../model/'
if (os.path.isdir(model_dir)):
    model_path =  model_dir+modal_name
elif(os.path.isdir(old_path)):
    model_path= old_path+ model_dir

if not os.path.isfile(model_path):
    print(r'file model existing')
    exit -100

if os.path.isdir(datasetfolder):
    if not str.endswith(datasetfolder, '/') and not str.endswith(datasetfolder,'\\'):
        datasetfolder = datasetfolder+'/'
else:
    datasetfolder ='./Images/' + datasetfolder + '/'
if not os.path.isdir(datasetfolder):
    print(r'could\'t find ds folder at: ' + datasetfolder)
    exit -101
tl = makeTimelapse(datasetfolder  , model_path, saveExp,saveImage=save_img,saveTrack= save_Track,savePred=save_pred,saveOverlay=save_overlay,saveLabels=save_Labels)
#tl = makeTimelapse('./Published/Images/Z2/', model_path, False)

if makePlots:
    plotFlTrack(tl)

print('done')
