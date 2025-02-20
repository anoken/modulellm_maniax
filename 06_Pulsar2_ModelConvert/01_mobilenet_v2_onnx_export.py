#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import torch

def pytorch_model_to_onnx():
    # MobileNetV2をダウンロードして作成          モデルをPyTorch Hubから取得し、事前学習済みの重みを使用
    model = torch.hub.load('pytorch/vision:v0.14.0', 'mobilenet_v2', pretrained=True)
    model.eval()                               # モデルを評価モードに設定
    
    # ダミー入力を作成                         モデルに入力するためのサンプルデータ（1バッチ、3チャンネル、224x224ピクセル）
    dummy_input = torch.randn(1, 3, 224, 224)
    
    # ONNX形式にエクスポート                  PyTorchモデルをONNX形式に変換
    torch.onnx.export(
        model,                                 # 変換対象のモデル
        dummy_input,                          # モデルの入力データ
        'mobilenet_v2.onnx',            # 出力ファイル名
        export_params=True,                   # 学習済みパラメータを含める
        opset_version=11,                     # ONNXの操作セットバージョン
        input_names=['input'],                # 入力ノードの名前
        output_names=['output']               # 出力ノードの名前
    )
    print("MobileNetV2がONNX形式に変換されました")  # 変換完了メッセージ

if __name__ == "__main__":
    pytorch_model_to_onnx()                   # 関数を実行


