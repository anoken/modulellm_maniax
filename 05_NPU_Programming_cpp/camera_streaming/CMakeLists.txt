# 最小CMakeバージョンの指定
cmake_minimum_required(VERSION 3.5)

# プロジェクト名の設定
project(camera_streaming)

# クロスコンパイル設定
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)
set(CMAKE_C_COMPILER aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER aarch64-linux-gnu-g++)

# ビルド設定
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -Wall")

# OpenCVのパス設定
set(OpenCV_DIR 
        /opt/ax-samples/3rdparty/opencv-aarch64-linux/lib/cmake/opencv4/)


# OpenCVの検索
find_package(OpenCV REQUIRED)

# インクルードディレクトリの設定
include_directories(${OpenCV_INCLUDE_DIRS})

# 実行ファイルの追加
add_executable(camera_streaming camera_streaming.cpp)

# OpenCVライブラリのリンク
target_link_libraries(camera_streaming PRIVATE ${OpenCV_LIBS})