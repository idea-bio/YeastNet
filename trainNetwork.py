import torch
from torch.utils.data import Dataset, DataLoader
import torchvision
import torch.nn as nn
import torch.nn.functional as F
from torch import optim

import numpy
import imageio

from processImages import YeastSegmentationDataset
from defineNetwork import Net
from weightedLoss import WeightedCrossEntropyLoss

yeast_dataset = YeastSegmentationDataset()

net = Net()
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
net.to(device)

optimizer = optim.SGD(net.parameters(),
                        lr=0.1,
                        momentum=0.9,
                        weight_decay=0.0005)

criterion = WeightedCrossEntropyLoss()#nn.CrossEntropyLoss()#

trainloader = torch.utils.data.DataLoader(yeast_dataset, batch_size=3,
                                          shuffle=True, num_workers=0)

testloader = torch.utils.data.DataLoader(yeast_dataset, batch_size=3,
                                         shuffle=False, num_workers=0)

classes = ('background','cell')
for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(trainloader, 0):
        # get the inputs
        inputs, labels, loss_weight_map = data
        inputs, labels, loss_weight_map = inputs.to(device), labels.to(device), loss_weight_map.to(device)
        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        outputs = net(inputs.float())

        #print(outputs.detach().numpy().shape)
        #bg = outputs.detach().numpy()[0,0,:,:]
        #cl = outputs.detach().numpy()[0,1,:,:]
        #mk = numpy.zeros((512,512))
        
        #print(cl)
        #print(bg)
        #imageio.imwrite('outputs/' + str(i) + '.png', mk)
        print('outputs')


        loss = criterion(outputs, labels.long(), loss_weight_map)
        print('loss1')
        loss.backward()
        print('loss2')
        optimizer.step()
        print('optimezer')

        # print statistics
        running_loss += loss.item()
        #if i % 5 == 4:    # print every 5 mini-batches
        print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 5))
        running_loss = 0.0

print('Finished Training')

