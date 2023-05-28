import numpy as np
import pandas as pd
import torch

from transformers import AutoModel, AutoTokenizer
from fastapi import FastAPI, UploadFile, File, Form
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = 'bert-base-multilingual-cased'
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

# cls token을 얻기 위한 함수
def get_cls_token(sent_A): # 문장이 입력
    model.eval()
    tokenized_sent = tokenizer(
        sent_A,
        return_tensors="pt",
        truncation=True,
        add_special_tokens=True,
        max_length=128
    )
    with torch.no_grad(): # 그라디엔트 계산 비활성화
        outputs = model( # **tokenized_sent -> 명시적으로 표시하기 위해 아래로 표현
            input_ids = tokenized_sent['input_ids'],
            attention_mask = tokenized_sent['attention_mask'],
            token_type_ids = tokenized_sent['token_type_ids']
        )
    logits = outputs.last_hidden_state[:, 0, :].detach().cpu().numpy()
    return logits

final_data_cls_hidden = np.load('final_data_cls_hidden_save.npy')
answer = pd.read_csv('answer.csv')['0']

app = FastAPI()

@app.post("/question")
async def model_endpoint(query: str = Form(...)):
    
    query_cls_hidden = get_cls_token(query)
    cos_sim = cosine_similarity(query_cls_hidden, final_data_cls_hidden)
    
    top_question = np.argmax(cos_sim)
    
    result = answer[top_question]
    
    print(result)
    
    return {'answer':result}