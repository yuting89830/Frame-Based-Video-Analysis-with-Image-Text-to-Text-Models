import os
import json
import torch
import cv2
from PIL import Image
from transformers import LlavaProcessor, LlavaForConditionalGeneration
import logging

logging.getLogger("transformers").setLevel(logging.ERROR)

model_id = "llava-hf/llava-interleave-qwen-0.5b-hf"
processor = LlavaProcessor.from_pretrained(model_id)
model = LlavaForConditionalGeneration.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")

def load_local_video(video_path, num_frames=6):
    """讀取並抽樣影片幀"""
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    interval = max(total_frames // num_frames, 1)
    
    for i in range(num_frames):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * interval)
        ret, frame = cap.read()
        if ret:
            frames.append(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
    
    cap.release()
    return frames

def process_video(video_path, video_id, user_query):
    """對單個影片進行inference"""
    video_frames = load_local_video(video_path)
    image_tokens = "<image>" * len(video_frames)
    prompt = f"<|im_start|>user{image_tokens}\n{user_query}<|im_end|><|im_start|>assistant"
    
    inputs = processor(text=prompt, images=video_frames, return_tensors="pt").to("cuda", torch.float16)
    outputs = model.generate(**inputs, max_new_tokens=200)
    
    full_response = processor.decode(outputs[0], skip_special_tokens=True)
    answer = full_response.split("assistant")[-1].strip()
    
    return {
        "id": video_id,
        "video": os.path.basename(video_path),
        "conversations": [
            {"from": "human", "value": user_query},
            {"from": "gpt", "value": answer}
        ]
    }

def process_video_folder(video_folder, output_file, user_queries):
    """遍歷資料夾內所有影片"""
    results = []
    video_files = sorted([f for f in os.listdir(video_folder) if f.endswith(".mp4")])
    
    for idx, video_file in enumerate(video_files):
        video_path = os.path.join(video_folder, video_file)
        user_query = user_queries[idx % len(user_queries)]  # 輪流選擇問題
        print(f"Processing {video_file} ({idx + 1}/{len(video_files)}) with query: {user_query}")
        result = process_video(video_path, idx, user_query)
        results.append(result)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"Results saved to {output_file}")

# 設定影片資料夾與輸出檔案
video_folder = "./test_videos"  
output_file = "traffic_flow_test_data.json"
user_queries = [
    "Is there a traffic jam right now?",
    "Is the road currently congested?",
    "Is the traffic heavy on the road right now?",
    "Is the traffic currently congested?",
    "Is the traffic currently smooth?"
]

# 執行處理
process_video_folder(video_folder, output_file, user_queries)
