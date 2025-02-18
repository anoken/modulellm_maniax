#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import socket
import json
import argparse
import time

def send_json_request(sock, request_data):
    """JSONリクエストをサーバーに送信"""
    try:
        json_string = json.dumps(request_data)
        sock.sendall(json_string.encode('utf-8'))
        print(f'Sent request: {json_string}')
        time.sleep(1)
    except Exception as e:
        print(f'Request send error: {e}')

def receive_response(sock):
    """サーバーからのレスポンスを受信して処理"""
    try:
        data = sock.recv(4096)
        if data:
            response = data.decode('utf-8')
            print(f'Received response: {response}')
            return json.loads(response)
    except Exception as e:
        print(f'Response receive error: {e}')
    return None

def receive_full_data(sock):
    data = b''
    while True:
        packet = sock.recv(4096)
        if not packet:
            break
        data += packet
        if b'\n' in data:
            break
    return data.split(b'\n')

def main(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f'Connected to server at {host}:{port}')
        print(f'Setup sequence starting:')

        # Audio setup
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

        # VAD setup
        vad_setup = {
            "request_id": "vad_setup",
            "work_id": "vad",
            "action": "setup",
            "object": "vad.setup",
            "data": {
                "input": ["sys.pcm"]
            }
        }
        send_json_request(client_socket, vad_setup)
        vad_response = receive_response(client_socket)
        vad_work_id = vad_response.get('work_id') if vad_response else None

        # Whisper setup
        whisper_setup = {
            "request_id": "whisper_setup",
            "work_id": "whisper",
            "action": "setup",
            "object": "whisper.setup",
            "data": {
                "model": "whisper-tiny",
                "response_format": "asr.utf-8",
#                "language": "ja",
                "language": "en",
                "enoutput": True,
                "input": ["sys.pcm", vad_work_id] if vad_work_id else ["sys.pcm"]
            }
        }
        send_json_request(client_socket, whisper_setup)
        receive_response(client_socket)

        print('Setup complete, listening for messages...')

        while True:
            data_packets = receive_full_data(client_socket)
            if not data_packets:
                print("Connection closed by server")
                break

            for packet in data_packets:
                if not packet:
                    continue
                try:
                    response = packet.decode("utf-8")
                    json_data = json.loads(response)
                    if "data" in json_data:
                        print(f"Transcription: {json_data['data']}")
                except json.JSONDecodeError as e:
                    print(f'JSON parse error: {e}')
                except Exception as e:
                    print(f'Error: {e}')

    finally:
        print("Closing connection")
        client_socket.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='M5Stack LLM Client')
    parser.add_argument('--host', type=str, default='m5stack-LLM.local',
                      help='Server hostname (default: m5stack-LLM.local)')
    parser.add_argument('--port', type=int, default=10001,
                      help='Server port (default: 10001)')

    args = parser.parse_args()
    main(args.host, args.port)
