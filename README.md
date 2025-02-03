# Video Traffic Analysis with Image-to-Text Models

## Introduction

This project processes videos by converting them into frames and using an image-text-to-text model to analyze traffic conditions. The model provides answers to traffic-related questions, which are then saved in a JSON file. Additionally, simple responses such as "Yes," "No," or blank answers are filtered out for better data quality.

## 使用說明

本專案透過將影片轉換為影像幀，並使用圖像-文本轉文本模型來分析車流狀況。模型提供的回答會儲存為 JSON 檔案，並進一步過濾掉簡單回答（例如 "Yes"、"No" 或空白答案），以提高資料品質。

## Model

We use the following model from Hugging Face: [llava-hf/llava-interleave-qwen-0.5b-hf](https://huggingface.co/llava-hf/llava-interleave-qwen-0.5b-hf)

## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Step 1: Process Video with traffic_understanding.py

Run the script to process a video and generate a JSON file with traffic-related answers.

```bash
python traffic_understanding.py
```

### Step 2: Remove Simple Answers with remove_simple_answer.py

This step filters out responses that are only "Yes," "No," or empty.

```bash
python remove_simple_answer.py
```
## Note

You are welcome to modify the prompts and video files to suit your specific needs. Adjusting the prompts or using different video files will allow you to tailor the analysis for various traffic scenarios or other use cases.
