#!/usr/bin/env python3
# Copyright (c) 2025 aNoken


import socket
import json
import time
import os
from pathlib import Path
import argparse

def send_json_request(sock, request_data):
    """JSONリクエストをサーバーに送信"""
    try:
        json_string = json.dumps(request_data)
        sock.sendall(json_string.encode('utf-8'))
        print(f'送信したリクエスト: {json_string}')
        time.sleep(1)
    except Exception as e:
        print(f'リクエスト送信エラー: {e}')

def receive_response(sock):
    """サーバーからのレスポンスを受信して処理"""
    try:
        data = sock.recv(4096)
        if data:
            response = data.decode('utf-8')
            print(f'受信したレスポンス: {response}')
            return json.loads(response)
    except Exception as e:
        print(f'レスポンス受信エラー: {e}')
    return None

def main(host, port):
    os.chdir(Path(__file__).parent)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((host, port))
        print(f'サーバー {host}:{port} に接続しました')

        # オーディオセットアップ
        audio_setup = {
            "request_id": "audio_setup",
            "work_id": "audio",
            "action": "setup",
            "object": "audio.setup",
            "data": {
                "capcard": 0,
                "capdevice": 0,
                "capVolume": 0.5,
                "playcard": 0,
                "playdevice": 1,
                "playVolume": 0.15
            }
        }
        send_json_request(client_socket, audio_setup)
        receive_response(client_socket)

        # TTSセットアップ
        tts_setup = {
            "request_id": "melotts_setup",
            "work_id": "melotts",
            "action": "setup",
            "object": "melotts.setup",
            "data": {
                "model": "melotts-zh-cn",
                "response_format": "sys.pcm",
                "input": ["tts.utf-8.stream"],
                "enoutput": False,
                "enaudio": True
            }
        }
        send_json_request(client_socket, tts_setup)
        receive_response(client_socket)

        # TTS推論
        inference_request = {
            "request_id": "tts_inference",
            "work_id": "melotts.1001",
            "action": "inference",
            "object": "tts.utf-8.stream",
            "data": {
                "delta": "Hello, I am Stack chan. Nice to meet you.",
                "index": 0,
                "finish": True
            }
        }
        send_json_request(client_socket, inference_request)
        receive_response(client_socket)
        
        time.sleep(5)
        
        # リセット
        reset_request = {
            "request_id": "4",
            "work_id": "sys",
            "action": "reset"
        }
        send_json_request(client_socket, reset_request)
        receive_response(client_socket)

    except Exception as e:
        print(f'エラー: {e}')
    finally:
        client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Client to send JSON data.')
    parser.add_argument('--host', type=str, default='m5stack-LLM.local',
                       help='Server hostname (default: m5stack-LLM.local)')
    parser.add_argument('--port', type=int, default=10001,
                       help='Server port (default: 10001)')
    args = parser.parse_args()
    main(args.host, args.port)