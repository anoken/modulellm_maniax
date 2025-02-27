// Copyright (c) 2025 aNoken

#include <Arduino.h>
#include <M5Unified.h>
#include <M5ModuleLLM.h>

// M5ModuleLLMクラスのインスタンスを作成
M5ModuleLLM module_llm;
// LLMの作業IDを保存する変数
String llm_work_id;

void setup() {
 // M5Stackの初期化
 M5.begin();
 // テキストサイズを2に設定
 M5.Display.setTextSize(2);
 // テキストスクロールを有効化
 M5.Display.setTextScroll(true);
 // 日本語フォントを設定
 M5.Lcd.setTextFont(&fonts::efontJA_12);
 // シリアル通信の開始（PCとの通信用）
 Serial.begin(115200);

 /* モジュールのシリアルポートを初期化 */
 // 現在のM5Stackモデルに適したピン設定を自動的に取得
 int rxd = M5.getPin(m5::pin_name_t::port_c_rxd);
 int txd = M5.getPin(m5::pin_name_t::port_c_txd);
 // シリアル2通信の開始（ModuleLLMとの通信用）
 Serial2.begin(115200, SERIAL_8N1, rxd, txd);

 /* ModuleLLMの初期化 */
 module_llm.begin(&Serial2);

 /* ModuleLLMとの接続確認 */
 M5.Display.printf(">> Check ModuleLLM connection..\n");
 // 接続が確立されるまで待機
 while (1) {
   if (module_llm.checkConnection()) {
     break;
   }
 }

 /* ModuleLLMのリセット */
 M5.Display.printf(">> Reset ModuleLLM..\n");
 module_llm.sys.reset();

 /* LLMモジュールの設定と作業IDの保存 */
 M5.Display.printf(">> Setup llm..\n");
 // LLM設定用の構造体を初期化
 m5_module_llm::ApiLlmSetupConfig_t llm_config;
 // 最大トークン長を設定（入出力の制限）
 llm_config.max_token_len = 1023;
 // 使用するモデルを「TinySwallow-1.5B」に設定
 llm_config.model = "TinySwallow-1.5B";
 // モジュールのセットアップを実行し、作業IDを取得
 llm_work_id = module_llm.llm.setup();
 // セットアップ完了メッセージを表示
 M5.Display.printf(">> Start.\n");
}

void loop() {
 // PCからのシリアル入力があるかチェック
 if (Serial.available() > 0) {
   // シリアルから文字列を読み込む
   String input = Serial.readString();
   std::string question = input.c_str();
   
   // 入力された質問を緑色で表示
   M5.Display.setTextColor(TFT_GREEN);
   M5.Display.printf("<< %s\n", question.c_str());
   Serial.printf("<< %s\n", question.c_str());
   
   // 回答の前に「>>」を黄色で表示
   M5.Display.setTextColor(TFT_YELLOW);
   M5.Display.printf(">> ");
   Serial.printf(">> ");
   
   /* 質問をLLMモジュールに送信し、推論結果を待機 */
   // 推論結果はラムダ関数でリアルタイムに処理
   module_llm.llm.inferenceAndWaitResult(llm_work_id, question.c_str(), [](String& result) {
     /* 結果を画面とシリアルに表示 */
     M5.Display.printf("%s", result.c_str());
     Serial.printf("%s", result.c_str());
   });
   
   // 回答後に改行を入れる
   M5.Display.println();
 }
 
 // 0.5秒待機してCPU負荷を軽減
 delay(500);
}
