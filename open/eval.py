from collections import defaultdict
import json

# 存放累加
score_sum_by_task = defaultdict(float)  
count_by_task     = defaultdict(int)    
total_score       = 0.0
total_count       = 0


json_path="your_json_path"


with open(json_path, 'r') as file:
    data = json.load(file)
    for item in data:
        score_str=item["score"]
        s1=int(score_str[:2])
        s2=int(score_str[-2:])
        score=(s2/s1)*10


        task = item["category"]
        score_sum_by_task[task] += score
        count_by_task[task]     += 1
        total_score += score
        total_count += 1


print("-----------------------------")
for t in count_by_task:
    print(f"{t:<30}  {score_sum_by_task[t]/count_by_task[t]:>6.2f}  ({count_by_task[t]} 条)")
print("-----------------------------")
print(f"总平均得分                    {total_score/total_count:>6.2f}  ({total_count} 条)")