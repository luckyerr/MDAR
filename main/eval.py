import argparse
import json
import re
from tqdm import tqdm

def string_match(answer, prediction, choices):
    # Function to normalize and tokenize text
    def tokenize(text):
        # text = re.sub(r'[,.;!?，。；！？]+$', '', text.lower())
        return set(re.findall(r'\b\w+\b', text.lower()))
    
    # Tokenize prediction and answer
    prediction_tokens = tokenize(prediction)
    answer_tokens = tokenize(answer)
    
    if not prediction_tokens:
        return False
    
    # Tokenize incorrect choices and exclude tokens present in the answer
    incorrect_tokens = set()
    for choice in choices:
        choice_tokens = tokenize(choice)
        if choice_tokens != answer_tokens:
            incorrect_tokens.update(choice_tokens - answer_tokens)
    
    # Condition 1: All tokens of the answer are in the prediction
    cond1 = answer_tokens.issubset(prediction_tokens)
    
    # Condition 2: Prediction does not contain any tokens from incorrect choices (excluding shared words)
    cond2 = prediction_tokens.isdisjoint(incorrect_tokens)
    
    return cond1 and cond2

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

        _prediction = sample[output_key]
        _answer = sample['answer']
        choices = sample['chosens']
        task = sample['category']

        # Initialize task metrics if not already present
        if task not in task_metrics:
            task_metrics[task] = {'correct': 0, 'total': 0}

        if string_match(_answer, _prediction, choices):
            corr += 1
            task_metrics[task]['correct'] += 1

        total += 1
        task_metrics[task]['total'] += 1

    # Print overall results:
    print("*" * 30)
    print(f"Total Accuracy: {(corr / total) * 100:.2f}% over {total} samples")
    print("*" * 30)
    print(f"No prediction count: {no_pred_count}")

    # # Print task-wise results:
    # print("*" * 30)
    # print("Task-wise Accuracy:")
    # for task, metrics in task_metrics.items():
    #     task_corr = metrics['correct']
    #     task_total = metrics['total']
    #     task_acc = (task_corr / task_total) * 100 if task_total > 0 else 0
    #     print(f"{task} : {task_acc:.2f}% over {task_total} samples")
    # print("*" * 30)

    combined_task_name = "人物关系与社交推理类"
    combined_corr = (task_metrics.get("人物身份关联任务", {'correct': 0})['correct'] +
                     task_metrics.get("社交意图推理任务", {'correct': 0})['correct'])
    combined_total = (task_metrics.get("人物身份关联任务", {'total': 0})['total'] +
                      task_metrics.get("社交意图推理任务", {'total': 0})['total'])

    combined_acc = (combined_corr / combined_total) * 100 if combined_total > 0 else 0

    # Print combined results
    print("*" * 30)
    print("Combined Task Accuracy:")
    print(f"{combined_task_name} : {combined_acc:.2f}% over {combined_total} samples")
    # print("*" * 30)

    combined_task_name = "场景理解类"
    combined_corr = (task_metrics.get("场景定位任务", {'correct': 0})['correct'] +
                     task_metrics.get("场景变化（切换）推理任务", {'correct': 0})['correct'] +
                     task_metrics.get("场景要素识别", {'correct': 0})['correct'])
    combined_total = (task_metrics.get("场景定位任务", {'total': 0})['total'] +
                      task_metrics.get("场景变化（切换）推理任务", {'total': 0})['total'] +
                      task_metrics.get("场景要素识别", {'total': 0})['total'])

    combined_acc = (combined_corr / combined_total) * 100 if combined_total > 0 else 0

    # Print combined results
    print("*" * 30)
    print("Combined Task Accuracy:")
    print(f"{combined_task_name} : {combined_acc:.2f}% over {combined_total} samples")
    # print("*" * 30)

    combined_task_name = "时间推理任务"
    combined_corr = (task_metrics.get("时间推理任务", {'correct': 0})['correct'])
    combined_total = (task_metrics.get("时间推理任务", {'total': 0})['total'])

    combined_acc = (combined_corr / combined_total) * 100 if combined_total > 0 else 0

    # Print combined results
    print("*" * 30)
    print("Combined Task Accuracy:")
    print(f"{combined_task_name} : {combined_acc:.2f}% over {combined_total} samples")
    # print("*" * 30)

    combined_task_name = "事件推理类"
    combined_corr = (task_metrics.get("事件因果推理任务", {'correct': 0})['correct'] +
                     task_metrics.get("事件顺序推理任务", {'correct': 0})['correct'])
    combined_total = (task_metrics.get("事件因果推理任务", {'total': 0})['total'] +
                      task_metrics.get("事件顺序推理任务", {'total': 0})['total'])

    combined_acc = (combined_corr / combined_total) * 100 if combined_total > 0 else 0

    # Print combined results
    print("*" * 30)
    print("Combined Task Accuracy:")
    print(f"{combined_task_name} : {combined_acc:.2f}% over {combined_total} samples")
    # print("*" * 30)

    combined_task_name = "异常检测与安全"
    combined_corr = (task_metrics.get("异常检测与安全任务", {'correct': 0})['correct'])
    combined_total = (task_metrics.get("异常检测与安全任务", {'total': 0})['total'])

    combined_acc = (combined_corr / combined_total) * 100 if combined_total > 0 else 0

    # Print combined results
    print("*" * 30)
    print("Combined Task Accuracy:")
    print(f"{combined_task_name} : {combined_acc:.2f}% over {combined_total} samples")
    print("*" * 30)