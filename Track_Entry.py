from Utils.makeTimelapse import makeTimelapse
from Utils.plotFLTrack import plotFlTrack
import numpy as np#import for C#, uses it...
# C# entry point


def run(imagedir, modelPath, saveLabels=True, saveImage=False, saveTrack=False, savePred=False, saveOverlay=False,Plot=False,saveExp=False):
    if not str.endswith(imagedir, '/') and not str.endswith(imagedir, '\\'):
        imagedir = imagedir+ '/'
    tl= makeTimelapse(imagedir, model_path= modelPath, saveExp= saveExp,
                  saveImage=saveImage, saveTrack=saveTrack, savePred=savePred,
                  saveOverlay=saveOverlay, saveLabels=saveLabels)
    if Plot:
       plotFlTrack(tl)
    return  tl
    #label=tl.labels[0].astype(np.uint16)
    #return label.shape, label.flatten()
    #return  tl
