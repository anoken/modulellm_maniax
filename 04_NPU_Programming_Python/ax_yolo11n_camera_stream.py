## Copyright (c) 2025 aNoken

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import axengine as axe
import time
import argparse
from dataclasses import dataclass

app = FastAPI()

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
    bbox: list
    label: int
    prob: float

def process_frame(frame: np.ndarray, input_size: int) -> tuple:
    """フレームの前処理を行う"""
    original_shape = frame.shape[:2]
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, (input_size, input_size))
    return np.expand_dims(resized, 0), original_shape, rgb

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x, axis=-1):
    x = x - np.max(x, axis=axis, keepdims=True)
    e_x = np.exp(x)
    return e_x / np.sum(e_x, axis=axis, keepdims=True)

def decode_distributions(feat, reg_max=16):
    prob = softmax(feat, axis=-1)
    return np.sum(prob * np.arange(reg_max), axis=-1)

def postprocess(outputs, original_shape, input_size, conf_threshold=0.45,
               nms_threshold=0.45, reg_max=16):
    """検出結果の後処理を行う"""
    detections = []
    bbox_channels = 4 * reg_max

    for output in outputs:
        batch_size, grid_h, grid_w, channels = output.shape
        stride = input_size // grid_h
        bbox_part = output[:, :, :, :bbox_channels]
        bbox_part = bbox_part.reshape(batch_size, grid_h, grid_w, 4, reg_max)
        bbox_part = bbox_part.reshape(grid_h * grid_w, 4, reg_max)
        class_part = output[:, :, :, bbox_channels:]
        class_part = class_part.reshape(batch_size, grid_h * grid_w, 80)

        for i in range(grid_h * grid_w):
            h, w = i // grid_w, i % grid_w
            scores = class_part[0, i, :]
            class_id = np.argmax(scores)
            box_prob = 1 / (1 + np.exp(-scores[class_id]))

            if box_prob < conf_threshold:
                continue

            bbox = bbox_part[i]
            x0 = (w + 0.5 - decode_distributions(bbox[0])) * stride
            y0 = (h + 0.5 - decode_distributions(bbox[1])) * stride
            x1 = (w + 0.5 + decode_distributions(bbox[2])) * stride
            y1 = (h + 0.5 + decode_distributions(bbox[3])) * stride

            scale_x = original_shape[1] / input_size
            scale_y = original_shape[0] / input_size
            x0 = np.clip(x0 * scale_x, 0, original_shape[1])
            y0 = np.clip(y0 * scale_y, 0, original_shape[0])
            x1 = np.clip(x1 * scale_x, 0, original_shape[1])
            y1 = np.clip(y1 * scale_y, 0, original_shape[0])

            detections.append(Object(
                bbox=[float(x0), float(y0), float(x1-x0), float(y1-y0)],
                label=int(class_id),
                prob=float(box_prob)
            ))

    return apply_nms(detections, nms_threshold)

def apply_nms(detections, nms_threshold):
    """非最大値抑制を適用"""
    if not detections:
        return []

    boxes = np.array([d.bbox for d in detections])
    scores = np.array([d.prob for d in detections])
    class_ids = np.array([d.label for d in detections])
    
    final_detections = []
    for cls in np.unique(class_ids):
        idxs = np.where(class_ids == cls)[0]
        if len(idxs) == 0:
            continue

        cls_boxes = boxes[idxs]
        cls_scores = scores[idxs]
        keep = []
        order = cls_scores.argsort()[::-1]

        while order.size > 0:
            i = order[0]
            keep.append(i)
            if order.size == 1:
                break

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
            inds = np.where(iou <= nms_threshold)[0]
            order = order[inds + 1]

        for idx in keep:
            final_detections.append(detections[idxs[idx]])

    return final_detections

def draw_detections(frame, detections):
    """検出結果を画像に描画"""
    for det in detections:
        x, y, w, h = map(int, det.bbox)
        label = f"{COCO_CLASSES[det.label]}: {det.prob:.2f}"
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, label, (x, y - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return frame

def get_video_stream(model_path: str, input_size: int):
    """ビデオストリームを生成"""
    session = axe.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    camera = cv2.VideoCapture(0)

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            input_tensor, shape, rgb = process_frame(frame, input_size)
            outputs = session.run(None, {input_name: input_tensor})
            detections = postprocess(outputs, shape, input_size)
            frame_with_det = draw_detections(frame, detections)

            _, buffer = cv2.imencode('.jpg', frame_with_det)
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + 
                  buffer.tobytes() + b'\r\n')
            time.sleep(0.005)
    finally:
        camera.release()

@app.get("/video")
async def video_endpoint(
    model: str = '/opt/m5stack/data/yolo11n/yolo11n.axmodel',
    input_size: int = 320
):
    """ビデオストリーミングのエンドポイント"""
    return StreamingResponse(
        get_video_stream(model, input_size),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YOLO11n Detection')
    parser.add_argument(
        '--model',
        default='/opt/m5stack/data/yolo11n/yolo11n.axmodel',
        help='モデルファイルのパス'
    )
    parser.add_argument(
        '--input-size',
        type=int,
        default=320,
        help='入力画像サイズ'
    )
    
    args = parser.parse_args()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)