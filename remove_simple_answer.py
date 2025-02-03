#移除過於簡潔的回答
import json

def filter_conversations(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    filtered_data = []
    for item in data:
        conversations = item.get("conversations", [])
        if not conversations:
            continue
        
        gpt_responses = [conv["value"].strip() for conv in conversations if conv["from"] == "gpt"]
        
        # 移除回答為 "Yes", "No" 或空白的資料
        if not all(resp in {"Yes", "No", "", "yes", "no"} for resp in gpt_responses):
            filtered_data.append(item)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

input_file = "traffic_flow_train_data.json"
output_file = "filtered_traffic_flow_train_data.json"
filter_conversations(input_file, output_file)