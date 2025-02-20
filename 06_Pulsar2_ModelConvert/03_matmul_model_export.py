#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import torch
import torch.nn as nn

class MatrixMult(nn.Module):
    def forward(self, matrix, points):
        return torch.matmul(matrix, points)

model = MatrixMult()
torch.onnx.export(model, 
                 (torch.randn(4, 4), torch.randn(4, 1)),
                 "onnx_matmul.onnx",
                 input_names=['matrix', 'points'],
                 output_names=['output'],
                 opset_version=16)

