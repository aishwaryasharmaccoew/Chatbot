from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# cd /home/user
# git clone https://github.com/gunthercox/chatterbot-corpus
# cp -R chatterbot-corpus/chatterbot_corpus .

english_bot = ChatBot("Toad", storage_adapter="chatterbot.storage.SQLStorageAdapter",
                      database_uri='sqlite:///database.sqlite3', logic_adapters=[{
        'import_path': 'chatterbot.logic.BestMatch',
        'default_response': 'I am sorry, but I do not understand.',
        'maximum_similarity_threshold': 0.90
        }
    ])

trainer = ChatterBotCorpusTrainer(english_bot)
trainer.train('chatterbot.corpus.english')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(english_bot.get_response(userText))


if __name__ == "__main__":
    app.run()
