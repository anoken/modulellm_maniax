#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import socket
import json
import argparse

# �\�P�b�g���烌�X�|���X����M���ĕ\������֐�
def receive_and_display_responses(sock):
    while True:
        try:
            print("\n=====:")

            # �\�P�b�g����f�[�^����M���ăf�R�[�h
            data = sock.recv(4096).decode()
            if not data:
                break
            response = json.loads(data)

            # �G���[�`�F�b�N: �G���[�R�[�h��0�ȊO�̏ꍇ�̓G���[���b�Z�[�W��\��
            if "error" in response and response["error"]["code"] != 0:
                print(f"Error {response['error']['code']}: {response['error']['message']}")
                continue
                
            # ���X�|���X�f�[�^�������^�ŁAdelta�L�[�����݂���ꍇ�͂��̒l��\��
            if "data" in response and isinstance(response["data"], dict):
                if "delta" in response["data"]:
                    print(response["data"]["delta"], end="")
            
            # ���������t���O��true�̏ꍇ�̓��[�v���I��
            if data.find('"finish":true') != -1:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# ���C�������֐�
def main(host, port):
    # �\�P�b�g�ڑ��̊m��
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((host, port))
            print(f'Connected to {host}:{port}')
            
            # ���N�G�X�g�̍\�z
            # �R�}���h 'ls /opt' �����s���郊�N�G�X�g���쐬
            request = {
                "request_id": "1",
                "work_id": "sys",
                "action": "bashexec",
                "object": "sys.stream",
                "data": {
                    "index": 0,
                    "delta": "ls /opt\n",
                    "finish": True
                }
            }
            
            # ���N�G�X�g��JSON�`���ɕϊ����đ��M
            json_str = json.dumps(request)
            client.send(json_str.encode())
            print(f'\nSent request:\n{json.dumps(request, indent=2)}')
            
            # ���X�|���X�̎�M�ƕ\��
            print("\nResponse:")
            receive_and_display_responses(client)
            
        except ConnectionRefusedError:
            print(f"Connection refused to {host}:{port}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # �R�}���h���C�������̉��
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=10001)
    args = parser.parse_args()
    
    # ���C�������̎��s
    main(args.host, args.port)