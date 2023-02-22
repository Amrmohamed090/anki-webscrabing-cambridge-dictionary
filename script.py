from py_anki import AnkiApi
import json
import requests
from bs4 import BeautifulSoup

def add_to_anki(word, noun_or_verb, meanings_list, sentense, audio_link):
    print("add to anki::function started")
    audio_file_name=audio_link.split('/')[-1]
    anki = AnkiApi()
    print("add to anki::finding word in sentence started")
    index = sentense.lower().find(word.lower())
    sentense = sentense[:index] + "<strong style='color:green;font-size:25px;'>" + sentense[index:index+len(word)] + "</strong>" + sentense[index+len(word):]
    print("add to anki::finding word in sentence finished")
    back = word + ' - ' + noun_or_verb +'<br> <br>'
    count = 0
    
    for meaning in meanings_list:
        back += meaning[:len(meaning)-1] + '<br> <br>'
        count +=1
        if count == 4:
            break
    
    
    # store audio from the web for Note 1
    print("add to anki::fetching audio")
    note1_audio1 = anki.fetch_audio(
    url=audio_link, 
    filename=audio_file_name, 
    fields=['Back']
    )
    print("add to anki::fetching audio finished")
    print("add to anki::creating notes started")
    note1 = anki.create_note(
    field_vals=[sentense, back],
    deck_name='ay',
    model_name='Basic',
    audios=[note1_audio1],
    making_note_list=True
    )
    print("add to anki::creating notes finished")


    # store list of notes
    notes = anki.create_notes([note1])

    # execute the query
    print("add to anki::executing query started")
    anki.exec(notes)
    print("add to anki::executing query finished")




def scrap(search_field):
    #the word to search
    print("scrap::search started")
    try:
        search_field = search_field.lower()
        
        
        headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0"
        }
        url = "https://dictionary.cambridge.org/dictionary/english/"+ search_field
        print("scrap::request get called")
        r = requests.get(url, headers=headers)
        print("scrap::request returned")
        soup = BeautifulSoup(r.content, "html.parser")
        print("scrap::soup object creatred")
        print("scrap::finding word started")
        word = soup.find_all("span", {"class": "hw dhw"})[0].text
        print("scrap::finding word finished")
    except:
        return False,False,False,False,False

    print("scrap::finding noun_or_verb Started")
    noun_or_verb = soup.find_all("span", {"class": "pos dpos"})[0].text
    print("scrap::finding noun_or_verb finished")
    print("scrap::finding meanings Started")
    meanings = soup.find_all("div", {"class": "def ddef_d db"})
    print("scrap::finding meanings finished")
    meanings_list = []
    for meaning in meanings:
        meanings_list.append("- " + str(meaning.text))
   
    print("scrap::finding sentenses Started")
    sentenses = soup.find_all("span", {"class": "eg deg"})
    sentenses_list = []
    for sentens in sentenses:
        sentenses_list.append(str(sentens.text))
        
    print("scrap::finding sentenses finished")
    audio_link = f"https://ssl.gstatic.com/dictionary/static/sounds/oxford/{search_field}--_us_1.mp3"
    return word, noun_or_verb, meanings_list, sentenses_list, audio_link
    
    
    
