from openai import OpenAI
import base64
import json
import os

client = OpenAI(
      api_key="xxxxx",
      base_url="xxxx"
  )

def get_open_qa_evaluation_prompt():
    """
    获取开放式问答评分的prompt模板
    
    Returns:
        str: 用于评分的system prompt模板
    """
    system_prompt = (
        "You are a helpful and precise assistant for checking the quality of the answer.\n"
        "[Detailed Audio Description]\nXAudioX\n"
        "[Question]\nXQuestionX\n"
        "[The Start of Assistant 1s Answer]\nXAssistant1X\n"
        "[The End of Assistant 1s Answer]\n"
        "[The Start of Assistant 2s Answer]\nXAssistant2X\n"
        "[The End of Assistant 2s Answer]\n"
        "[System]\n"
        "We would like to request your feedback on the performance of two AI assistants in response to the user question "
        "and audio description displayed above. AI assistants are provided with detailed audio descriptions and questions.\n"
        "Please rate the helpfulness, relevance, accuracy, and comprehensiveness of their responses. "
        "Each assistant receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance. "
        "Please output a single line containing only two values indicating the scores for Assistant 1 and 2, respectively. "
        "The two scores are separated by a space."
    )
    return system_prompt


def build_evaluation_content(audio_description, question, ground_truth_answer, model_response):
    """
    构建用于评分的完整内容
    
    Args:
        audio_description (str): 音频的详细描述信息
        question (str): 问题内容
        ground_truth_answer (str): 标准答案
        model_response (str): 模型回答
        
    Returns:
        str: 填充好的评分prompt
    """
    system_prompt = get_open_qa_evaluation_prompt()
    
    content = system_prompt.replace("XAudioX", audio_description)\
                          .replace("XQuestionX", question)\
                          .replace("XAssistant1X", ground_truth_answer)\
                          .replace("XAssistant2X", model_response)
    
    return content


def parse_evaluation_scores(response_text):
    """
    解析评分结果
    
    Args:
        response_text (str): GPT评分的原始回复
        
    Returns:
        tuple: (assistant1_score, assistant2_score) 或 None（如果解析失败）
    """
    try:
        scores_text = response_text.strip().replace('\n', '')
        scores = scores_text.split(' ')
        
        if len(scores) == 2:
            score1 = int(scores[0])
            score2 = int(scores[1])
            
            # 验证分数范围
            if 1 <= score1 <= 10 and 1 <= score2 <= 10:
                return (score1, score2)
        
        return None
    except (ValueError, IndexError):
        return None


def get_evaluation_criteria():
    """
    获取评分标准说明
    
    Returns:
        dict: 评分标准的详细说明
    """
    criteria = {
        "helpfulness": "回答是否对用户有帮助，能否解决用户的问题",
        "relevance": "回答是否与问题和音频内容相关",
        "accuracy": "回答的准确性，是否符合事实",
        "comprehensiveness": "回答的全面性，是否涵盖了问题的各个方面",
        "score_range": "1-10分，分数越高表示表现越好",
        "output_format": "输出一行包含两个分数，用空格分隔"
    }
    return criteria



new_answers = []
json_path="your_json_path"

cnt=0
with open(json_path, 'r') as file:
    data = json.load(file)
    for item in data:
        if cnt>-1:
            print("ID:", item["id"])
            audio_desc = item["caption"]
            question = item["question"]
            gt_answer = item["answer"]
            model_answer = item["model_output"]
            eval_content = build_evaluation_content(audio_desc, question, gt_answer, model_answer)
            text_prompt=eval_content
            criteria = get_evaluation_criteria()
            text_prompt=text_prompt+"评分标准:"
            for key, value in criteria.items():
                # print(f"- {key}: {value}")
                text_prompt=text_prompt+f"{key}: {value}"
            # response = client.chat.completions.create(
                # your api
            # )
            response_text=response.choices[0].message.content
            item["score"] = response_text
            with open('your_json_path', 'w', encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        cnt=cnt+1
