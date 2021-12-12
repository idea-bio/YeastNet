import torch

from ynetmodel.detect import LoadModel

org = LoadModel('../Model/YNMOdelParams.pt')

#script = torch.jit.script(org)
#script.save('model/script.pt')

#trace = torch.jit.trace(org, torch.rand(1,1,1024,1024),)
#trace.save('model/trace.pt')

dummy_input = torch.randn(1, 1, 1024, 1024)
torch.onnx.export(org,dummy_input,"../Model/yeast.onnx")


