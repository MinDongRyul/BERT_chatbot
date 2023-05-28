import streamlit as st

import requests
import base64

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
set_background('bg2.jpg')

st.title('cosine유사도를 통한 Chatbot')

if 'chat_num' not in st.session_state:
    st.session_state['chat_num'] = 1

for i in range(st.session_state['chat_num']):
    me, ques =  st.columns([0.8, 9])
    
    with me:
        st.text_input(f'me_{i}', '나', label_visibility='hidden')

    with ques:
        query = st.text_input(f'query_{i}', '', label_visibility='hidden')
    
    if query == '이제 난 갈게':
        st.text_input(f'end', '채팅이 종료되었습니다.', label_visibility='hidden')
        break
        
    if len(query) > 0:
        response = requests.post('http://localhost:8000/question', data={'query':query})
        if response.ok:
            res = response.json()
            chat, ans =  st.columns([0.8, 9])
            with chat:
                st.text_input(f'chat_{i}', '챗봇', label_visibility='hidden')
            with ans:
                st.text_input(f'ans_{i}',res['answer'], disabled=False, label_visibility='hidden')
        else:
            st.write(res)
    st.session_state['chat_num'] += 1