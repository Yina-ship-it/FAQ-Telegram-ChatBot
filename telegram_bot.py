from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import telebot
import pandas as pd

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
    
    def setup(self):
        self.initialize_qa_model("neural_network_model")

        @self.bot.message_handler(commands= 'start', content_types= 'text')
        def start(message):
            self.bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}!")


        @self.bot.message_handler(content_types=['text'])
        def answer_question(message):
            try:
                self.bot.send_chat_action(message.chat.id, 'typing')
                answer = self.get_model_response(message.text)
                self.bot.send_message(message.chat.id, answer)
            except Exception as e:
                print(e)
                self.bot.send_message(message.chat.id, "Я вас немного не понял, переформулируйте свой впорос, либо уточните свой вопрос в онлайн чате у нас на сайте")

    def start(self):
        self.bot.polling()

    def initialize_qa_model(self,model_directory):
        with open("resources/Context.txt", "r", encoding="utf-8") as file:
            self.context = file.read()
        start_index = 0
        self.answers = {}
        df = pd.read_csv('resources/answers.csv')
        n = len(df)
        for i in range(1, n):
            idx = f"{i + 1}."
            end_index = self.context.find(idx)
            self.answers[range(start_index, end_index)] = df.loc[i - 1]["Text"]
            start_index = end_index
        self.answers[range(start_index,len(self.context) - 1)] = df.loc[n - 1]["Text"]
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_directory)
            self.model = AutoModelForQuestionAnswering.from_pretrained(model_directory)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
        
    def get_model_response(self,question):
        nlp = pipeline("question-answering", model=self.model, tokenizer=self.tokenizer)
        answerInf = nlp(question=question, context=self.context)
        print(answerInf)
        if answerInf["score"] < 0.10:
            raise LowConfidenceError(answerInf["score"]) 
        for key in self.answers:
            if answerInf["start"] + 1 in key:
                return self.answers[key]
            
        raise KeyError(answerInf["start"] + 1)
    
class LowConfidenceError(Exception):
    def __init__(self, score, message="Низкая уверенность в ответе"):
        self.score = score
        self.message = message
        super().__init__(self.message)

