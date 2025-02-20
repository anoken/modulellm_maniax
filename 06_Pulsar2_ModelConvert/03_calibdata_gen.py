#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import torch
import torch.nn as nn
import numpy as np
import os
import tarfile

class MatrixMult(nn.Module):
    def forward(self, matrix, points): return torch.matmul(matrix, points)

def generate_test_data():
    # 1点の点群と変換行列を生成
    points = np.random.uniform(-1, 1, (4, 1)).astype(np.float32)
    matrix = np.random.uniform(-1, 1, (4, 4)).astype(np.float32)
    
    temp_files = []
    try:
        # 10個のデータセット生成
        for i in range(10):
            points_file = f'points_{i:02d}.npy'
            matrix_file = f'matrix_{i:02d}.npy'
            
            np.save(points_file, points)
            np.save(matrix_file, matrix)
            temp_files.extend([points_file, matrix_file])
        
        # tarファイル作成
        for prefix in ['points', 'matrix']:
            with tarfile.open(f'{prefix}_data.tar', 'w') as tar:
                for i in range(10):
                    filename = f'{prefix}_{i:02d}.npy'
                    if os.path.exists(filename):
                        tar.add(filename)
                        
    finally:
        # 一時ファイル削除
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)


os.chdir("dataset")
# データ生成とモデルエクスポート
generate_test_data()
