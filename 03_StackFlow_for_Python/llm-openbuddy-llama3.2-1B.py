#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import socket
import json
import argparse


# TCPソケット接続を確立する関数
def create_tcp_connection(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    return sock


# JSONデータをソケットに送信する関数
def send_json(sock, data):
    json_data = json.dumps(data, ensure_ascii=False) + '\n'
    sock.sendall(json_data.encode('utf-8'))


# ソケットからレスポンスを受信する関数
def receive_response(sock):
    response = ''
    while True:
        part = sock.recv(4096).decode('utf-8')
        response += part
        if '\n' in response:
            break
    return response.strip()


# ソケット接続を閉じる関数
def close_connection(sock):
    if sock:
        sock.close()


# LLMの初期設定データを作成する関数
def create_init_data():
    return {
        "request_id": "llm_001",
        "work_id": "llm",
        "action": "setup",
        "object": "llm.setup",
        "data": {
            "model": "openbuddy-llama3.2-1B-ax630c",  # 使用するモデル
            "response_format": "llm.utf-8.stream",   # レスポンスのフォーマット
            "input": "llm.utf-8.stream",            # 入力フォーマット
            "enoutput": True,                        # 出力を有効化
            "max_token_len": 1023,                   # 最大トークン長
            "prompt": "あなたは、スタックチャン という名前の、親切で礼儀正しく正直なAI アシスタントです。。"  # システムプロンプト
        }
    }


# セットアップレスポンスを解析する関数
def parse_setup_response(response_data, sent_request_id):
    error = response_data.get('error')
    request_id = response_data.get('request_id')

    # リクエストIDの一致確認
    if request_id != sent_request_id:
        print(f"Request ID mismatch: sent {sent_request_id}, received {request_id}")
        return None

    # エラーチェック
    if error and error.get('code') != 0:
        print(f"Error Code: {error['code']}, Message: {error['message']}")
        return None

    return response_data.get('work_id')


# LLMのセットアップを実行する関数
def setup(sock, init_data):
    sent_request_id = init_data['request_id']
    send_json(sock, init_data)
    response = receive_response(sock)
    response_data = json.loads(response)
    return parse_setup_response(response_data, sent_request_id)


# セッションを終了する関数
def exit_session(sock, deinit_data):
    send_json(sock, deinit_data)
    response = receive_response(sock)
    response_data = json.loads(response)
    print("Exit Response:", response_data)


# 推論レスポンスを解析する関数
def parse_inference_response(response_data):
    error = response_data.get('error')
    if error and error.get('code') != 0:
        print(f"Error Code: {error['code']}, Message: {error['message']}")
        return None

    return response_data.get('data')


# メイン処理関数
def main(host, port):
    # TCPソケット接続の確立
    sock = create_tcp_connection(host, port)

    try:
        print("Setup LLM...")
        # LLMの初期設定
        init_data = create_init_data()
        llm_work_id = setup(sock, init_data)
        print("Setup LLM finished.")

        # 対話ループ
        while True:
            user_input = input("Enter your message (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            # 推論リクエストの送信
            send_json(sock, {
                "request_id": "llm_001",
                "work_id": llm_work_id,
                "action": "inference",
                "object": "llm.utf-8.stream",
                "data": {
                    "delta": user_input,
                    "index": 0,
                    "finish": True
                }
            })

            # ストリーミングレスポンスの受信と表示
            while True:
                response = receive_response(sock)
                response_data = json.loads(response)

                data = parse_inference_response(response_data)
                if data is None:
                    break

                delta = data.get('delta')
                finish = data.get('finish')
                print(delta, end='', flush=True)

                if finish:
                    print()
                    break

        # セッションの終了処理
        exit_session(sock, {
            "request_id": "llm_exit",
            "work_id": llm_work_id,
            "action": "exit"
        })
    finally:
        close_connection(sock)


# スクリプトのエントリーポイント
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='TCP Client to send JSON data.')
    parser.add_argument('--host', type=str, default='localhost', help='Server hostname (default: localhost)')
    parser.add_argument('--port', type=int, default=10001, help='Server port (default: 10001)')

    args = parser.parse_args()
    main(args.host, args.port)