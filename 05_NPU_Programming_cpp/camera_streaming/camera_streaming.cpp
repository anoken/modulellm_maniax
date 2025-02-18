// Copyright (c) 2025 aNoken

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <unistd.h>

int main()
{
    // カメラキャプチャーオブジェクトの作成
    cv::VideoCapture cap;
    // デフォルトカメラ（通常はID:0）をオープン
    cap.open(0);

    // HTTPストリーミング用のビデオライターオブジェクトの作成
    cv::VideoWriter http;
    // ポート8888でHTTPストリーミングを開始
    http.open("httpjpg", 8888);
    // ブラウザでアクセスする際のURL: http://<サーバーのIP>:8888

    // カメラからの画像を格納するためのMatオブジェクト
    cv::Mat bgr;

    // 無限ループでストリーミングを継続
    while (1)
    {
        // カメラから1フレームを取得
        cap >> bgr;
        // 取得したフレームをHTTPストリームに送信
        http << bgr;
        // フレームレート調整のため25ミリ秒待機
        usleep(25000);
    }

    return 0;
}
