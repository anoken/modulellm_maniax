## Copyright (c) 2025 aNoken

import cv2
import numpy as np
import axengine as axe
import argparse

def process_depth_map(input_path, output_path, model_path):
   # 入力画像の読み込みとリサイズ
   frame = cv2.imread(input_path)
   frame = cv2.resize(frame, (384, 256))
   input_tensor = np.expand_dims(frame[..., ::-1], axis=0)
   
   # 深度推定の実行
   session = axe.InferenceSession(model_path)
   depth_map = session.run(None, {session.get_inputs()[0].name: input_tensor})[0]
   
   # 深度マップの可視化
   depth_feature = depth_map.reshape(depth_map.shape[-2:])
   normalized = (depth_feature - depth_feature.min()) / \
               (depth_feature.max() - depth_feature.min())
   depth_colored = cv2.applyColorMap(
       (normalized * 255).astype(np.uint8), 
       cv2.COLORMAP_INFERNO
   )
   depth_resized = cv2.resize(depth_colored, (frame.shape[1], frame.shape[0]))
   
   # 結果を保存
   cv2.imwrite(output_path, np.concatenate([frame, depth_resized], axis=1))

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='画像の深度マップを生成します')
   parser.add_argument(
       '--input', 
       default='/opt/data/npu/images/dog.jpg',
       help='入力画像のパス'
   )
   parser.add_argument(
       '--output',
       default='output.jpg',
       help='出力画像のパス'
   )
   parser.add_argument(
       '--model',
       default='/opt/m5stack/data/depth-anything-ax630c/depth_anything.axmodel',
       help='モデルファイルのパス'
   )
   
   args = parser.parse_args()
   process_depth_map(args.input, args.output, args.model)