#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2
from typing import Generator
import time

# FastAPI�A�v���P�[�V�����̃C���X�^���X���쐬
app = FastAPI()

def get_video_stream() -> Generator[bytes, None, None]:
    # �J��������r�f�I�X�g���[���𐶐�����֐�
    # �J�����f�o�C�X���J���i0�͒ʏ�A�f�t�H���g�̃J�����j
    camera = cv2.VideoCapture(0)
    try:
        while True:
            # �J��������t���[����ǂݎ��
            success, frame = camera.read()
            if not success:
                break
            
            # �t���[�������T�C�Y�i320x240�j
            frame = cv2.resize(frame, (320, 240))
            
            # �t���[�����[�g�𐧌�i0.05�b�̑ҋ@�j
            time.sleep(0.05)
            
            # �t���[����JPEG�`���ɃG���R�[�h
            _, buffer = cv2.imencode('.jpg', frame)
            
            # �}���`�p�[�g�`���Ńt���[����Ԃ�
            yield (b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + 
                  buffer.tobytes() + b'\r\n')
    finally:
        # �I�����ɃJ���������
        camera.release()

@app.get("/video")
async def video_endpoint():
    # �r�f�I�X�g���[����񋟂���G���h�|�C���g
    return StreamingResponse(
        get_video_stream(),
        media_type='multipart/x-mixed-replace; boundary=frame'
    )

if __name__ == "__main__":
    import uvicorn
    # �T�[�o�[���N���i���ׂĂ�IP�A�h���X����A�N�Z�X�\�j
    uvicorn.run(app, host="0.0.0.0", port=8888)
