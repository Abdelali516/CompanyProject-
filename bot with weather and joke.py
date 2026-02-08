import requests
import time
import random

API_JOKE="https://official-joke-api.appspot.com/jokes/random"

API_KEY_WEATHER="16c97252f712255f5a259158bb44c3bc"
API_FOR_WEATHER="https://api.openweathermap.org/data/2.5/weather"

def load_user_name():
    try:
        with open("name_file.txt","r") as file:
            name=file.read().strip()
            print(f"Bot: Welcome Back {name.title()}.") 
            return name
    except FileNotFoundError:
        with open("name_file.txt","w") as file:
            name=input("Bot: Hi i am your Chat Bot what's your name:").lower().strip()
            file.write(name)
            return name
        
def jokes():
    try:
        response=requests.get(API_JOKE)
        if response.status_code==200:
            data=response.json()
            return f"Bot: {data['setup']}\n{data['punchline']}."
        elif response.status_code==429:
            return "Bot: sorry i couldn't find a joke due to too many requests."
        elif response.status_code==404:
           return "Bot: Sorry i couldn't find a joke."
    except requests.exceptions.RequestException as e:
        return f"Bot: Request Failed : {e}"
    
def city_weather(city):
    params={
        "q":city,
        "appid":API_KEY_WEATHER,
        "units":"metric"
    }
    try:
        response=requests.get(API_FOR_WEATHER,params=params)
        if response.status_code==200:
            data=response.json()
            temp=data["main"]["temp"]
            desc=data["weather"][0]["description"]
            return f"Bot: {city.title()} has a temperature of {temp}°C and {desc}."
        elif response.status_code==404:
            return "Bot: Please check the city name."
        elif response.status_code==401:
            return "Bot: Please your API Key."
    except requests.exceptions.RequestException as e:
        return f"Bot: Request Faled : {e}"


RESPONSES={
    ("hey","hi","hello","wassup","what's up"):
    ["Hi how are you ?","Hello there how are you ?"],
    
    ("i am good","i am fine","i am ok","i'm good","i'm fine","i'm ok"):
    ["Happy to hear it, i am also fine by the way. So how was your day ?","Glad to hear it, i am also good by the way. So any plans for this weekend ?"],

    ("it was ok","it was so so","it was good"):
    ["Well i hope it gets better.","Hope it gets better."],

    ("it was bad","it wasn't good","it wasn't"):
    ["Sorry to hear that, i hope it gets better."],

    ("no plans","not yet","no nothing"):
    ["I pretty sure you will find some to do in this weekend."],

    ("yes i have some","yes i have","yeah i have","yeah i have some"):
    ["Have fun then.","Enoy them."],

    ("yes everything is good","yes everything is alright","yes","yeah"):
    ["Glad to hear it.","Happy to hear it"],

    ("no","not really"):
    ["Well i am sorry to hear it but i am just a bot with a limited list, i am affraid i can't help you !"],

    ("thanks","thank you","you're right","you are right"):
    ["You're Welcome.","Anytime."]
}

GOODBYES={
    ("i have to go","see you","bye","talk to you later"):
    ["See you later, it was nice talking to you.","Hope to see you soon, it was fun talking to you."]
}

MOODS={
    "good":("good","great","happy","awesome"),
    "bad":("bad","angry","mad","sad","tired","worried","shit")
}

MOOD_SENTENCES=("i feel","i am","i'm")
WETHER_SENTENCES=("the weather in","weather of","temperature in","temperature of")
JOKE_SENETNCES=("tell me a joke","play me a joke","give me a joke","wanna hear a joke","joke")

def normalize(text):
    return text.lower().strip()

def get_responses(message):
    for key,replies in RESPONSES.items():
        for keys in key:
            if keys in message:
                return random.choice(replies)

def get_goodbye(message):
    for key,replies in GOODBYES.items():
        for keys in key:
            if keys in message:
                return random.choice(replies)
            
def detect_moods(message):
    for keys,replie in MOODS.items():
        for replies in replie:
            if replies in message:
                return keys

def detect_mood_sentences(message):
    for words in MOOD_SENTENCES:
        if words in message:
            return True
    return False

def detect_joke(message):
    for words in JOKE_SENETNCES:
        if words in message:
            return True
    return False

def detect_city(message):
    for words in WETHER_SENTENCES:
        if words in message:
            index=message.index(words)+len(words)
            next_word=message[index:]
            if next_word:
                return next_word.split()[0]

def thinking():
    print("Hmm",end="",flush=True)
    number=random.randint(2,4)
    for i in range(number):
        time.sleep(0.5)
        print(".",end="",flush=True)
    print()

conversation_state={
    "mood":None
}

with open("Conversation_2.txt","a") as file:
    file.write("\n====== NEW HISTORY ======\n")

name=load_user_name()
while True:
    with open("Conversation_2.txt","a") as file:
        user_input=normalize(input(f"{name.title()}:"))
        if not user_input:
            print("Bot: You forgot to type something.")
            continue
        
        bot_goodbye=get_goodbye(user_input)
        if bot_goodbye:
            thinking()
            print("Bot:",bot_goodbye)
            file.write(f"\n{name.title()}: {user_input}\nBot: {bot_goodbye}\n")
            break

        user_mood=detect_moods(user_input)
        mood_sentences=detect_mood_sentences(user_input)
        last_mood=conversation_state["mood"]
        if mood_sentences and user_mood:
            conversation_state["mood"]=user_mood
            if last_mood=="good" and user_mood=="bad":
                thinking()
                print("Bot: Earlier you seemed good,is everything still ok.")
                file.write(f"\n{name.title()}: {user_input}\nBot: Earlier you seemed good,is everything still ok.\n")
                continue
            elif last_mood=="bad" and user_mood=="good":
                thinking()
                print("Bot: Earlier you seemed down, happy that you feel good now.")
                file.write(f"\n{name.title()}: {user_input}\nBot: Earlier you seemed down, happy that you feel good now.\n")
                continue

        play_joke=jokes()
        if detect_joke(user_input):
            thinking()
            print(play_joke)
            file.write(f"\n{name.title()}: {user_input}\nBot:{play_joke}")
            continue

        city_name=detect_city(user_input)
        weather=city_weather(city_name)
        if city_name:
            thinking()
            print(weather)
            file.write(f"\n{name.title()}: {user_input}\nBot:{weather}")
            continue

        bot_responses=get_responses(user_input)
        if bot_responses:
            thinking()
            print("Bot:",bot_responses)
            file.write(f"\n{name.title()}: {user_input}\nBot: {bot_responses}\n")
        else:
            thinking()
            print("Bot: Sorry but can you rephrase that.")
            file.write(f"\n{name.title()}: {user_input}\nBot: Sorry but can you rephrase that.\n")
