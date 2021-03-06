# -*- coding: utf-8 -*-
"""
Created on Tue Oct 30 13:12:14 2018

@author: ieada
"""

import torch
import numpy as np
from torch.autograd import Variable
import math
import matplotlib.pyplot as plt

xy = np.genfromtxt('data.csv', delimiter=',', dtype='str')
[a,b] = np.shape(xy)
#print(xy[121,:])
#print(a,b,'*')
for i in range(a):
    for j in range(b):
        if xy[i,j] == 'M':
            xy[i,j] = 1
        elif xy[i,j] == 'B':
            xy[i,j] = 0
        elif xy[i,j] == 'nan':
            xy[i,j] = 0

xy = np.float32(xy)
#print(xy[121,:])
x_data = Variable(torch.from_numpy(xy[1:401,2:]))
y_data = Variable(torch.from_numpy(xy[1:401,[1]]))
x_eval = Variable(torch.from_numpy(xy[401:,2:]))
y_gtruth = Variable(torch.from_numpy(xy[401:,[1]]))

#print(np.average(y_gtruth))
#print(x_data.data.shape)
#print(y_data.data)

class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.l1 = torch.nn.Linear(30,25)
        self.l2 = torch.nn.Linear(25,10)
        self.l3 = torch.nn.Linear(10,1)
        self.sigmoid = torch.nn.Sigmoid()
    
    def forward(self, x):
        out1 = self.sigmoid(self.l1(x))
        out2 = self.sigmoid(self.l2(out1))
        y_pred = self.sigmoid(self.l3(out2))
        return y_pred
    
model = Model()
criterion = torch.nn.BCELoss(size_average=True)
optimizer = torch.optim.SGD(model.parameters(), lr = 0.1)

i = 0
n_epoch = 2
y = [0]*n_epoch
x = [0]*n_epoch

for epoch in range(n_epoch):
    y_pred = model(x_data)
    loss = criterion(y_pred,y_data)
    y[i] = loss.data[0]
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    x[i] = i
    i += 1
    

plt.plot(x, y, linewidth=2.0)
plt.show()
length = y_gtruth.data.shape[0]
y2 = [0]*length
x2 = [0]*length
pred_error = criterion(model.forward(x_eval).data[0],y_gtruth.data[0])
for i in range(length):  
    print(y_gtruth.data[i,0]," ",model.forward(x_eval).data[i,0])
    
    #y2[i] = pred_error
    #x2[i] = i
#plt.plot(x2, y2, linewidth=2.0)
#plt.show()
#print("prediction after training:", xy[401:500,[1]], model.forward(x_prediction).data)

## The result shows that maybe we should do PCA to only choose the most relevant features
    