import streamlit as st
from streamlit_chat import message
import requests
import base64

# def get_base64(bin_file):
#     with open(bin_file, 'rb') as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
        
# def set_background(png_file):
#     bin_str = get_base64(png_file)
#     page_bg_img = '''
#     <style>
#     .stApp {
#     background-image: url("data:image/png;base64,%s");
#     background-size: cover;
#     }
#     </style>
#     ''' % bin_str
#     st.markdown(page_bg_img, unsafe_allow_html=True)
# set_background('bg2.jpg')

def update_log(user_message, bot_message):
    if 'chat_log' not in st.session_state:
        st.session_state.chat_log = {'user_message': [], 'bot_message': []}

    st.session_state.chat_log['user_message'].append(user_message)
    st.session_state.chat_log['bot_message'].append(bot_message)

    return st.session_state.chat_log

def get_answer(query):
    response = requests.post('http://localhost:8503/question', data={'query':query})
    output = response.json()['answer']
    return output

st.title('cosine유사도를 통한 Chatbot')

st.text_input("type a message..", key="user_message")
        
if user_message := st.session_state['user_message']:
    output = get_answer(user_message)
    # message(user_message, is_user=True)
    # message(output)
    chat_log = update_log(user_message, output)

    bot_messages = chat_log['bot_message'][::-1]
    user_messages = chat_log['user_message'][::-1]

    for idx, (bot, user) in enumerate(zip(bot_messages, user_messages)):
        message(user, key=f"{idx}_user", is_user=True)
        message(bot, key=f"{idx}_bot")


# if 'chat_num' not in st.session_state:
#     st.session_state['chat_num'] = 1

# for i in range(st.session_state['chat_num']):
#     me, ques =  st.columns([0.8, 9])
    
#     with me:
#         st.text_input(f'me_{i}', '나', label_visibility='hidden')

#     with ques:
#         query = st.text_input(f'query_{i}', '', label_visibility='hidden')
    
#     if query == '이제 난 갈게':
#         st.text_input(f'end', '채팅이 종료되었습니다.', label_visibility='hidden')
#         break
        
#     if len(query) > 0:
#         response = requests.post('http://localhost:8000/question', data={'query':query})
#         if response.ok:
#             res = response.json()
#             chat, ans =  st.columns([0.8, 9])
#             with chat:
#                 st.text_input(f'chat_{i}', '챗봇', label_visibility='hidden')
#             with ans:
#                 st.text_input(f'ans_{i}',res['answer'], disabled=False, label_visibility='hidden')
#         else:
#             st.write(res)
#     st.session_state['chat_num'] += 1
