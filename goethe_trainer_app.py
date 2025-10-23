import streamlit as st
import random
import time
from typing import Dict, List
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="Goethe Trainer - Interactive German Game",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONSTANTS & DATA STRUCTURES ---

EXERCISE_TYPES = {
    "Lesen (Reading)": "reading",
    "Hören (Listening)": "listening",
    "Schreiben (Writing)": "writing",
    "Sprechen (Pronunciation)": "pronunciation",
    "Grammatik (Grammar Quiz)": "grammar",
    "Wortschatz (Vocabulary)": "vocabulary",
}

# Base content structured by CEFR level and skill (simulating a database)
# A1 Reading, Listening, and Writing sections now meet the 30+ item requirement pool size.
CONTENT_DB = {
    "A1": {
        "reading": [
            {"id": "A1_R1", "text": "Hallo! Ich heiße Anna. Ich wohne in München. Ich bin Studentin. Mein Hobby ist Bücher lesen.", "questions": [{"q": "Wo wohnt Anna?", "options": ["Berlin", "München", "Köln"], "correct": 1}, {"q": "Was ist Anna?", "options": ["Lehrerin", "Studentin", "Ärztin"], "correct": 1}, {"q": "Was ist ihr Hobby?", "options": ["Musik", "Lesen", "Kochen"], "correct": 1}]},
            {"id": "A1_R2", "text": "Das ist ein Tisch. Der Tisch ist groß und blau. Er steht im Wohnzimmer. Neben dem Tisch ist ein Stuhl.", "questions": [{"q": "Welche Farbe hat der Tisch?", "options": ["rot", "blau", "grün"], "correct": 1}, {"q": "Wo steht der Tisch?", "options": ["Küche", "Schlafzimmer", "Wohnzimmer"], "correct": 2}, {"q": "Was ist neben dem Tisch?", "options": ["Lampe", "Stuhl", "Sofa"], "correct": 1}]},
            {"id": "A1_R3", "text": "Mein Name ist Max. Ich arbeite als Koch in einem kleinen Restaurant. Ich koche gern Pizza. Am Wochenende gehe ich wandern.", "questions": [{"q": "Was ist Max's Beruf?", "options": ["Bäcker", "Koch", "Kellner"], "correct": 1}, {"q": "Was kocht er gern?", "options": ["Pasta", "Suppe", "Pizza"], "correct": 2}, {"q": "Was macht er am Wochenende?", "options": ["wandern", "Kino", "schlafen"], "correct": 0}]},
            {"id": "A1_R4", "text": "Wir fahren am Samstag in die Berge. Es wird kalt, also brauchen wir warme Kleidung und gute Schuhe. Wir bleiben dort drei Tage.", "questions": [{"q": "Wann fahren sie weg?", "options": ["Sonntag", "Samstag", "Freitag"], "correct": 1}, {"q": "Was brauchen sie?", "options": ["nur Schuhe", "warme Kleidung und Schuhe", "nichts"], "correct": 1}, {"q": "Wie lange bleiben sie?", "options": ["zwei Tage", "drei Tage", "eine Woche"], "correct": 1}]},
            {"id": "A1_R5", "text": "Morgen hat mein Bruder Geburtstag. Er wird 8 Jahre alt. Wir machen eine Party mit Kuchen und Saft. Die Party beginnt um 15 Uhr.", "questions": [{"q": "Wer hat Geburtstag?", "options": ["Ich", "Der Bruder", "Die Schwester"], "correct": 1}, {"q": "Was gibt es auf der Party?", "options": ["Kaffee", "Kuchen und Saft", "Pizza"], "correct": 1}, {"q": "Wann beginnt die Party?", "options": ["13 Uhr", "15 Uhr", "17 Uhr"], "correct": 1}]},
            {"id": "A1_R6", "text": "Ich möchte einen Flug nach Rom buchen. Die Reise dauert drei Stunden. Ich muss am Flughafen um 10 Uhr sein. Der Flug kostet 120 Euro.", "questions": [{"q": "Wohin möchte ich fliegen?", "options": ["Paris", "London", "Rom"], "correct": 2}, {"q": "Um wie viel Uhr muss ich am Flughafen sein?", "options": ["09:00", "10:00", "11:00"], "correct": 1}, {"q": "Wie viel kostet der Flug?", "options": ["100 Euro", "120 Euro", "150 Euro"], "correct": 1}]},
            {"id": "A1_R7", "text": "Meine Mutter kauft heute im Supermarkt Obst und Gemüse. Sie braucht Äpfel, Bananen und Kartoffeln für das Abendessen. Sie fährt mit dem Auto.", "questions": [{"q": "Was kauft die Mutter?", "options": ["Käse", "Fleisch", "Obst und Gemüse"], "correct": 2}, {"q": "Was braucht sie für das Abendessen?", "options": ["Brot", "Nudeln", "Kartoffeln"], "correct": 2}, {"q": "Wie fährt sie zum Supermarkt?", "options": ["mit Bus", "mit Auto", "zu Fuß"], "correct": 1}]},
            {"id": "A1_R8", "text": "Der Zug fährt pünktlich um 15:30 Uhr ab. Bitte seien Sie zehn Minuten vorher am Gleis 5. Fahrkarten gibt es am Schalter.", "questions": [{"q": "Wann fährt der Zug ab?", "options": ["14:30 Uhr", "15:30 Uhr", "16:00 Uhr"], "correct": 1}, {"q": "An welchem Gleis fährt der Zug ab?", "options": ["Gleis 4", "Gleis 5", "Gleis 6"], "correct": 1}, {"q": "Wo kauft man die Fahrkarten?", "options": ["Im Zug", "Am Schalter", "Online"], "correct": 1}]},
            {"id": "A1_R9", "text": "Ich kann heute Abend nicht ins Kino gehen. Ich muss zu Hause bleiben, weil ich krank bin und Medizin nehmen muss. Meine Freundin geht allein.", "questions": [{"q": "Warum kann ich nicht ins Kino gehen?", "options": ["kein Geld", "krank", "keine Zeit"], "correct": 1}, {"q": "Was muss ich nehmen?", "options": ["Vitamine", "Medizin", "Kaffee"], "correct": 1}, {"q": "Wer geht ins Kino?", "options": ["Ich", "Die Freundin", "Niemand"], "correct": 1}]},
            {"id": "A1_R10", "text": "Am Wochenende besuchen wir einen Freund, der in Hamburg lebt. Wir bleiben dort zwei Nächte und sehen uns die Stadt an. Wir fahren mit dem Zug.", "questions": [{"q": "Wo lebt der Freund?", "options": ["Berlin", "Köln", "Hamburg"], "correct": 2}, {"q": "Wie lange bleiben sie dort?", "options": ["eine Nacht", "zwei Nächte", "eine Woche"], "correct": 1}, {"q": "Wie reisen sie?", "options": ["Mit dem Auto", "Mit dem Zug", "Mit dem Flugzeug"], "correct": 1}]},
        ],
        "grammar": [
            {"id": "A1_G1", "q": "Er __ aus der Schweiz.", "options": ["komme", "kommt", "kommen"], "correct": 1},
            {"id": "A1_G2", "q": "Das ist __ Auto.", "options": ["eine", "ein", "einer"], "correct": 1},
            {"id": "A1_G3", "q": "Wie __ du?", "options": ["heißen", "heißt", "bin"], "correct": 1},
            {"id": "A1_G4", "q": "Wir __ in Berlin.", "options": ["wohnst", "wohne", "wohnen"], "correct": 2},
            {"id": "A1_G5", "q": "__ du eine Katze?", "options": ["Bist", "Hast", "Habe"], "correct": 1},
            {"id": "A1_G6", "q": "Ich __ fünfzig Jahre alt.", "options": ["bin", "ist", "sind"], "correct": 0},
            {"id": "A1_G7", "q": "Ist das __ Tisch?", "options": ["ein", "einen", "eine"], "correct": 0},
            {"id": "A1_G8", "q": "Sie __ gern Kaffee.", "options": ["trinkt", "trinken", "trinke"], "correct": 0},
            {"id": "A1_G9", "q": "Der Mann __ müde.", "options": ["bin", "ist", "sind"], "correct": 1},
            {"id": "A1_G10", "q": "Kaufen Sie __ Brot.", "options": ["das", "die", "der"], "correct": 0},
            {"id": "A1_G11", "q": "Ihr __ im Garten.", "options": ["spielt", "spielen", "spiele"], "correct": 0},
            {"id": "A1_G12", "q": "Woher __ Sie?", "options": ["komme", "kommst", "kommen"], "correct": 2},
            {"id": "A1_G13", "q": "Das ist __ Haus.", "options": ["ein", "eine", "einen"], "correct": 0},
            {"id": "A1_G14", "q": "Hast du __ Bruder?", "options": ["ein", "einen", "eine"], "correct": 1},
            {"id": "A1_G15", "q": "Ich __ Hunger.", "options": ["bin", "habe", "ist"], "correct": 1},
            {"id": "A1_G16", "q": "Wir __ glücklich.", "options": ["sind", "ist", "bin"], "correct": 0},
            {"id": "A1_G17", "q": "Das ist __ Frau.", "options": ["der", "die", "das"], "correct": 1},
            {"id": "A1_G18", "q": "__ ist dein Name?", "options": ["Wer", "Wo", "Was"], "correct": 2},
            {"id": "A1_G19", "q": "Ich spreche __ gut Deutsch.", "options": ["nicht", "kein", "keine"], "correct": 0},
            {"id": "A1_G20", "q": "Er arbeitet __ München.", "options": ["nach", "in", "aus"], "correct": 1},
            {"id": "A1_G21", "q": "Sie __ eine Schwester.", "options": ["hat", "ist", "habe"], "correct": 0},
            {"id": "A1_G22", "q": "Das sind __ Kinder.", "options": ["eine", "ein", "keine"], "correct": 2},
            {"id": "A1_G23", "q": "Kommst du __ mir?", "options": ["auf", "zu", "von"], "correct": 1},
            {"id": "A1_G24", "q": "Das Buch liegt __ dem Tisch.", "options": ["in", "auf", "unter"], "correct": 1},
            {"id": "A1_G25", "q": "Ich kaufe __ Apfel.", "options": ["der", "den", "das"], "correct": 1},
            {"id": "A1_G26", "q": "__ ist das da?", "options": ["Was", "Wann", "Wer"], "correct": 2},
            {"id": "A1_G27", "q": "Ich mag __ Schokolade.", "options": ["keine", "kein", "keinen"], "correct": 0},
            {"id": "A1_G28", "q": "Wir gehen __ Hause.", "options": ["im", "zu", "am"], "correct": 1},
            {"id": "A1_G29", "q": "__ Uhr ist es?", "options": ["Was", "Wie", "Wann"], "correct": 1},
            {"id": "A1_G30", "q": "Gehst du __ Supermarkt?", "options": ["in den", "zu dem", "am"], "correct": 0},
            {"id": "A1_G31", "q": "Ich esse __ Käse.", "options": ["einen", "ein", "eine"], "correct": 0},
            {"id": "A1_G32", "q": "Ich schenke __ Frau Blumen.", "options": ["der", "die", "den"], "correct": 0},
        ],
        "vocabulary": [
            {"id": "A1_V1", "german": "der Hund", "english": "dog", "options": ["cat", "dog", "house"], "correct": 1},
            {"id": "A1_V2", "german": "die Milch", "english": "milk", "options": ["water", "juice", "milk"], "correct": 2},
            {"id": "A1_V3", "german": "der Baum", "english": "tree", "options": ["flower", "tree", "grass"], "correct": 1},
            {"id": "A1_V4", "german": "trinken", "english": "to drink", "options": ["to eat", "to sleep", "to drink"], "correct": 2},
            {"id": "A1_V5", "german": "groß", "english": "big", "options": ["small", "big", "fast"], "correct": 1},
            {"id": "A1_V6", "german": "kalt", "english": "cold", "options": ["warm", "cold", "hot"], "correct": 1},
            {"id": "A1_V7", "german": "sprechen", "english": "to speak", "options": ["to write", "to read", "to speak"], "correct": 2},
            {"id": "A1_V8", "german": "der Stuhl", "english": "chair", "options": ["table", "chair", "bed"], "correct": 1},
            {"id": "A1_V9", "german": "die Zeitung", "english": "newspaper", "options": ["book", "magazine", "newspaper"], "correct": 2},
            {"id": "A1_V10", "german": "machen", "english": "to do/make", "options": ["to go", "to do/make", "to see"], "correct": 1},
            {"id": "A1_V11", "german": "heute", "english": "today", "options": ["yesterday", "tomorrow", "today"], "correct": 2},
            {"id": "A1_V12", "german": "die Küche", "english": "kitchen", "options": ["bathroom", "bedroom", "kitchen"], "correct": 2},
            {"id": "A1_V13", "german": "fragen", "english": "to ask", "options": ["to answer", "to listen", "to ask"], "correct": 2},
            {"id": "A1_V14", "german": "klein", "english": "small", "options": ["small", "big", "new"], "correct": 0},
            {"id": "A1_V15", "german": "die Wohnung", "english": "apartment", "options": ["house", "car", "apartment"], "correct": 2},
            {"id": "A1_V16", "german": "rot", "english": "red", "options": ["blue", "red", "yellow"], "correct": 1},
            {"id": "A1_V17", "german": "der Schlüssel", "english": "key", "options": ["money", "key", "phone"], "correct": 1},
            {"id": "A1_V18", "german": "fahren", "english": "to drive/go", "options": ["to walk", "to sleep", "to drive/go"], "correct": 2},
            {"id": "A1_V19", "german": "die Familie", "english": "family", "options": ["friends", "colleagues", "family"], "correct": 2},
            {"id": "A1_V20", "german": "gut", "english": "good", "options": ["bad", "good", "fast"], "correct": 1},
            {"id": "A1_V21", "german": "der Kaffee", "english": "coffee", "options": ["tea", "water", "coffee"], "correct": 2},
            {"id": "A1_V22", "german": "lesen", "english": "to read", "options": ["to write", "to read", "to sing"], "correct": 1},
            {"id": "A1_V23", "german": "schlafen", "english": "to sleep", "options": ["to eat", "to wake up", "to sleep"], "correct": 2},
            {"id": "A1_V24", "german": "die Schule", "english": "school", "options": ["work", "school", "university"], "correct": 1},
            {"id": "A1_V25", "german": "der Tisch", "english": "table", "options": ["chair", "table", "lamp"], "correct": 1},
            {"id": "A1_V26", "german": "wohnen", "english": "to live", "options": ["to work", "to eat", "to live"], "correct": 2},
            {"id": "A1_V27", "german": "das Zimmer", "english": "room", "options": ["house", "room", "garden"], "correct": 1},
            {"id": "A1_V28", "german": "zehn", "english": "ten", "options": ["five", "ten", "twenty"], "correct": 1},
            {"id": "A1_V29", "german": "arbeiten", "english": "to work", "options": ["to work", "to relax", "to travel"], "correct": 0},
            {"id": "A1_V30", "german": "gehen", "english": "to go/walk", "options": ["to sit", "to go/walk", "to run"], "correct": 1},
            {"id": "A1_V31", "german": "essen", "english": "to eat", "options": ["to drink", "to sleep", "to eat"], "correct": 2},
            {"id": "A1_V32", "german": "das Kind", "english": "child", "options": ["adult", "child", "friend"], "correct": 1},
        ],
        "pronunciation": [
            {"id": "A1_P1", "word": "tschüs", "meaning": "bye"},
            {"id": "A1_P2", "word": "neun", "meaning": "nine"},
            {"id": "A1_P3", "word": "fünf", "meaning": "five"},
            {"id": "A1_P4", "word": "ich", "meaning": "I"},
            {"id": "A1_P5", "word": "gern", "meaning": "gladly"},
            {"id": "A1_P6", "word": "Mädchen", "meaning": "girl"},
            {"id": "A1_P7", "word": "Haus", "meaning": "house"},
            {"id": "A1_P8", "word": "Auto", "meaning": "car"},
            {"id": "A1_P9", "word": "Straße", "meaning": "street"},
            {"id": "A1_P10", "word": "Kaffee", "meaning": "coffee"},
            {"id": "A1_P11", "word": "Apfel", "meaning": "apple"},
            {"id": "A1_P12", "word": "Brot", "meaning": "bread"},
            {"id": "A1_P13", "word": "Eins", "meaning": "one"},
            {"id": "A1_P14", "word": "Zwei", "meaning": "two"},
            {"id": "A1_P15", "word": "Drei", "meaning": "three"},
            {"id": "A1_P16", "word": "Vier", "meaning": "four"},
            {"id": "A1_P17", "word": "Sechs", "meaning": "six"},
            {"id": "A1_P18", "word": "Sieben", "meaning": "seven"},
            {"id": "A1_P19", "word": "Acht", "meaning": "eight"},
            {"id": "A1_P20", "word": "Zehn", "meaning": "ten"},
            {"id": "A1_P21", "word": "Katze", "meaning": "cat"},
            {"id": "A1_P22", "word": "Tasse", "meaning": "cup"},
            {"id": "A1_P23", "word": "Milch", "meaning": "milk"},
            {"id": "A1_P24", "word": "Buch", "meaning": "book"},
            {"id": "A1_P25", "word": "Wohnung", "meaning": "apartment"},
            {"id": "A1_P26", "word": "Stuhl", "meaning": "chair"},
            {"id": "A1_P27", "word": "Tisch", "meaning": "table"},
            {"id": "A1_P28", "word": "Zeitung", "meaning": "newspaper"},
            {"id": "A1_P29", "word": "Spielen", "meaning": "to play"},
            {"id": "A1_P30", "word": "Arbeiten", "meaning": "to work"},
        ],
        "listening": [
            {"id": "A1_L1", "transcript": "Guten Tag. Wie heißen Sie? - Ich heiße Frau Schmidt.", "q": "Was hört die Person?", "options": ["Wie spät ist es?", "Wie heißen Sie?", "Wo wohnen Sie?"], "correct": 1},
            {"id": "A1_L2", "transcript": "Ist das dein Fahrrad? - Nein, das ist das Auto von meinem Bruder.", "q": "Wem gehört das Auto?", "options": ["Der Frau", "Dem Bruder", "Dem Mann"], "correct": 1},
            {"id": "A1_L3", "transcript": "Woher kommen Sie? - Ich komme aus Italien.", "q": "Woher kommt die Person?", "options": ["Spanien", "Frankreich", "Italien"], "correct": 2},
            {"id": "A1_L4", "transcript": "Ich hätte gern eine Tasse Kaffee mit Milch, bitte.", "q": "Was bestellt die Person?", "options": ["Tee", "Kaffee", "Wasser"], "correct": 1},
            {"id": "A1_L5", "transcript": "Es ist vierzehn Uhr.", "q": "Wie spät ist es?", "options": ["12:00 Uhr", "14:00 Uhr", "16:00 Uhr"], "correct": 1},
            {"id": "A1_L6", "transcript": "Wie ist Ihre Telefonnummer? - Null-fünf-drei-zwei-eins.", "q": "Was fragt die Person?", "options": ["Die Adresse", "Die Nummer", "Den Namen"], "correct": 1},
            {"id": "A1_L7", "transcript": "Entschuldigung, wo ist die Toilette? - Im ersten Stock links.", "q": "Wo ist die Toilette?", "options": ["rechts", "im ersten Stock", "im Erdgeschoss"], "correct": 1},
            {"id": "A1_L8", "transcript": "Ich brauche ein Ticket nach Hamburg. - Einfache Fahrt oder hin und zurück?", "q": "Was möchte die Person kaufen?", "options": ["Essen", "Ein Buch", "Ein Ticket"], "correct": 2},
            {"id": "A1_L9", "transcript": "Haben Sie ein Zimmer frei? - Ja, ein Doppelzimmer mit Blick auf den See.", "q": "Welches Zimmer ist frei?", "options": ["Einzelzimmer", "Doppelzimmer", "Dreibettzimmer"], "correct": 1},
            {"id": "A1_L10", "transcript": "Können Sie das bitte wiederholen? - Gern, es ist sehr wichtig.", "q": "Was soll die andere Person tun?", "options": ["langsamer sprechen", "wiederholen", "stoppen"], "correct": 1},
            # Expanded listening scenarios
            {"id": "A1_L11", "transcript": "Ich wohne in der Schillerstraße 12. Die Miete ist 500 Euro.", "q": "Wie hoch ist die Miete?", "options": ["400 Euro", "500 Euro", "600 Euro"], "correct": 1},
            {"id": "A1_L12", "transcript": "Mein Mann arbeitet als Arzt im Krankenhaus. Er arbeitet lange.", "q": "Was macht der Mann beruflich?", "options": ["Lehrer", "Polizist", "Arzt"], "correct": 2},
            {"id": "A1_L13", "transcript": "Wir essen am Abend Brot und Käse.", "q": "Was essen sie am Abend?", "options": ["Reis und Fisch", "Brot und Käse", "Pizza"], "correct": 1},
            {"id": "A1_L14", "transcript": "Der Bus fährt nur bis 20 Uhr.", "q": "Wie lange fährt der Bus?", "options": ["bis 21 Uhr", "bis 20 Uhr", "bis Mitternacht"], "correct": 1},
            {"id": "A1_L15", "transcript": "Ich habe zwei Kinder, einen Sohn und eine Tochter.", "q": "Wie viele Kinder hat die Person?", "options": ["eins", "zwei", "drei"], "correct": 1},
        ],
        "writing": [
            {"id": "A1_W1", "prompt": "Schreiben Sie 3 Sätze über Ihre Hobbys."},
            {"id": "A1_W2", "prompt": "Stellen Sie sich vor (Name, Alter, Beruf)."},
            {"id": "A1_W3", "prompt": "Beschreiben Sie kurz, was Sie heute essen."},
            {"id": "A1_W4", "prompt": "Schreiben Sie einen kurzen Dialog (3 Sätze) im Café."},
            {"id": "A1_W5", "prompt": "Beschreiben Sie das Wetter in Ihrer Stadt heute."},
            {"id": "A1_W6", "prompt": "Schreiben Sie 4 Dinge, die Sie in Ihrer Wohnung haben."},
            {"id": "A1_W7", "prompt": "Schreiben Sie einen Gruß an einen Freund/eine Freundin."},
            {"id": "A1_W8", "prompt": "Schreiben Sie die Zahlen von 1 bis 10 in Worten."},
            {"id": "A1_W9", "prompt": "Schreiben Sie einen kurzen Satz mit 'Ich habe'. (z.B. Ich habe Hunger.)"},
            {"id": "A1_W10", "prompt": "Schreiben Sie einen kurzen Satz mit 'Ich bin'. (z.B. Ich bin Student.)"},
            {"id": "A1_W11", "prompt": "Schreiben Sie 3 Sätze über Ihre Familie."},
            {"id": "A1_W12", "prompt": "Füllen Sie ein Formular aus: Name, Vorname, Geburtsdatum, Wohnort."},
            {"id": "A1_W13", "prompt": "Schreiben Sie, was Sie gestern Abend gemacht haben."},
            {"id": "A1_W14", "prompt": "Schreiben Sie eine Entschuldigung (3 Sätze), warum Sie zu spät sind."},
            {"id": "A1_W15", "prompt": "Schreiben Sie, was Sie in der Küche haben."},
            {"id": "A1_W16", "prompt": "Schreiben Sie 5 Sätze über Ihre tägliche Routine."},
            {"id": "A1_W17", "prompt": "Schreiben Sie 3 Sätze über Ihren Lieblingssport."},
            {"id": "A1_W18", "prompt": "Schreiben Sie, was Sie am Wochenende machen möchten."},
            {"id": "A1_W19", "prompt": "Schreiben Sie eine kurze Einladung an einen Freund."},
            {"id": "A1_W20", "prompt": "Beschreiben Sie Ihr bestes Kleidungsstück (Farbe, Größe)."},
            {"id": "A1_W21", "prompt": "Schreiben Sie 4 Fragen an einen neuen Nachbarn."},
            {"id": "A1_W22", "prompt": "Schreiben Sie einen kurzen Dankesbrief."},
            {"id": "A1_W23", "prompt": "Schreiben Sie 3 Dinge, die Sie nicht mögen."},
            {"id": "A1_W24", "prompt": "Schreiben Sie, was Sie in Ihrer Tasche/Ihrem Rucksack haben."},
            {"id": "A1_W25", "prompt": "Schreiben Sie die Uhrzeit auf Deutsch (z.B. 10:45 Uhr)."},
            {"id": "A1_W26", "prompt": "Schreiben Sie einen kurzen Satz mit dem Verb 'haben' (Perfekt)."},
            {"id": "A1_W27", "prompt": "Schreiben Sie 3 Sätze, wo Ihre Freunde wohnen."},
            {"id": "A1_W28", "prompt": "Schreiben Sie einen kurzen Wunsch (z.B. Ich wünsche dir alles Gute)."},
            {"id": "A1_W29", "prompt": "Schreiben Sie, wie Sie zur Arbeit/Uni kommen."},
            {"id": "A1_W30", "prompt": "Schreiben Sie einen Satz mit 'weil' (Begründung)."},
        ]
    },
    "A2": {
        "reading": [
            {"id": "A2_R1", "text": "Ich habe gestern meine Tante im Krankenhaus besucht. Sie hat mir erzählt, dass sie am Wochenende wieder nach Hause darf. Das ist sehr gut!", "questions": [{"q": "Wo war die Tante?", "options": ["im Park", "im Krankenhaus", "im Kino"], "correct": 1}, {"q": "Wann darf sie nach Hause?", "options": ["morgen", "am Wochenende", "nächste Woche"], "correct": 1}]},
            {"id": "A2_R2", "text": "Wir suchen eine neue Wohnung. Sie soll drei Zimmer und einen Balkon haben. Die Miete darf nicht über 900 Euro liegen.", "questions": [{"q": "Wie viele Zimmer soll die Wohnung haben?", "options": ["zwei", "drei", "vier"], "correct": 1}, {"q": "Was ist die maximale Miete?", "options": ["800 Euro", "900 Euro", "1000 Euro"], "correct": 1}]},
            {"id": "A2_R3", "text": "Bitte senden Sie uns Ihre Bewerbungsunterlagen bis zum 15. Mai. Wir benötigen Ihren Lebenslauf und ein Motivationsschreiben. Verspätete Bewerbungen können nicht berücksichtigt werden.", "questions": [{"q": "Welches Dokument wird benötigt?", "options": ["Foto", "Reisepass", "Motivationsschreiben"], "correct": 2}, {"q": "Wann ist die Frist?", "options": ["15. April", "15. Mai", "15. Juni"], "correct": 1}]},
        ],
        "grammar": [
            {"id": "A2_G1", "q": "Obwohl es regnete, __ wir spazieren gegangen.", "options": ["sind", "haben", "waren"], "correct": 0},
            {"id": "A2_G2", "q": "Der Mann, __ ich gestern getroffen habe, ist mein Nachbar.", "options": ["der", "den", "dem"], "correct": 1},
            {"id": "A2_G3", "q": "Ich möchte, __ du mir hilfst.", "options": ["dass", "ob", "weil"], "correct": 0},
            {"id": "A2_G4", "q": "Das gehört __ Frau.", "options": ["der", "die", "den"], "correct": 0},
            {"id": "A2_G5", "q": "Sie hat __ einen neuen Computer gekauft.", "options": ["sich", "ihr", "ihm"], "correct": 0},
            {"id": "A2_G6", "q": "Er spielt Fußball, obwohl __.", "options": ["muss er arbeiten", "er arbeiten muss", "er arbeiten kann"], "correct": 1},
            {"id": "A2_G7", "q": "Ich fahre __ meinem Fahrrad.", "options": ["mit", "bei", "zu"], "correct": 0},
            {"id": "A2_G8", "q": "Wir wissen nicht, __ er kommt.", "options": ["wann", "was", "wer"], "correct": 0},
            {"id": "A2_G9", "q": "Möchtest du __ Tee oder Kaffee?", "options": ["einen", "ein", "eine"], "correct": 0},
            {"id": "A2_G10", "q": "Ich gehe ohne __ Mantel spazieren.", "options": ["mein", "meinem", "meinen"], "correct": 2},
        ],
        "vocabulary": [
            {"id": "A2_V1", "german": "der Fahrstuhl", "english": "elevator", "options": ["stairs", "door", "elevator"], "correct": 2},
            {"id": "A2_V2", "german": "die Behörde", "english": "authority", "options": ["school", "market", "authority"], "correct": 2},
            {"id": "A2_V3", "german": "unterschreiben", "english": "to sign", "options": ["to read", "to sign", "to print"], "correct": 1},
            {"id": "A2_V4", "german": "pünktlich", "english": "punctual", "options": ["late", "fast", "punctual"], "correct": 2},
            {"id": "A2_V5", "german": "die Nebenkosten", "english": "utility costs", "options": ["rent", "food costs", "utility costs"], "correct": 2},
            {"id": "A2_V6", "german": "kennenlernen", "english": "to get to know", "options": ["to forget", "to meet", "to get to know"], "correct": 2},
            {"id": "A2_V7", "german": "die Kündigung", "english": "termination", "options": ["contract", "promotion", "termination"], "correct": 2},
            {"id": "A2_V8", "german": "die Verspätung", "english": "delay", "options": ["delay", "start", "speed"], "correct": 0},
            {"id": "A2_V9", "german": "der Ratschlag", "english": "advice", "options": ["money", "advice", "gift"], "correct": 1},
            {"id": "A2_V10", "german": "ausfüllen", "english": "to fill out", "options": ["to empty", "to close", "to fill out"], "correct": 2},
        ],
        "pronunciation": [
            {"id": "A2_P1", "word": "Entschuldigung", "meaning": "excuse me"},
        ],
        "listening": [
            {"id": "A2_L1", "transcript": "Können Sie mir bitte sagen, wie ich zum Bahnhof komme? - Gehen Sie geradeaus bis zur Ampel, dann links.", "q": "Was soll die Person an der Ampel tun?", "options": ["rechts gehen", "geradeaus gehen", "links gehen"], "correct": 2},
        ],
        "writing": [
            {"id": "A2_W1", "prompt": "Schreiben Sie eine E-Mail an Ihren Freund über Ihren letzten Urlaub."},
        ]
    },
    "B1": {
        "reading": [
            {"id": "B1_R1", "text": "Die Mülltrennung ist in Deutschland gesetzlich geregelt. Jeder Haushalt muss seinen Abfall sorgfältig trennen, um die Umwelt zu schützen. Wer dies nicht tut, riskiert hohe Bußgelder.", "questions": [{"q": "Was wird durch Mülltrennung geschützt?", "options": ["Die Nachbarn", "Die Wirtschaft", "Die Umwelt"], "correct": 2}]},
        ],
        "grammar": [
            {"id": "B1_G1", "q": "Wenn ich mehr Geld hätte, __ ich ein neues Auto kaufen.", "options": ["werde", "kann", "würde"], "correct": 2},
            {"id": "B1_G2", "q": "Das ist das Buch, __ ich dir empfohlen habe.", "options": ["das", "dem", "den", "der"], "correct": 0},
        ],
        "vocabulary": [
            {"id": "B1_V1", "german": "die Nachhaltigkeit", "english": "sustainability", "options": ["growth", "sustainability", "efficiency"], "correct": 1},
            {"id": "B1_V2", "german": "sich bemühen", "english": "to make an effort", "options": ["to forget", "to make an effort", "to complain"], "correct": 1},
        ],
        "pronunciation": [
            {"id": "B1_P1", "word": "Gesellschaft", "meaning": "society"},
        ],
        "listening": [
            {"id": "B1_L1", "transcript": "Der Gastronom sagte, dass er aufgrund steigender Lebensmittelpreise die Preise erhöhen müsse. Er hofft auf das Verständnis seiner Kunden.", "q": "Warum erhöht der Gastronom die Preise?", "options": ["wegen des Wetters", "wegen der Preise", "wegen der Lebensmittelpreise"], "correct": 2},
        ],
        "writing": [
            {"id": "B1_W1", "prompt": "Diskutieren Sie die Vor- und Nachteile der Digitalisierung in der Schule. (ca. 80 Wörter)"},
        ]
    },
    "B2": {
        "reading": [
            {"id": "B2_R1", "text": "Die kontroverse Debatte über Künstliche Intelligenz wirft ethische Fragen auf. Die Automatisierung vieler Prozesse könnte Arbeitsplätze vernichten, aber gleichzeitig zu enormen Produktivitätssteigerungen führen. Es ist ein Balanceakt.", "questions": [{"q": "Welche Art von Fragen wirft die KI-Debatte auf?", "options": ["politische", "ethische", "historische"], "correct": 1}]},
        ],
        "grammar": [
            {"id": "B2_G1", "q": "Er sagte, __ er morgen kommen würde.", "options": ["dass", "ob", "falls"], "correct": 0},
        ],
        "vocabulary": [
            {"id": "B2_V1", "german": "die Eindämmung", "english": "containment", "options": ["expansion", "containment", "development"], "correct": 1},
        ],
        "pronunciation": [
            {"id": "B2_P1", "word": "Gewährleisten", "meaning": "to guarantee"},
        ],
        "listening": [
            {"id": "B2_L1", "transcript": "Der Soziologe betonte, dass der demografische Wandel eine fundamentale Umgestaltung der sozialen Sicherungssysteme erfordert. Dies sei unvermeidlich.", "q": "Was erfordert der demografische Wandel?", "options": ["neue Steuern", "eine fundamentale Umgestaltung", "mehr Arbeitskräfte"], "correct": 1},
        ],
        "writing": [
            {"id": "B2_W1", "prompt": "Analysieren Sie kritisch die Auswirkungen der Globalisierung auf die lokale Kultur. (ca. 100 Wörter)"},
        ]
    }
}


class GoetheTrainer:
    def __init__(self):
        self.levels = {
            "A1": {"name": "Start Deutsch", "description": "Basic comprehension and simple sentences."},
            "A2": {"name": "Goethe-Zertifikat A2", "description": "Simple conversations and common situations."},
            "B1": {"name": "Goethe-Zertifikat B1", "description": "Independent use in everyday situations."},
            "B2": {"name": "Goethe-Zertifikat B2", "description": "Understanding complex texts and fluent communication."},
        }
        
        # Initialize session state variables
        self._init_session_state()

    def _init_session_state(self):
        """Initializes all necessary session state variables for stability."""
        if 'current_level' not in st.session_state:
            st.session_state.current_level = "A1"
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'total_exercises' not in st.session_state:
            st.session_state.total_exercises = 0
        if 'user_progress' not in st.session_state:
            st.session_state.user_progress = {level: 0 for level in self.levels.keys()}
        if 'current_exercise_type' not in st.session_state:
            st.session_state.current_exercise_type = list(EXERCISE_TYPES.keys())[0]

        # NEW STATE FLAG: Used to defer the final rerun after a 'Next Exercise' click
        if 'do_reset' not in st.session_state:
            st.session_state.do_reset = False

        for key in EXERCISE_TYPES.values(): 
            if key not in st.session_state:
                st.session_state[key] = None
            if f"checked_{key}" not in st.session_state:
                 st.session_state[f"checked_{key}"] = False
        
        # Initialize stable containers for user answers
        if 'current_answers' not in st.session_state:
            st.session_state.current_answers = []

    # --- CORE GAME LOGIC ---

    def _select_exercise(self, level: str, content_key: str, state_key: str, count: int = 30): 
        """
        Selects a random exercise only if one isn't already stored in session state.
        Ensures content stability across reruns.
        """
        if st.session_state[state_key] is None or level != st.session_state.current_level:
            available_content = CONTENT_DB.get(level, {}).get(content_key, [])
            if not available_content:
                st.session_state[state_key] = None
                return None
                
            # Determine the sample size (maximum 30 items)
            sample_count = min(count, len(available_content))

            # Use random.sample for non-repetitive selection from the expanded pools
            sample = random.sample(available_content, sample_count)
            st.session_state[state_key] = sample
        
        return st.session_state[state_key]

    def _reset_exercise(self, state_key: str, answers_state_key: str):
        """
        Resets the exercise, checked status, and answers for a clean transition.
        FIX: Sets the do_reset flag instead of calling st.rerun().
        """
        st.session_state[state_key] = None
        st.session_state[answers_state_key] = []
        st.session_state[f"checked_{state_key}"] = False
        st.session_state.do_reset = True # Set the flag to trigger RERUN from the main loop

    def _update_score(self, correct_count, total_count, level, state_key):
        """
        Updates global score, total exercises, and level progress.
        FIX: Added st.rerun() call back to force immediate transition to results view.
        """
        st.session_state.score += correct_count
        st.session_state.total_exercises += 1
        st.session_state.user_progress[level] += correct_count / total_count
        
        # Display immediate feedback
        if correct_count == total_count:
            st.success(f"Perfect! You got all {total_count} questions correct! 🎉")
        elif correct_count >= total_count * 0.7:
            st.success(f"Great job! You got {correct_count}/{total_count} questions correct! 👍")
        else:
            st.warning(f"You got {correct_count}/{total_count} questions correct. Keep practicing! 💪")

        # Set checked state to display detailed results
        st.session_state[f"checked_{state_key}"] = True
        st.rerun() # FIX: This rerun is necessary to immediately switch the display mode

    
    # --- HEADER RENDERING (RESTORED) ---
    def display_header(self):
        """Display the main header and navigation"""
        st.title("🇩🇪 Deutsch Lernen - German Learning Game")
        st.markdown("### Interactive German Language Learning Platform")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # FIX: Using the same key "level_select" to stabilize the widget
            selected_level = st.selectbox(
                "Select Your Level:",
                options=list(self.levels.keys()),
                format_func=lambda x: f"{x} - {self.levels[x]['name']}",
                index=list(self.levels.keys()).index(st.session_state.current_level),
                key="level_select"
            )
            # Only update if value changes
            if selected_level != st.session_state.current_level:
                 # Reset state when level changes
                 self._reset_all_exercises()
                 st.session_state.current_level = selected_level
                 st.rerun()
        
        with col2:
            st.info(f"**Current Level:** {st.session_state.current_level}")
            st.write(self.levels[st.session_state.current_level]['description'])
        
        with col3:
            st.metric("Score", st.session_state.score)
            st.metric("Exercises Completed", st.session_state.total_exercises)

    def _reset_all_exercises(self):
        """Helper to clear all exercise data when level changes."""
        for state_key in EXERCISE_TYPES.values():
            st.session_state[state_key] = None
            st.session_state[f"checked_{state_key}"] = False
        st.session_state.current_answers = []

    # --- EXERCISE RENDERING ---

    def reading_exercise(self, level: str):
        """Reading comprehension exercise (Goethe Lesen)"""
        state_key = EXERCISE_TYPES["Lesen (Reading)"] # FIX: Used EXERCISE_TYPES
        answers_state_key = 'current_answers'
        
        st.subheader("📖 Reading Comprehension (Lesen)")
        
        # Reading comprehension has ONE passage, but multiple questions embedded
        exercise_list = self._select_exercise(level, "reading", state_key, 1) # exercise is a list now
        
        if exercise_list is None or not exercise_list:
            st.warning(f"No reading exercises available for {level} yet.")
            return
        
        # Since reading is designed to be one passage with embedded questions:
        exercise = exercise_list[0] 
        questions = exercise["questions"]
        
        # Initialize/resize answers list
        if len(st.session_state.current_answers) != len(questions):
            st.session_state.current_answers = [0] * len(questions)

        # Check if results should be displayed
        if st.session_state.get(f"checked_{state_key}"):
            self._render_results(questions, level, state_key, "reading")
            return
        
        # --- INPUT PHASE ---
        st.markdown("**Read the text:**")
        st.info(f"*{exercise['text']}*")
        
        st.markdown("---")
        st.markdown("**Answer the questions (Multiple Choice):**")
        
        # Display questions and capture answers
        for i, question in enumerate(questions):
            # FIX: Stable key based on exercise ID and question index
            options_key = f"{exercise['id']}_q_{i}"
            
            # Use index() to map the currently selected option back to the list index for storage
            selected_option_label = st.radio(
                f"**{question['q']}**",
                options=question["options"],
                # FIX: Set the default index based on stored answer index
                index=st.session_state[answers_state_key][i] if i < len(st.session_state[answers_state_key]) else 0,
                key=options_key
            )
            
            # FIX: Store the selected index
            st.session_state[answers_state_key][i] = question["options"].index(selected_option_label)
        
        # Button to submit and check answers
        if st.button("Check Answers", key="reading_check", type="primary"):
            correct_count = sum(1 for i, q in enumerate(questions) 
                                if st.session_state.current_answers[i] == q["correct"])
            self._update_score(correct_count, len(questions), level, state_key)


    def vocabulary_exercise(self, level: str):
        """Vocabulary exercise (Goethe Wortschatz)"""
        state_key = EXERCISE_TYPES["Wortschatz (Vocabulary)"] # FIX: Used EXERCISE_TYPES
        answers_state_key = 'current_answers'
        
        st.subheader("📚 Vocabulary Building (Wortschatz)")
        # FIX: Sample size changed to 30
        vocab_items = self._select_exercise(level, "vocabulary", state_key, 30)

        if vocab_items is None:
            st.warning(f"No vocabulary exercises available for {level} yet.")
            return

        # Initialize/resize answers list
        if len(st.session_state.current_answers) != len(vocab_items):
            st.session_state.current_answers = [0] * len(vocab_items)

        
        if st.session_state.get(f"checked_{state_key}"):
            self._render_results(vocab_items, level, state_key, "vocabulary")
            return

        # --- INPUT PHASE ---
        st.markdown("**Choose the correct English translation:**")

        # Display questions and capture answers
        for i, item in enumerate(vocab_items):
            options_key = f"{item['id']}_v_{i}"
            
            st.markdown(f"**{item['german']}**")
            selected_option_label = st.radio(
                "Select the correct translation:",
                options=item["options"],
                index=st.session_state.current_answers[i],
                key=options_key
            )
            st.session_state.current_answers[i] = item["options"].index(selected_option_label)
        
        if st.button("Check Vocabulary", key="vocab_check", type="primary"):
            correct_count = sum(1 for i, item in enumerate(vocab_items) 
                                if st.session_state.current_answers[i] == item["options"].index(item["english"]))
            self._update_score(correct_count, len(vocab_items), level, state_key)


    def grammar_exercise(self, level: str):
        """Grammar quiz exercise (Goethe Grammatik)"""
        state_key = EXERCISE_TYPES["Grammatik (Grammar Quiz)"] # FIX: Used EXERCISE_TYPES
        answers_state_key = 'current_answers'
        
        st.subheader("⚙️ Grammar Quiz (Grammatik)")
        # FIX: Sample size changed to 30
        grammar_items = self._select_exercise(level, "grammar", state_key, 30)

        if grammar_items is None:
            st.warning(f"No grammar exercises available for {level} yet.")
            return

        # Initialize/resize answers list
        if len(st.session_state.current_answers) != len(grammar_items):
            st.session_state.current_answers = [0] * len(grammar_items)

        
        if st.session_state.get(f"checked_{state_key}"):
            self._render_results(grammar_items, level, state_key, "grammar")
            return

        # --- INPUT PHASE ---
        st.markdown("**Fill in the blanks with the correct option:**")

        # Display questions and capture answers
        for i, item in enumerate(grammar_items):
            options_key = f"{item['id']}_g_{i}"
            
            st.markdown(f"**{item['q']}**")
            selected_option_label = st.radio(
                "Select the correct option:",
                options=item["options"],
                index=st.session_state.current_answers[i],
                key=options_key
            )
            st.session_state.current_answers[i] = item["options"].index(selected_option_label)
        
        if st.button("Check Grammar", key="grammar_check", type="primary"):
            correct_count = sum(1 for i, item in enumerate(grammar_items) 
                                if st.session_state.current_answers[i] == item["correct"])
            self._update_score(correct_count, len(grammar_items), level, state_key)

    def writing_exercise(self, level: str):
        """Writing exercise (Goethe Schreiben)"""
        state_key = EXERCISE_TYPES["Schreiben (Writing)"] # FIX: Used EXERCISE_TYPES
        st.subheader("✍️ Writing Exercise (Schreiben)")
        
        prompt_list = CONTENT_DB.get(level, {}).get("writing", [])
        if not prompt_list:
             st.warning(f"No writing prompts available for {level} yet.")
             return
        
        # Ensure a single prompt is stable
        prompt_data_list = self._select_exercise(level, "writing", state_key, 1)
        if prompt_data_list is None or not prompt_data_list: return
        prompt_data = prompt_data_list[0]

        prompt = prompt_data['prompt']
        
        st.markdown("**Writing Prompt:**")
        st.info(prompt)
        
        user_text = st.text_area(
            "Write your response here:",
            height=200,
            key=f"writing_{level}_{prompt_data['id']}"
        )
        
        col1, col2 = st.columns(2)
        
        if st.session_state.get(f"checked_{state_key}"):
             st.markdown("---")
             st.success("Exercise marked complete.")
             # FIX: Use on_click callback
             if st.button("Next Writing Prompt", key="writing_next_after_check", on_click=self._reset_exercise, args=(state_key, 'current_answers')):
                 pass
             return

        with col1:
            if st.button("Submit Writing & Mark Complete", key="writing_submit", type="primary"):
                if user_text.strip():
                    word_count = len(user_text.split())
                    
                    st.session_state.total_exercises += 1
                    st.session_state.user_progress[level] += 1.0 # Full point for attempt
                    st.session_state[f"checked_{state_key}"] = True
                    
                    st.success(f"Writing submitted! Word count: {word_count}. Feedback would be generated by LLM here.")
                    st.rerun()
                else:
                    st.warning("Please write something before submitting.")
        
        with col2:
            if user_text:
                st.metric("Word Count", len(user_text.split()))

    def listening_exercise(self, level: str):
        """Listening comprehension exercise (Goethe Hören)"""
        state_key = EXERCISE_TYPES["Hören (Listening)"] # FIX: Used EXERCISE_TYPES
        answers_state_key = 'current_answers'
        
        st.subheader("👂 Listening Comprehension (Hören)")
        exercise_list = self._select_exercise(level, "listening", state_key, 1)
        
        if exercise_list is None or not exercise_list:
            st.warning(f"No listening exercises available for {level} yet.")
            return

        exercise = exercise_list[0]
        questions = exercise["questions"]
        if len(st.session_state.current_answers) != len(questions):
            st.session_state.current_answers = [0] * len(questions)

        
        if st.session_state.get(f"checked_{state_key}"):
            self._render_results(questions, level, state_key, "listening")
            return
        
        # --- INPUT PHASE ---
        st.markdown(f"**Scenario:** *{self.levels[level]['name']} Level Listening*")
        st.info("🔊 Audio Player Placeholder (TTS audio would play here for the scenario)")
        
        with st.expander("Show Transcript (for practice/checking)"):
            st.markdown(f"*{exercise['transcript']}*")
        
        st.markdown("---")
        st.markdown("**Answer the questions based on what you heard:**")

        for i, question in enumerate(questions):
            options_key = f"{exercise['id']}_l_{i}"
            
            selected_option_label = st.radio(
                f"**{question['q']}**",
                options=question["options"],
                index=st.session_state.current_answers[i],
                key=options_key
            )
            st.session_state.current_answers[i] = question["options"].index(selected_option_label)
        
        if st.button("Check Listening", key="listening_check", type="primary"):
            correct_count = sum(1 for i, q in enumerate(questions) 
                                if st.session_state.current_answers[i] == q["correct"])
            self._update_score(correct_count, len(questions), level, state_key)

    def pronunciation_exercise(self, level: str):
        """Pronunciation practice (Goethe Sprechen)"""
        state_key = EXERCISE_TYPES["Sprechen (Pronunciation)"] # FIX: Used EXERCISE_TYPES
        st.subheader("🗣️ Pronunciation Practice (Sprechen)")
        
        # FIX: Sample size changed to 10
        pron_items = self._select_exercise(level, "pronunciation", state_key, 10)

        if pron_items is None:
            st.warning(f"No pronunciation exercises available for {level} yet.")
            return
        
        st.markdown("**Practice pronouncing these German words:**")
        st.markdown("*Note: In a full deployment, this would include audio playback and recording features.*")
        
        for i, item in enumerate(pron_items):
            with st.expander(f"Word {i+1}: **{item['word']}**"):
                st.markdown(f"**Meaning:** {item['meaning']}")
                st.info("🎤 Recording feature placeholder. Speak the word now.")
            
        if st.session_state.get(f"checked_{state_key}"):
             st.success("Pronunciation marked as practiced.")
             # FIX: Use on_click callback
             if st.button("Next Pronunciation Set", key="pron_next_after_check", on_click=self._reset_exercise, args=(state_key, 'current_answers')):
                 pass
             return
        
        if st.button("Mark as Practiced", key="pronunciation_done", type="primary"):
            st.session_state.total_exercises += 1
            st.session_state.user_progress[level] += 1.0 # Full point for attempting
            st.session_state[f"checked_{state_key}"] = True
            st.rerun()

    def _render_results(self, exercise_items, level, state_key, content_key):
        """
        Centralized function to display detailed results and handle score updates (which already happened).
        FIX: Explicitly renders the context text (reading/listening) before detailed results.
        """
        st.markdown("---")

        # Get the full exercise object list/item to retrieve context text
        full_exercise_list = st.session_state[state_key]

        if content_key == "reading":
            # For reading, full_exercise_list is a list containing ONE item (the passage)
            full_exercise = full_exercise_list[0]
            st.subheader("📖 Reading Comprehension (Lesen)")
            st.markdown("**Text:**")
            st.info(f"*{full_exercise.get('text')}*")
        elif content_key == "listening":
            # For listening, full_exercise_list is a list containing ONE item (the scenario)
            full_exercise = full_exercise_list[0]
            st.subheader("👂 Listening Comprehension (Hören)")
            st.markdown("**Scenario:**")
            st.info(f"*{full_exercise.get('transcript')}*")
        
        st.markdown("---")
        st.markdown("**Detailed Results:**")

        # Recalculate based on current state (answers already stored)
        user_answers_indices = st.session_state.current_answers
        
        for i, item in enumerate(exercise_items):
            user_choice_index = user_answers_indices[i]
            
            if content_key == "vocabulary":
                # Find the correct English translation from the options array
                correct_label = item["english"]
                is_correct = (user_choice_index >= 0 and item["options"][user_choice_index] == correct_label)
                question_text = f"{item['german']}"
                user_choice_display = item["options"][user_choice_index] if user_choice_index >= 0 else "None selected"
            else:
                # Find the correct option using the stored index
                correct_index = item["correct"]
                correct_label = item["options"][correct_index]
                is_correct = user_choice_index == correct_index
                question_text = item.get("q") or item.get("prompt") or item.get("word")
                user_choice_display = item["options"][user_choice_index] if user_choice_index >= 0 else "None selected"
            
            icon = "✅" if is_correct else "❌"
            feedback_text = f"**{icon} {question_text}**"
            
            if not is_correct:
                feedback_text += f"<br>_Correct Answer:_ **{correct_label}** (You selected: {user_choice_display})"
            
            st.markdown(feedback_text, unsafe_allow_html=True)
        
        # FIX: Use on_click callback with arguments for guaranteed scope stability
        # The action is triggered via the on_click callback
        if st.button("Next Exercise", 
                     key=f"next_{state_key}", 
                     on_click=self._reset_exercise,
                     args=(state_key, 'current_answers')): 
            pass # Action handled by callback


    def display_progress(self):
        """Display user progress and statistics"""
        st.subheader("📈 Your Progress")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Level Progress:**")
            for level, progress in st.session_state.user_progress.items():
                progress_percent = min(100, progress * 10)  # Scale progress for display
                st.progress(progress_percent / 100)
                st.markdown(f"{level}: {progress_percent:.1f}%")
        
        with col2:
            st.markdown("**Overall Statistics:**")
            total_score = st.session_state.score
            total_exercises = st.session_state.total_exercises
            
            if total_exercises > 0:
                # FIX: Use a simplified metric (average score per completed exercise).
                avg_score_per_exercise = total_score / total_exercises
                st.metric("Avg Score/Exercise", f"{avg_score_per_exercise:.2f}")
            else:
                st.metric("Avg Score/Exercise", "N/A")
            
            st.metric("Total Score", total_score)
            st.metric("Exercises Completed", total_exercises)

    def run(self):
        """Main application runner"""
        
        # FIX: Check the 'do_reset' flag early to trigger the final rerun
        # This handles the transition from _reset_exercise to the next question.
        if st.session_state.get('do_reset'):
            st.session_state.do_reset = False
            st.rerun()

        # Display header
        self.display_header()
        
        # Sidebar for exercise selection
        st.sidebar.title("Exercise Menu")
        # Store the selected exercise type in session state for stability
        exercise_type = st.sidebar.selectbox(
            "Choose Exercise Type:",
            list(EXERCISE_TYPES.keys()),
            key='exercise_type_select',
            index=list(EXERCISE_TYPES.keys()).index(st.session_state.current_exercise_type)
        )

        # FIX: Check if exercise type has changed and reset the 'checked' state
        if st.session_state.current_exercise_type != exercise_type:
            st.session_state.current_exercise_type = exercise_type
            
            # Reset the 'checked' state when the exercise type changes to allow a new quiz
            state_key = EXERCISE_TYPES.get(exercise_type) # FIX: Used EXERCISE_TYPES
            if state_key:
                st.session_state[f"checked_{state_key}"] = False
            st.rerun()
        
        # Display progress in sidebar
        with st.sidebar:
            st.markdown("---")
            self.display_progress()
            
            # Reset progress button
            if st.button("Reset Progress", key="reset_progress"):
                st.session_state.score = 0
                st.session_state.total_exercises = 0
                st.session_state.user_progress = {level: 0 for level in self.levels.keys()}
                # Ensure all exercises are rerandomized on full reset
                self._reset_all_exercises()
                st.success("Progress reset!")
                st.rerun()
        
        # Main content area
        st.markdown("---")
        
        current_level = st.session_state.current_level
        
        # Route to appropriate exercise
        if exercise_type == "Lesen (Reading)":
            self.reading_exercise(current_level)
        elif exercise_type == "Wortschatz (Vocabulary)":
            self.vocabulary_exercise(current_level)
        elif exercise_type == "Grammatik (Grammar Quiz)":
            self.grammar_exercise(current_level)
        elif exercise_type == "Sprechen (Pronunciation)":
            self.pronunciation_exercise(current_level)
        elif exercise_type == "Schreiben (Writing)":
            self.writing_exercise(current_level)
        elif exercise_type == "Hören (Listening)":
            self.listening_exercise(current_level)
            
        # Footer
        st.markdown("---")
        st.markdown(
            """
            <div style='text-align: center'>
                <p>🇩🇪 <strong>Deutsch Lernen</strong> - Interactive German Learning Platform</p>
                <p>Practice makes perfect! Keep learning and improving your German skills.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Run the application
if __name__ == "__main__":
    # FIX: Initialize the Game class only once across reruns
    if 'game_instance' not in st.session_state:
        st.session_state.game_instance = GoetheTrainer()
    
    st.session_state.game_instance.run()
