## Import Librarys and Modules
import torch
from torch.utils.data import DataLoader
from torch import optim
import tensorboardX as tbX
import pdb
import random
import time
import numpy

## Import Custom Modules
import processImages as pi
import validateNetwork as valNet

## Import Custom Classes
from processImages import YeastSegmentationDataset
from defineNetwork import Net
from weightedLoss import WeightedCrossEntropyLoss

## Start Timer, Tensorboard
start_time = time.time()
writer = tbX.SummaryWriter()#log_dir="./logs")
resume = True

## Instantiate Net, Load Parameters, Move Net to GPU
net = Net()
optimizer = optim.SGD(net.parameters(), lr=0.01)#, momentum=0.9)

##Send Model to GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)

## Load State
if resume==False:
    ## Make Test and Validation Partitions
    samplingList = list(range(pi.numImages()))
    samples = random.sample(samplingList,153)
    trainIDs = samples[:129]
    testIDs = samples[130:]
    iteration = 0 #30634
    start = 0 # 1803
else:
    checkpoint = torch.load("model_cp.pt")
    testIDs = checkpoint['testID']
    trainIDs = checkpoint['trainID']
    iteration = checkpoint['iteration']
    start = checkpoint['epoch']
    net.load_state_dict(checkpoint['network'])
    optimizer.load_state_dict(checkpoint['optimizer'])
    #batchIDs = numpy.load('batchIDs.npy').item()
    #testIDs = batchIDs['test']
    #trainIDs = batchIDs['train']
    #iteration = 30634
    #start = 1803
    #optimizer.load_state_dict(torch.load('model_opt.pt'))
    #net.load_state_dict(torch.load('model.pt'))

## Instantiate Training and Validation DataLoaders
trainDataSet = YeastSegmentationDataset(trainIDs, crop_size = 256, random_rotate = True)
trainLoader = torch.utils.data.DataLoader(trainDataSet, batch_size=8,
                                          shuffle=True, num_workers=0)

testDataSet = YeastSegmentationDataset(testIDs, crop_size = 512)
testLoader = torch.utils.data.DataLoader(testDataSet, batch_size=1,
                                         shuffle=False, num_workers=0)

## Set Training hyperparameters/conditions
criterion = WeightedCrossEntropyLoss()
classes = ('background','cell')


## Epoch Loop: first loops over batches, then over v alidation set
for epoch in range(start,10000):  
    
    ## Batch Loop
    for i, data in enumerate(trainLoader, 0):
        ## Total iteration
        iteration+=1

        ## Get inputs
        trainingImage, mask, lossWeightMap = data
        trainingImage, mask, lossWeightMap = trainingImage.to(device), mask.to(device), lossWeightMap.to(device)

        ## Zero the parameter gradients
        optimizer.zero_grad()

        ## Forward Pass
        outputs = net(trainingImage.float())
        print('Forward Pass')

        ## Write Graph
        writer.add_graph(net, trainingImage.float())

        ## Calculate and Write Loss
        loss = criterion(outputs, mask.long(), lossWeightMap)
        print('Loss Calculated:', loss.item())
        writer.add_scalar('Batch Loss', loss.item(), iteration)
        
        ## Backpropagate Loss
        loss.backward()
        print('Backpropagation Done')

        ## Update Parameters
        optimizer.step()
        print('optimizer')


    ## Epoch validation
    print('\n\nValidating.... Please Hold')
    val_acc = valNet.validate(net, device, testLoader, criterion, saveImages=True)
    print('[%d, %d] IntOfUnion (Cell): %.5f \n\n' % (iteration, epoch + 1, val_acc))
    writer.add_scalar('Validation Cell IOU', val_acc, epoch)
    ## Save Model 
    #if True #saveCP:
    checkpoint = {
        "network": net.state_dict(),
        "optimizer": optimizer.state_dict(),
        "trainID": trainIDs,
        "testID": testIDs,
        "epoch": epoch,
        "iteration": iteration
    }
    pdb.set_trace()
    torch.save(checkpoint, "model_cp.pt")
## Finish
elapsed_time = time.time() - start_time
print('Finished Training, Duration: seconds' + str(elapsed_time))
writer.close()
