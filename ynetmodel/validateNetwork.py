## Import Libraries and Modules
import torch
import imageio
import numpy as np
import pdb

## Import Custom Code
from Utils.helpers import accuracy

def validate(net, device, testLoader, criterion, saveImages = False):

    ## Run net without regularization techniques
    net.eval()

    ## Loss Sum accumulator for output
    runningIOU = 0

    ## Loop over batches
    for i, data in enumerate(testLoader, 1):
        ## Get inputs and transfer to GPU
        validationImage, mask, _ = data
        validationImage = validationImage.to(device)
       
        ## Run Batch through data with no grad
        with torch.no_grad():
            outputs = net(validationImage.float())
        predictions = outputs.cpu().detach().numpy()[0,:,:,:]
        maskPrediction = (predictions[1] > predictions[0]) * 1

        ## Calculate Accuracy and update running total
        _, IntOfUnion = accuracy(mask.cpu().detach().numpy()[0,:,:,0], maskPrediction)
        runningIOU += IntOfUnion[1]
        
        ## Output Images
        if saveImages:
            
            imageio.imwrite('Validation/' + str(i) + 'Pred.png', maskPrediction.astype(float))
            imageio.imwrite('Validation/' + str(i) + 'IMG.png', validationImage[0,0,:,:].cpu().detach().numpy())
            imageio.imwrite('Validation/' + str(i) + 'True.png', mask[0,:,:,0].cpu().detach().numpy())

    ## Return the mean Loss
    return runningIOU / i










