import torch
import pdb

from ynetmodel.defineNetwork import Net


def inferNetwork(images, num_images, device = "cpu", model_path = "./model_cp.pt"):
    ## Instantiate Net, load parameters
    net = Net()
    net.eval()
    checkpoint = torch.load(model_path, map_location=device)
    net.load_state_dict(checkpoint['network'])

    ## Move Net to GPU
    net.to(device)

    ## Inference
    output = [None] * num_images

    for idx, image in enumerate(images):
        image = image.to(device)

        with torch.no_grad():
            output[idx] = net(image)

        image = image.to(torch.device("cpu"))

    return output