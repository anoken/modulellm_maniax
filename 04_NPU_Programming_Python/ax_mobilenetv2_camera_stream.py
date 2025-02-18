## Copyright (c) 2025 aNoken

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import axengine as axe
import time
import argparse

app = FastAPI()

def process_frame(frame: np.ndarray, size=(224, 224)) -> np.ndarray:
    """フレームを前処理する"""
    if frame is None:
        raise ValueError("フレームの読み込みに失敗しました")
        
    # BGRからRGBに変換
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 正方形にクロップ
    h, w = rgb.shape[:2]
    crop = min(w, h)
    x = (w - crop) // 2
    y = (h - crop) // 2
    cropped = rgb[y:y+crop, x:x+crop]
    
    # リサイズしてバッチ次元を追加
    resized = cv2.resize(cropped, size)
    return np.expand_dims(resized, 0)

def get_top_k_predictions(output, k=5):
    """上位k個の予測結果を取得する"""
    output_flat = output[0].flatten()
    idx = np.argsort(output_flat)[-k:][::-1]
    scores = output_flat[idx]
    return idx, scores

def draw_predictions(frame, indices, scores):
    """予測結果を画像に描画する"""
    h, w = frame.shape[:2]
    y_offset = 30
    
    for i, (idx, score) in enumerate(zip(indices, scores)):
        text = f"Class {idx}: {score:.4f}"
        y = y_offset + (i * 30)
        cv2.putText(frame, text, (10, y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    return frame

def get_video_stream(model_path: str):
    """ビデオストリームを生成する"""
    session = axe.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    camera = cv2.VideoCapture(0)

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            # 推論実行
            input_tensor = process_frame(frame)
            output = session.run(None, {input_name: input_tensor})
            
            # 予測結果を取得して描画
            indices, scores = get_top_k_predictions(output[0])
            frame_with_pred = draw_predictions(frame, indices, scores)
            
            # JPEGエンコード
            _, buffer = cv2.imencode('.jpg', frame_with_pred)
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + 
                  buffer.tobytes() + b'\r\n')
            
            time.sleep(0.005)
    finally:
        camera.release()

@app.get("/video")
async def video_endpoint(
    model: str = '/opt/data/npu/models/mobilenetv2.axmodel'
):
    """ビデオストリーミングのエンドポイント"""
    return StreamingResponse(
        get_video_stream(model),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='リアルタイム分類推論')
    parser.add_argument(
        '--model',
        default='/opt/data/npu/models/mobilenetv2.axmodel',
        help='モデルファイルのパス'
    )
    
    args = parser.parse_args()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)