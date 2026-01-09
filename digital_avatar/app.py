from dotenv import load_dotenv
from openai import OpenAI
import os
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)
google_api_key = os.getenv('GEMINI_API_KEY')
model_name= "gemini-2.5-flash"

class Me:

    def __init__(self):
        self.gemini = OpenAI(api_key=google_api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
        self.name = "Arun Pillai"
        reader = PdfReader("me/linkedin.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()

    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, instruct the user to reach out to {self.name} via Linkedin or email (arundeepak89@gmail.com). \
If the user is engaging in discussion, try to steer them towards getting in touch via Linkedin or email (arundeepak89@gmail.com)"

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        response = self.gemini.chat.completions.create(model=model_name, messages=messages)
        return response.choices[0].message.content
    

if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()
    