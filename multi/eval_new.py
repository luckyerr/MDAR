import argparse
import json
import re
from tqdm import tqdm
from collections import defaultdict
from tqdm import tqdm

# 存放各类累加值
correct_by_task1 = defaultdict(float)   
count_by_task1  = defaultdict(int)   
correct_by_task2 = defaultdict(float)   
count_by_task2  = defaultdict(int)      
correct_by_task3 = defaultdict(float)   
count_by_task3  = defaultdict(int)      
correct_by_task4 = defaultdict(float)   
count_by_task4  = defaultdict(int)      
total_correct1 = 0.0
total_count1   = 0
no_pred_count1 = 0
total_correct2 = 0.0
total_count2   = 0
no_pred_count2 = 0
total_correct3 = 0.0
total_count3   = 0
no_pred_count3 = 0
total_correct4 = 0.0
total_count4  = 0
no_pred_count4 = 0

def EM(pred_set: set, gold_set: set) -> float:
    return float(pred_set == gold_set)

def JI(pred_set: set, gold_set: set) -> float:
    inter = pred_set & gold_set
    union = pred_set | gold_set
    return len(inter) / len(union) if union else 0.0

def Precision(pred_set: set, gold_set: set) -> float:
    if not pred_set:
        return 0.0
    return len(pred_set & gold_set) / len(pred_set)

def Recall(pred_set: set, gold_set: set) -> float:
    if not gold_set:
        return 0.0
    return len(pred_set & gold_set) / len(gold_set)

def clean(txt: str) -> str:
    return re.sub(r'[,.;!?，。；！？]+$', '', txt.strip())

def exact_acc(model_output: str, choices_list: list[str], answer_list: list[str]) -> float:
    # print(model_output)
    sep_pattern = re.compile(r'[；;\n]+')
    parts = sep_pattern.split(model_output)

    out_answer = []
    for seg in parts:
        if clean(seg) in choices_list:
            out_answer.append(clean(seg))

    answer_list = set(answer_list)
    out_answer = set(out_answer)

    acc1=EM(out_answer,answer_list)
    acc2=JI(out_answer,answer_list)
    acc3=Precision(out_answer,answer_list)
    acc4=Recall(out_answer,answer_list)
    return acc1,acc2,acc3,acc4


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process benchmark JSON and calculate accuracy.")
    parser.add_argument('--input', type=str, required=True, help='Path to input JSON file to be evaluated')
    args = parser.parse_args()  

    with open(args.input, 'r') as f:
        input_data = json.load(f)
        
    corr, total = 0, 0
    no_pred_count = 0
    output_key = 'model_output'  # The key that contains model output

    # Dictionary to track metrics for different tasks
    task_metrics = {}

    for idx, sample in enumerate(tqdm(input_data)):
        if output_key not in sample:
            no_pred_count += 1
            continue

        _prediction = sample[output_key][0]
        _answer = sample['answer']
        choices = sample['chosens']
        task = sample['category']

        acc1,acc2,acc3,acc4 = exact_acc(_prediction, choices, _answer)

        total_correct1 += acc1
        total_count1   += 1

        correct_by_task1[task] += acc1
        count_by_task1[task]   += 1

        total_correct2 += acc2
        total_count2   += 1

        correct_by_task2[task] += acc2
        count_by_task2[task]   += 1

        total_correct3 += acc3
        total_count3   += 1

        correct_by_task3[task] += acc3
        count_by_task3[task]   += 1

        total_correct4 += acc4
        total_count4   += 1

        correct_by_task4[task] += acc4
        count_by_task4[task]   += 1

    # ---------------- 打印结果 ----------------
    print("--------------EM---------------")
    for t in count_by_task1:
        print(f"{t:<20}  {correct_by_task1[t]/count_by_task1[t]:>6.2%}  ({count_by_task1[t]} 条)")
    print("-----------------------------")
    print(f"总正确率              {total_correct1/total_count1:>6.2%}  ({total_count1} 条)")
    if no_pred_count1:
        print(f"无预测条目            {no_pred_count1:>6} 条")

    print("--------------JI---------------")
    for t in count_by_task2:
        print(f"{t:<20}  {correct_by_task2[t]/count_by_task2[t]:>6.2%}  ({count_by_task2[t]} 条)")
    print("-----------------------------")
    print(f"总正确率              {total_correct2/total_count2:>6.2%}  ({total_count2} 条)")
    if no_pred_count2:
        print(f"无预测条目            {no_pred_count2:>6} 条")

    print("--------------Precision---------------")
    for t in count_by_task3:
        print(f"{t:<20}  {correct_by_task3[t]/count_by_task3[t]:>6.2%}  ({count_by_task3[t]} 条)")
    print("-----------------------------")
    print(f"总正确率              {total_correct3/total_count3:>6.2%}  ({total_count3} 条)")
    if no_pred_count3:
        print(f"无预测条目            {no_pred_count3:>6} 条")

    print("--------------Recall---------------")
    for t in count_by_task4:
        print(f"{t:<20}  {correct_by_task4[t]/count_by_task4[t]:>6.2%}  ({count_by_task4[t]} 条)")
    print("-----------------------------")
    print(f"总正确率              {total_correct4/total_count4:>6.2%}  ({total_count4} 条)")
    if no_pred_count4:
        print(f"无预测条目            {no_pred_count4:>6} 条")