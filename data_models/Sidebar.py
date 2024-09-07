import streamlit as st
from config import OPENAI_API_KEY , OPENAI_MODEL
from openai import OpenAI


class OpenAI_LLM:
    api_key = OPENAI_API_KEY
    model_name = OPENAI_MODEL

    def __init__(self) -> None:
        self.client = OpenAI(api_key=self.api_key)

    
    def get_reponse(self , chat_history)->str:
        completion = self.client.chat.completions.create(
            model = self.model_name,
            messages = [{"role" : message['sender'], "content" : message["message"] } for message in chat_history]
        )
        return completion.choices[0].message.content



class Chatbot:

    chat_history = []
    loading_reponse = False 
    llm = OpenAI_LLM()
    
    def render(self, parent: st.delta_generator.DeltaGenerator):
        
        chat_container=parent.container(height=500,border=True)
        
        chat_container.empty()
        # print(chat_container)
        chat_input = parent.chat_input("How can I help you?")
        # self.chat_history.append({"sender" : "user" , "message" : parent.chat_input("How can I help you?")})
        if chat_input:
            
            self.chat_history.append({"sender" : "user" , "message" : chat_input})


        self.render_chats(chat_container)

    def render_chats(self , chat_container):
        with chat_container:
            for message in self.chat_history:
                st.chat_message(message["sender"]).write(message["message"])

            if self.chat_history and self.chat_history[-1]["sender"] == "user":
                bot_reponse = self.llm.get_reponse(self.chat_history)
                self.chat_history.append({"sender" : "assistant" , "message" : bot_reponse})
                st.chat_message("assistant").write(bot_reponse)





class Sidebar : 
    element = st.sidebar
    parent = None
    chatbot : Chatbot = Chatbot()
    def render(self):
        
        side=self.element.subheader("Ask In-Q Center")
        self.chatbot.render(self.element)

    def set_parent(self , parent):
        self.parent=parent
        

        