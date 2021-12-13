## Import Libraries and Modules
import time

import torch
import imageio
import numpy as np
import pdb

## Import Custom Code
from Utils.helpers import accuracy
from ynetmodel.defineNetwork import NetOld

def LoadModel(model_path, device="cpu"):
    net = NetOld()
    net.eval()
    checkpoint = torch.load(model_path, map_location=device)
    net.load_state_dict(checkpoint["network"])
    ## Move Net to GPU
    net.to(device)
    return net

net =  None
def infer(images, num_images, device="cpu", model_path="./model_cp.pt"):
    global net
    st = time.time()
    took=0
    if not net:
        net = LoadModel(model_path,device)
        took =time.time() - st
    from Globals import debug
    if debug:
        print ("took load model"+str(took))
    ## Inference
    output = [None] * num_images

    for idx, image in enumerate(images):
        image = image.to(device)
        st2 = time.time()
        with torch.no_grad():
            output[idx] = net(image)#this line tooks ~5 seconds
        l36=time.time() - st2
        if debug:
            print("took lin 36-39 "+str(l36))
        image = image.to(torch.device("cpu"))
        if debug:
            print("took move image" + str(time.time() - st2-l36))
    return output


def validate(net, device, testLoader, criterion=None, saveImages=False):

    ## Run net without regularization techniques
    net.eval()

    ## Loss Sum accumulator for output
    runningIOU = 0

    ## Loop over batches
    for i, data in enumerate(testLoader, 1):
        ## Get inputs and transfer to GPU
        image, mask, _ = data
        image = image.to(device)
        ## Run Batch through data with no grad
        with torch.no_grad():
            outputs = net(image.float())
        predictions = outputs.cpu().detach().numpy()[0, :, :, :]
        maskPrediction = (predictions[1] > predictions[0]) * 1

        ## Calculate Accuracy and update running total
        _, IntOfUnion = accuracy(mask.cpu().detach().numpy()[0, :, :, 0], maskPrediction)
        runningIOU += IntOfUnion[1]

        ## Output Images
        if saveImages:
            # pdb.set_trace()
            imageio.imwrite(
                "Validation/" + str(i) + "Pred.png", (maskPrediction.astype("uint8")) * 255
            )
            imageio.imwrite(
                "Validation/" + str(i) + "IMG.png",
                (image[0, 0, :, :].cpu().detach().numpy() * 255).astype("uint8"),
            )
            imageio.imwrite(
                "Validation/" + str(i) + "True.png",
                (mask[0, :, :, 0].cpu().detach().numpy() * 255).astype("uint8"),
            )

    ## Return the mean Loss
    return runningIOU / i
