#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import socket
import json
import argparse

# ソケットからレスポンスを受信して表示する関数
def receive_and_display_responses(sock):
    while True:
        try:
            print("\n=====:")

            # ソケットからデータを受信してデコード
            data = sock.recv(4096).decode()
            if not data:
                break
            response = json.loads(data)

            # エラーチェック: エラーコードが0以外の場合はエラーメッセージを表示
            if "error" in response and response["error"]["code"] != 0:
                print(f"Error {response['error']['code']}: {response['error']['message']}")
                continue
                
            # レスポンスデータが辞書型で、deltaキーが存在する場合はその値を表示
            if "data" in response and isinstance(response["data"], dict):
                if "delta" in response["data"]:
                    print(response["data"]["delta"], end="")
            
            # 処理完了フラグがtrueの場合はループを終了
            if data.find('"finish":true') != -1:
                break
        except Exception as e:
            print(f"Error: {e}")
            break

# メイン処理関数
def main(host, port):
    # ソケット接続の確立
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((host, port))
            print(f'Connected to {host}:{port}')
            
            # リクエストの構築
            # コマンド 'ls /opt' を実行するリクエストを作成
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
            
            # リクエストをJSON形式に変換して送信
            json_str = json.dumps(request)
            client.send(json_str.encode())
            print(f'\nSent request:\n{json.dumps(request, indent=2)}')
            
            # レスポンスの受信と表示
            print("\nResponse:")
            receive_and_display_responses(client)
            
        except ConnectionRefusedError:
            print(f"Connection refused to {host}:{port}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=10001)
    args = parser.parse_args()
    
    # メイン処理の実行
    main(args.host, args.port)