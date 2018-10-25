## Import Librarys and Modules
import torch
from torch.utils.data import DataLoader
from torch import optim
import tensorboardX as tbX
import pdb
import random
import time

## Import Custom Modules
import processImages as pi
import validateNetwork as valNet

## Import Custom Classes
from processImages import YeastSegmentationDataset
from defineNetwork import Net
from weightedLoss import WeightedCrossEntropyLoss

## Start Timer
start_time = time.time()

## Launch Tensorboard Summary Writing Object
writer = tbX.SummaryWriter()#log_dir="./logs")

## Make Test and Validation Partitions
samplingList = list(range(pi.num_images()))

trainingIDs = random.sample(samplingList,130)
testIDs = random.sample(samplingList,29)

## Instantiate Net, Load Parameters, Move Net to GPU
net = Net()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)
net.load_state_dict(torch.load("good_model.pt"))

## Instantiate Training and Validation DataLoaders
trainDataSet = YeastSegmentationDataset(trainingIDs, crop_size = 128)
trainLoader = torch.utils.data.DataLoader(trainDataSet, batch_size=1,
                                          shuffle=False, num_workers=0)

testDataSet = YeastSegmentationDataset(testIDs, crop_size = 512)
testLoader = torch.utils.data.DataLoader(testDataSet, batch_size=1,
                                         shuffle=False, num_workers=0)


## Set Training hyperparameters/conditions
optimizer = optim.SGD(net.parameters(), lr=0.1)#, momentum=0.9, weight_decay=0.0005)
criterion = WeightedCrossEntropyLoss()#nn.CrossEntropyLoss()#
classes = ('background','cell')
iteration = 0

# Epoch Loop: first loops over batches, then over v alidation set
for epoch in range(10):  
    
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
        writer.add_scalar('loss', loss.item(), iteration)
        
        ## Backpropagate Loss
        loss.backward()
        print('Backpropagation Done')

        for param in net.parameters():
            print(param.grad.data.sum())
        
        pdb.set_trace()
        ## Update Parameters
        optimizer.step()
        print('optimizer')


    ## Epoch validation
    #print('Validating.... Please Hold')
    #val_loss = valNet.validate(net, device, testLoader, criterion, saveImages=True)
    #print('[%d, %d] loss: %.5f' % (iteration, epoch + 1, val_loss))
    
    ## Save Model 
    #if save_at_cp:
        #torch.save(net.state_dict(),  "model.pt")

## Finish
elapsed_time = time.time() - start_time
print('Finished Training, Duration: seconds' + str(format(elapsed_time, '02d')))
writer.close()
torch.save(net.state_dict(),  "model.pt")
