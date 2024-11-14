import tkinter as tk
import datetime
import random
from pydoc import describe

import dateutil.parser
import requests
import nltk
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tkinter import scrolledtext

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))


#malagasy stopwords list
malagasy_stopwords =[
    "ny", "ao", "dia", "amin'ny", "fa", "sy", "izay", "ka", "avy", "rehetra", "dia", "ity", "efa", "anefa", "hoy", "ao", "no", "hoe", "mbola",  "tsy", "avy", "izao", "tena", "ve", "toa", "raha", "ihany", "misy" ,"indray"
]

stop_words = set (stopwords.words('english'))
weather_keywords = [
    "toetr'andro", "toetrin'ny andro", "toetrandro", "mari-pana", "maripana", "hafanàna", "meteo", "andro", "ho avy ve ny oarana?", "ho avy ve ny orana", "ahoana ny andro androany", "hafana ve ny andro?", "hafana ve ny andro", "hangatsiaka ve androany?", "hangatsiaka ve ny androany",
]




api_url = "http://api.openweathermap.org/data/2.5/weather"
api_key = "bcde802327c9af40150c26581e1a50ec"  
location = "Antananarivo"  


response = requests.get(api_url, params={
    "q": location,
    "appid": api_key,
    "units": "metric"  
})

days_in_malagasy = {
    'Monday': 'Alatsinainy',
    'Tuesday': 'Talata',
    'Wednesday': 'Alarobia',
    'Thursday': 'Alakamisy',
    'Friday': 'Zoma',
    'Saturday': 'Sabotsy',
    'Sunday': 'Alahady'
}
months_in_malagasy = {
    'January': 'Janoary',
    'February': 'Febroary',
    'March': 'Marta',
    'April': 'Aprily',
    'May': 'Mey',
    'June': 'Jona',
    'July': 'Jolay',
    'August': 'Aogositra',
    'September': 'Septambra',
    'October': 'Oktobra',
    'November': 'Novambra',
    'December': 'Desambra'
}

weather_translations = {
    "clear sky": "hibaliaka ny masoandro",
    "few clouds": "mety handrahona kely",
    "scattered clouds": "ho rahona mikirindro",
    "broken clouds": "rahona maro",
    "shower rain": "orambe ",
    "thunderstorm": "hisy kotroka sy tselatra",
    "mist": "rakotra zavona"
}

intents = {
    "get_time": ["ora", "am firy", "amfiry zao","am firy zao", "firy ny ora", "amin'ny firy izao", "firy ny amin’izao", "amin'ny firy", "te-hahafantatra ny ora", "inona ny ora"],
    "greet": ["manao ahoana", "manaona","aona" ,"manao akory", "salama tompoko", "Salama", "Bonjour", "salama", "bonjour", "miarahaba","Miarahaba"],
    "thank": ["misaotra", "misaotra tompoko", "merci", "saotra"],
    "get_date": ["daty", "inona androany?", "le firy androany?","firy androany", "firy androany","firy ny daty androany","inona isika androany?","inona isika androany","" "firy ny daty androany?", "fahafiry ny volana androany"],
    "apology": ["azafady tompoko", "miala tsiny tompoko", "azafady"],
    "get_weather": ["hanao ahoana ny toetrin'ny andro","aona androany?", "inona ny toetr'andro", "firy ny maripana androany", "mety ho avy ve ny orana", "toetr'andro any"]

}
apology_response = [
    "tsy misy tsiny tompoko",
    "tsy misy olana tompoko ny amin'izany",
    "aza manahy tompoko",
    "tsy maninona tompoko"
]
thank_responses = [
    "Misaotra anao tompoko",
    "Ianao tompoko no isaorana",
    "mankasitraka indrindra tompoko"
]

greet_responses = [
    "Salama e! Inona no azo atao ho anao?",
    "Manao ahoana ianao!",
    "Salama tompoko! misy afaka azoko hanampiana anao ve?",
    "Miarahaba, inona ny vaovao?",
    "Salama oh"
]

date_responses = [
    "Ny andro androany dia {date}.",
    "Androany dia {date}",
    " {date} androany",
    "{date} isika anio"
]


def preprocess_text_malagasy(user_input):
    tokens = user_input.split()
    filtered_tokens = [token for token in tokens  if token.lower() not in malagasy_stopwords]
    return ' '.join(filtered_tokens)

def preprocess_text(user_input):
    tokens = word_tokenize(user_input.lower())
    filtered_tokens = [ token for token in tokens if token not in stop_words]
    return filtered_tokens


def get_weather_intent(user_input):
    user_input = user_input.lower()

    tokens = word_tokenize(user_input)  # Tokenize user input

    # Check for a match with any of the weather keywords
    for keyword in weather_keywords:
        if any(keyword in token for token in tokens):
            return "get_weather"

    return "unknown"


user_input = "Ahoana ny maripana androany?"
intent = get_weather_intent(user_input)


if intent == "get_weather":
    print("Te hafantatra ny toetrandro ")
else:
    print("tsy misy fanotaniana momba ny toetrandro")

import requests


def get_weather(location="Antananarivo", api_key="bcde802327c9af40150c26581e1a50ec"):
    api_url = "https://api.openweathermap.org/data/2.5/weather"
    try:
        response = requests.get(api_url, params={
            "q": location,
            "appid": api_key,
            "units": "metric"
        })
        data = response.json()

        if data.get("cod") != 200:
            return "Miala tsiny, tsy afaka maka ny vaovao momba ny toetrandro amin'izao fotoana izao."


        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }
        return weather_info
    except requests.exceptions.RequestException:
        return "Miala tsiny, misy olana amin'ny fifandraisana amin'ny serivisy toetrandro."


def chatbot():
    #tongasoa eto @ chatbot
    print(" " * 20 + "Tongasoa eto amin'ny chatbot!")  # Centered greeting

    weather_info = get_weather()  # Fetch weather info
    if isinstance(weather_info, dict):
        # meteo info
        print(" " * 20 + f"Toetrandro ankehitriny any {weather_info['city']}:")
        print(" " * 20 + f"{weather_info['temperature']}°C, {weather_info['description']}.")
        print(" " * 20 + "Mety ho mangatsiaka androany, mitondrà fiarovana amin'ny rivotra.")
    else:
        print(" " * 20 + weather_info)

    print("\nAhoana no ahafahako manampy anao androany?")

    #
    while True:
        user_input = input("Ianao: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Misaotra nanandrana ny chatbot. Veloma!")
            break
        else:
            print("Bot: Miala tsiny fa tsy azoko tsara ny tianao holazaina.")
            time.sleep(1)


if __name__ == "__main__":
    chatbot()







#def get_weather_info(location="Antananarivo"):
 #   api_key = "bcde802327c9af40150c26581e1a50ec"  # Your API key
  #  api_url = "http://api.openweathermap.org/data/2.5/weather"

    #try:
       # response = requests.get(api_url, params={
       #     "q": location,
       #     "appid": api_key,
       #     "units": "metric",
       # })
        #weather_data = response.json()

      #  if response.status_code == 200:
          #  temperature = weather_data['main']['temp']
          #  weather_description = weather_data['weather'][0]['description']
           # advice = "Aza adino ny mitondra fiarovana amin'ny toetr'andro!"

            #return f"Amin'izao fotoana izao, {location} dia misy {weather_description} ary ny mari-pana dia {temperature}°C. {advice}"
        #else:
          #  return "Miala tsiny, tsy afaka mahazo vaovao momba ny toetr'andro izahay amin'izao fotoana izao."
    #except requests.exceptions.RequestException as e:
      #  return "Miala tsiny, misy olana amin'ny fangatahana."


def chatbot_intro():
    # Display the polite greeting and weather information
    print("Tongasoa eto amin'ny chatbot!")
    weather_info = get_weather_info()
    print(weather_info)
    # Continue with the chatbot conversation here


# Start the conversation and show the polite greeting and weather info
chatbot_intro()


#preprocess text in chatbot's response
def chatbot_response(user_input):
#preprocess input to remove sw
    processed_input =  preprocess_text(user_input)
    intent = get_itent(processed_input)

    if intent == "get weather":
        return get_weather("Antananrivo")
    elif intent == "get time":
        return f"amin'izao dia {datetime.datetime.now.strftime('%H:%M:%S')}"
    elif intent == "greet":
        return random.choice(greet_responses)
    else :
        return "Miala tsiny fa tsy azoko tsara ny tianao lazaina"




def translate_weather(description):
    return weather_translations.get(description, description)

def translate_date_to_malagasy(date):
    day_name = date.strftime('%A')
    month_name = date.strftime('%B')
    
    malagasy_day = days_in_malagasy.get(day_name, day_name)
    malagasy_month = months_in_malagasy.get(month_name, month_name)
    
    formatted_date = f"{malagasy_day}, {malagasy_month} {date.day}, {date.year}"
    return formatted_date

def get_weather_advice(description, temperature):
    if "rain" in description or "showers" in description:
        return "Mety hilatsaka ny orana, ka tsara raha mitondra elo."
    elif "cloud" in description:
        return "Mety andrahona, ka tsara raha mivonona amin'ny filatsahan'ny orana tsy ampoizina."
    elif temperature < 20:
        return "Vinavinaina hangatsiaka tokoa ny andro anio, ka aza atao alavitra ny akanjo mafana sy ny rano mafana."
    elif temperature > 29:
        return "Vinavinaina hafana tokoa ny andro androany, noho izany aza adino ny misotro rano sy manao akanjo maivana."

def get_weather(city):
    api_key = "bcde802327c9af40150c26581e1a50ec"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)


    if response.status_code == 200:
        data = response.json()
        temp = data ['main']['temp']
        description = data ['weather'][0]['description']

        malagasy_description = translate_weather(description)
        advice = get_weather_advice(malagasy_description, temp)

        return f"Ny mari-pana ao {city} dia {temp}°C ary {malagasy_description}, {advice} ."
    else :
        return "Miala tsiny, tsy afakama mahazo ny vaovao momba ny toetr'andro aho."


print (get_weather("Antananarivo"))

















def get_intent(user_input):
    user_input = user_input.lower()  
    for intent, keywords in intents.items():
        if any(keyword in user_input for keyword in keywords):
            return intent
    return "unknown"

def chatbot_response(user_input):
    intent = get_intent(user_input)
    if intent == "get_weather":
       city_name = "Antananarivo"
       return get_weather(city_name)
    elif intent == "get_time":
        return f"amin'izao dia {datetime.datetime.now().strftime('%H:%M:%S')}"
    elif intent == "greet":
        return random.choice(greet_responses)
    elif intent == "thank":
        return random.choice(thank_responses)
    elif intent == "apology":
        return random.choice(apology_response)
    elif intent == "get_date":
        return handle_date_query(user_input)
    else:
        return "Miala tsiny fa tsy azoko tsara ny tianao holazaina."



def handle_weather_query(user_input):
    if "andro" in user_input or "toetrandro" in user_input:
        # Call the weather API and fetch data
        response = requests.get(api_url, params={
            "q": location,
            "appid": api_key,
            "units": "metric"
        })
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather = data["weather"][0]["description"]
            return f"Androany dia {weather}, ary ny mari-pana dia {temp}°C."
        else:
            return "Tsy afaka mahazo vaovao momba ny toetrandro aho izao."

user_input = "Ahoana ny andro any Antananarivo?"
print(handle_weather_query(user_input))


def handle_date_query(user_input):
   
    if "androany" in user_input or "rahampitso" in user_input:
        today = datetime.datetime.now()
        malagasy_date = translate_date_to_malagasy(today)
        return random.choice(date_responses).format(date=malagasy_date)
    
    try:
        parsed_date = dateutil.parser.parse(user_input, fuzzy=True)
        malagasy_date = translate_date_to_malagasy(parsed_date)  # Translate to Malagasy
        return random.choice(date_responses).format(date=malagasy_date)
    
    except (ValueError, TypeError):
        return "Tsy mazava amiko ilay daty tianao fantarina."
def send():
    user_input = entry.get() 
    if user_input.lower() == "veloma":
        chat_window.config(state='normal') 
        chat_window.insert(tk.END, "Bot: Misaotra anao! Mandrapihaona!\n")
        chat_window.config(state='disabled')  
        root.quit()
    else:
        chat_window.config(state='normal')  
        chat_window.insert(tk.END, f"Ianao: {user_input}\n")
        response = chatbot_response(user_input)
        chat_window.insert(tk.END, f"Bot: {response}\n")
        chat_window.config(state='disabled') 
        entry.delete(0, tk.END)  

root = tk.Tk()
root.title("Chatbot")

chat_window = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
chat_window.grid(row=0, column=0, padx=10, pady=10)

entry = tk.Entry(root, width=43)
entry.grid(row=1, column=0, padx=10, pady=10)


send_button = tk.Button(root, text="Alefaso", command=send)
send_button.grid(row=1, column=1)


entry.bind('<Return>', lambda event: send())
root.mainloop()
