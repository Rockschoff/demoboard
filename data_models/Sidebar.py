import streamlit as st
from config import OPENAI_API_KEY , OPENAI_MODEL
from openai import OpenAI
from enum import Enum




class OpenAI_LLM:
    api_key = OPENAI_API_KEY
    model_name = OPENAI_MODEL

    def __init__(self) -> None:
        self.client = OpenAI(api_key=self.api_key)
        self.system_message = """You are helpful asstant that help people navigate the grpahs and visulations in the IN_Q center dashboard
         You are FDA Assitant that is alwasys gives actianlbe steps to insights and  ties the insights from the dasboard with FDA rules and regualtions.
         Here is all the information that is available to you from the dashbaord. In the app data that is provided to you always look at the metrics coming from different charts and address them to the user""" 

    
    def get_reponse(self , chat_history)->str:

        self.system_message= self.system_message+ f"{st.session_state.app.generate_app_state()}" + """ Please make good use of this infomration to answer the user queries"""
        completion = self.client.chat.completions.create(
            model = self.model_name,
            messages = [{"role" : "system" , "content" : self.system_message}]+[{"role" : message['sender'], "content" : message["message"] } for message in chat_history]
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
        

        