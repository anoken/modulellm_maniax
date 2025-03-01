## Copyright (c) 2025 aNoken

import axengine as axe
import numpy as np
import cv2
import argparse
from dataclasses import dataclass

# COCOデータセットの80クラス名リスト
COCO_CLASSES = [
   'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 
   'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 
   'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
   'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 
   'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 
   'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
   'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 
   'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 
   'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 
   'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 
   'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 
   'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 
   'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

@dataclass
class Object:
   bbox: list    # バウンディングボックス[x, y, w, h]
   label: int    # クラスID（COCOデータセットの80クラスに対応）
   prob: float   # 検出確率（0-1の範囲）

def preprocess(image_path, input_size):
   #入力画像の前処理を行う 
   image = cv2.imread(image_path)
   if image is None:
       raise FileNotFoundError(f"画像ファイルを読み取れませんでした: {image_path}")
   original_shape = image.shape[:2]

   #Pulsar2の変換パラメータによっては、以下は不要
   #M5Stackのllm-yolo_1.4-m5stack1_arm64.deb内のaxmodelを使う場合は必要
   image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

   resized_image = cv2.resize(image, input_size)
   input_tensor = np.expand_dims(resized_image, axis=0).astype(np.uint8)
   return input_tensor, original_shape, image

def postprocess(outputs, original_shape, input_size, confidence_threshold, 
               nms_threshold, reg_max=16):
   # モデル出力の後処理を行う 
   # モデル出力を処理して検出候補を取得
   detections = []
   bbox_channels = 4 * reg_max

   # 各特徴マップレベル（8、16、32ストライド）での処理
   for output in outputs:
       batch_size, grid_h, grid_w, channels = output.shape
       stride = input_size[0] // grid_h

       # バウンディングボックスとクラス予測を分離
       bbox_part = output[:, :, :, :bbox_channels]
       bbox_part = bbox_part.reshape(batch_size, grid_h, grid_w, 4, reg_max)
       bbox_part = bbox_part.reshape(grid_h * grid_w, 4, reg_max)

       class_part = output[:, :, :, bbox_channels:]
       class_part = class_part.reshape(batch_size, grid_h * grid_w, 80)

       # グリッドセルごとの検出処理
       for i in range(grid_h * grid_w):
           h, w = i // grid_w, i % grid_w
           scores = class_part[0, i, :]
           class_id = np.argmax(scores)
           box_prob = 1 / (1 + np.exp(-scores[class_id]))

           if box_prob < confidence_threshold:
               continue

           # バウンディングボックスのデコード
           bbox = bbox_part[i]
           x0 = (w + 0.5 - decode_distributions(bbox[0])) * stride
           y0 = (h + 0.5 - decode_distributions(bbox[1])) * stride
           x1 = (w + 0.5 + decode_distributions(bbox[2])) * stride
           y1 = (h + 0.5 + decode_distributions(bbox[3])) * stride

           # 元の画像サイズにスケーリング
           scale_x = original_shape[1] / input_size[0]
           scale_y = original_shape[0] / input_size[1]
           x0 = np.clip(x0 * scale_x, 0, original_shape[1])
           y0 = np.clip(y0 * scale_y, 0, original_shape[0])
           x1 = np.clip(x1 * scale_x, 0, original_shape[1])
           y1 = np.clip(y1 * scale_y, 0, original_shape[0])

           detections.append(Object(
               bbox=[float(x0), float(y0), float(x1-x0), float(y1-y0)],
               label=int(class_id),
               prob=float(box_prob)
           ))

   if not detections:
       return []

   # 非最大値抑制による重複検出の除去
   boxes = np.array([d.bbox for d in detections])
   scores = np.array([d.prob for d in detections])
   class_ids = np.array([d.label for d in detections])
   
   final_detections = []
   for cls in np.unique(class_ids):
       idxs = np.where(class_ids == cls)[0]
       if len(idxs) == 0:
           continue

       # クラスごとにNMSを適用
       cls_boxes = boxes[idxs]
       cls_scores = scores[idxs]
       keep = []
       order = cls_scores.argsort()[::-1]

       while order.size > 0:
           i = order[0]
           keep.append(i)
           if order.size == 1:
               break

           # IoU（Intersection over Union）の計算
           xx1 = np.maximum(cls_boxes[i, 0], cls_boxes[order[1:], 0])
           yy1 = np.maximum(cls_boxes[i, 1], cls_boxes[order[1:], 1])
           xx2 = np.minimum(cls_boxes[i, 0] + cls_boxes[i, 2],
                          cls_boxes[order[1:], 0] + cls_boxes[order[1:], 2])
           yy2 = np.minimum(cls_boxes[i, 1] + cls_boxes[i, 3],
                          cls_boxes[order[1:], 1] + cls_boxes[order[1:], 3])

           w = np.maximum(0, xx2 - xx1)
           h = np.maximum(0, yy2 - yy1)
           intersection = w * h
           union = (cls_boxes[i, 2] * cls_boxes[i, 3] + 
                   cls_boxes[order[1:], 2] * cls_boxes[order[1:], 3] - 
                   intersection)
           iou = intersection / union

           # IoUが閾値以下の検出を保持
           inds = np.where(iou <= nms_threshold)[0]
           order = order[inds + 1]

       for idx in keep:
           final_detections.append(detections[idxs[idx]])

   return final_detections

def sigmoid(x):
   # シグモイド関数の実装
   return 1 / (1 + np.exp(-x))

def softmax(x, axis=-1):
   # 数値的に安定なソフトマックス関数の実装
   x = x - np.max(x, axis=axis, keepdims=True)
   e_x = np.exp(x)
   return e_x / np.sum(e_x, axis=axis, keepdims=True)

def decode_distributions(feat, reg_max=16):
   # Distribution Focal Loss (DFL)の出力をデコード
   prob = softmax(feat, axis=-1)
   return np.sum(prob * np.arange(reg_max), axis=-1)

def main(args):
   #  1. 画像の前処理
   input_tensor, original_shape, original_image = preprocess(
       args.image, (args.input_size, args.input_size))

   #  2. モデルによる推論
   session = axe.InferenceSession(args.model)
   outputs = session.run(None, {session.get_inputs()[0].name: input_tensor})

   #  3. 検出結果の後処理
   detections = postprocess(
       outputs, original_shape, (args.input_size, args.input_size),
       args.conf_threshold, args.nms_threshold)

   # 4. 結果の可視化と保存
   for det in detections:
       x, y, w, h = map(int, det.bbox)
       label = f"{COCO_CLASSES[det.label]}: {det.prob:.2f}"
       cv2.rectangle(original_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
       cv2.putText(original_image, label, (x, y - 10),
                  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
   
   cv2.imwrite(args.output, cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description='YOLO11 Object Detection')
   parser.add_argument('--model', 
                      default='/opt/m5stack/data/yolo11n/yolo11n.axmodel')
   parser.add_argument('--image', 
                      default='/opt/data/npu/images/dog.jpg')
   parser.add_argument('--output',
                      default='output_ax.jpg')
   parser.add_argument('--input-size', type=int, default=320)
   parser.add_argument('--conf-threshold', type=float, default=0.45)
   parser.add_argument('--nms-threshold', type=float, default=0.45)
   
   args = parser.parse_args()
   main(args)
