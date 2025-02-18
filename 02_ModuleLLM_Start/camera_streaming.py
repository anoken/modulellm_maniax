#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
from typing import Generator
import time

# FastAPIアプリケーションのインスタンスを作成
app = FastAPI()

def get_video_stream() -> Generator[bytes, None, None]:
    # カメラからビデオストリームを生成する関数
    # カメラデバイスを開く（0は通常、デフォルトのカメラ）
    camera = cv2.VideoCapture(0)
    try:
        while True:
            # カメラからフレームを読み取る
            success, frame = camera.read()
            if not success:
                break
            
            # フレームをリサイズ（320x240）
            frame = cv2.resize(frame, (320, 240))
            
            # フレームレートを制御（0.05秒の待機）
            time.sleep(0.05)
            
            # フレームをJPEG形式にエンコード
            _, buffer = cv2.imencode('.jpg', frame)
            
            # マルチパート形式でフレームを返す
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + 
                  buffer.tobytes() + b'\r\n')
    finally:
        # 終了時にカメラを解放
        camera.release()

@app.get("/video")
async def video_endpoint():
    # ビデオストリームを提供するエンドポイント
    return StreamingResponse(
        get_video_stream(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    import uvicorn
    # サーバーを起動（すべてのIPアドレスからアクセス可能）
    uvicorn.run(app, host="0.0.0.0", port=8888)
