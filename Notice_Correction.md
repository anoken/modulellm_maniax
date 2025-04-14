# 訂正とお詫びのお知らせ

ModuleLLM_MAniaX に下記のように誤りがありました。<br>
ご購入頂いた読者の皆様には、大変ご迷惑をおかけ致しました。<br>
ここに深くお詫びし、訂正させていただきます。<br>

## ver 1.0.0(2025 年2 月27 日印刷版)

#### P.103<br>

誤：
Ubuntu 24.04.1にて、cmakeのプロジェクト設定が、クロスコンパイル設定の前にあると,
"No CMAKE_CXX_COMPILER could be found."が発生する不具合出るため、修正。

```
リスト5.2: CMakeLists.txt
------
# プロジェクト名の設定
project(ax_depth_anything_image)
# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
```
→
正：
```
リスト5.2: CMakeLists.txt
------
# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
# プロジェクト名の設定
project(ax_depth_anything_image)
```
#### P.106<br>

誤：
Ubuntu 24.04.1にて、cmakeのプロジェクト設定が、クロスコンパイル設定の前にあると,
"No CMAKE_CXX_COMPILER could be found."が発生する不具合出るため、修正。

```
リスト5.4: CMakeLists.txt
------
# プロジェクト名の設定
project(camera_streaming)
# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
```
→
正：
```
リスト5.2: CMakeLists.txt
------
# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
# プロジェクト名の設定
project(camera_streaming)
```
#### P.111<br>

誤：
Ubuntu 24.04.1にて、cmakeのプロジェクト設定が、クロスコンパイル設定の前にあると,
"No CMAKE_CXX_COMPILER could be found."が発生する不具合あるため、修正。

```
リスト5.6: CMakeLists.txt
------
# プロジェクト名の設定
project(ax_depth_anything_camera_stream)
# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
```
→
正：
```
リスト5.6: CMakeLists.txt
------
# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)
# プロジェクト名の設定
project(ax_depth_anything_camera_stream)
```

#### P.96<br>
誤：5.2.2 AX620Q BSP SDK のダウンロード<br>
→正：5.2.2 AX620E BSP SDK のダウンロード<br>

- P.112<br>
誤：set(BSP_MSP_DIR /opt/ax620q_bsp_sdk/msp/out)<br>
→正：set(BSP_MSP_DIR /opt/ax620e_bsp_sdk/msp/out)<br>

#### P.113<br>
誤：<br>
```
 UbuntuPC$ git clone https://github.com/AXERA-TECH/ax620q_bsp_sdk.git<br>
 UbuntuPC$ export ax_bsp=$PWD/ax620e_bsp_sdk/msp/out/arm64_glibc/<br>
 UbuntuPC$ echo $ax_bsp /opt/ax620e_bsp_sdk/msp/out/arm64_glibc/<br>
```
→正：<br>
```
 UbuntuPC$ git clone https://github.com/AXERA-TECH/ax620e_bsp_sdk.git<br>
 UbuntuPC$ export ax_bsp=$PWD/ax620e_bsp_sdk/msp/out/arm64_glibc/<br>
 UbuntuPC$ echo $ax_bsp /opt/ax620e_bsp_sdk/msp/out/arm64_glibc/<br>
```









