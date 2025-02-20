#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

from ultralytics import YOLO

# モデルを読み込む
model = YOLO("yolo11n.pt")
# モデルの情報を表示
model.info()
# ONNX形式にエクスポート（画像サイズ320x320）
model.export(format='onnx', simplify=True, opset=17, imgsz=[320, 320])


