## Copyright (c) 2025 aNoken

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
import numpy as np
import axengine as axe
import time
import argparse

app = FastAPI()

def process_frame(frame: np.ndarray, width: int, height: int) -> np.ndarray:
    """フレームの前処理を行う"""
    if frame is None:
        raise ValueError("フレームの読み込みに失敗しました")
    resized = cv2.resize(frame, (width, height))
    return np.expand_dims(resized[..., ::-1], axis=0)

def create_depth_map(depth_map: np.ndarray, frame: np.ndarray) -> np.ndarray:
    """深度マップの可視化を行う"""
    depth = depth_map.reshape(depth_map.shape[-2:])
    norm = (depth - depth.min()) / (depth.max() - depth.min())
    colored = cv2.applyColorMap(
        (norm * 255).astype(np.uint8),
        cv2.COLORMAP_INFERNO
    )
    resized = cv2.resize(colored, (frame.shape[1], frame.shape[0]))
    return np.concatenate([frame, resized], axis=1)

def get_video_stream(model_path: str, width: int, height: int):
    """ビデオストリームを生成する"""
    session = axe.InferenceSession(model_path)
    input_name = session.get_inputs()[0].name
    camera = cv2.VideoCapture(0)

    try:
        while True:
            success, frame = camera.read()
            if not success:
                break

            frame = cv2.resize(frame, (width, height))
            tensor = process_frame(frame, width, height)
            output = session.run(None, {input_name: tensor})
            viz = create_depth_map(output[0], frame)
            
            _, buffer = cv2.imencode('.jpg', viz)
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + 
                  buffer.tobytes() + b'\r\n')
            time.sleep(0.005)
    finally:
        camera.release()

@app.get("/video")
async def video_endpoint(
    model: str = '/opt/m5stack/data/depth-anything-ax630c/depth_anything.axmodel',
    width: int = 384,
    height: int = 256
):
    """ビデオストリーミングのエンドポイント"""
    return StreamingResponse(
        get_video_stream(model, width, height),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='深度マップを生成します')
    parser.add_argument(
        '--model',
        default='/opt/m5stack/data/depth-anything-ax630c/depth_anything.axmodel',
        help='モデルファイルのパス'
    )
    parser.add_argument(
        '--width',
        type=int,
        default=384,
        help='処理する画像の幅'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=256,
        help='処理する画像の高さ'
    )
    
    args = parser.parse_args()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)