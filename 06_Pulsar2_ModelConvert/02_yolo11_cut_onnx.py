#!/usr/bin/env python3
# Copyright (c) 2025 aNoken

import onnx
import os
def extract_onnx_model(input_path, output_path):
   input_names = ["images"]
   output_names = [
       "/model.23/Concat_output_0",
       "/model.23/Concat_1_output_0", 
       "/model.23/Concat_2_output_0"
   ]
   onnx.utils.extract_model(input_path, output_path, input_names, output_names)

extract_onnx_model("yolo11n.onnx", "yolo11n-cut.onnx")
