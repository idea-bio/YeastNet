import torch
import os
from ynetmodel.detect import LoadModel


modelPath = 'C:\code\YeastNet\Model\YeastNet2Param.pt'
assert os.path.exists(modelPath)
org = LoadModel(modelPath)
script = torch.jit.script(org)

#script.save('model/script.pt')
#trace = torch.jit.trace(org, torch.rand(1,1,1024,1024),)
#trace.save('model/trace.pt')

dummy_input = torch.randn(1, 1, 1024, 1024)
folder = "C:\code\YeastNet\Model"
if not os.path.exists(folder):
    os.mkdir(folder)
f = os.path.join(folder, "yeast.onnx")
torch.onnx.export(model=script,
                  args=dummy_input,
                  example_outputs=dummy_input,
                  f=f,
                  input_names= ['input'] , output_names=['output'],
                  dynamic_axes={'input':{2:'width',
                                         3:'height'},
                                    #the output 1ts index is always 2 of the  input 1ts but is dynamic becouse of bug
                                  'output':{1:'lables',
                                            2:'width',
                                            3:'height'
                                            }}
                  )

f = os.path.join(folder, "yeast_org.onnx")
torch.onnx.export(org,dummy_input,f=f)
print(f"save file to {f}")