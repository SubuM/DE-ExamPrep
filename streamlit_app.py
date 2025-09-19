import streamlit as st
import random
import time
from datetime import datetime
import base64
import io
import json
from typing import Dict, List, Tuple
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="Deutsch Lernen - German Learning Game",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

class GermanLearningGame:
    def __init__(self):
        self.levels = {
            "A1": {"name": "Beginner", "description": "Basic user - Breakthrough or beginner"},
            "A2": {"name": "Elementary", "description": "Basic user - Waystage or elementary"},
            "B1": {"name": "Intermediate", "description": "Independent user - Threshold or intermediate"},
            "B2": {"name": "Upper Intermediate", "description": "Independent user - Vantage or upper intermediate"}
        }
        
        self.exercise_types = [
            "Reading Comprehension",
            "Listening Comprehension", 
            "Writing Exercise",
            "Pronunciation Practice",
            "Grammar Quiz",
            "Vocabulary Building"
        ]
        
        # Sample content database
        self.content = self._initialize_content()
        
        # Initialize session state
        if 'current_level' not in st.session_state:
            st.session_state.current_level = "A1"
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'total_exercises' not in st.session_state:
            st.session_state.total_exercises = 0
        if 'user_progress' not in st.session_state:
            st.session_state.user_progress = {level: 0 for level in self.levels.keys()}

    def _initialize_content(self) -> Dict:
        """Initialize the content database with exercises for each level"""
        return {
            "A1": {
                "reading": [
                    {
                        "text": "Hallo! Ich heiße Maria. Ich komme aus Deutschland. Ich bin 25 Jahre alt und ich wohne in Berlin. Ich arbeite als Lehrerin in einer Schule.",
                        "questions": [
                            {"q": "Wie heißt die Person?", "options": ["Maria", "Anna", "Lisa", "Emma"], "correct": 0},
                            {"q": "Wo wohnt Maria?", "options": ["München", "Hamburg", "Berlin", "Köln"], "correct": 2},
                            {"q": "Was ist Marias Beruf?", "options": ["Ärztin", "Lehrerin", "Studentin", "Verkäuferin"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"german": "das Haus", "english": "house", "options": ["car", "house", "tree", "book"]},
                    {"german": "die Katze", "english": "cat", "options": ["dog", "cat", "bird", "fish"]},
                    {"german": "essen", "english": "to eat", "options": ["to sleep", "to eat", "to run", "to write"]}
                ],
                "grammar": [
                    {"question": "Ich __ aus Deutschland.", "options": ["komme", "kommst", "kommt", "kommen"], "correct": 0},
                    {"question": "Das ist __ Buch.", "options": ["eine", "ein", "einer", "eines"], "correct": 1}
                ],
                "pronunciation": [
                    {"word": "Guten Tag", "ipa": "/ˈɡuːtən taːk/", "meaning": "Good day"},
                    {"word": "Danke schön", "ipa": "/ˈdaŋkə ʃøːn/", "meaning": "Thank you very much"},
                    {"word": "Entschuldigung", "ipa": "/ɛntˈʃʊldɪɡʊŋ/", "meaning": "Excuse me/Sorry"}
                ]
            },
            "A2": {
                "reading": [
                    {
                        "text": "Letzten Samstag war ich mit meiner Familie im Park. Das Wetter war sehr schön und warm. Wir haben ein Picknick gemacht und Fußball gespielt. Meine Schwester hat ein Buch gelesen, während mein Bruder mit dem Hund gespielt hat.",
                        "questions": [
                            {"q": "Wann war die Familie im Park?", "options": ["Sonntag", "Samstag", "Freitag", "Montag"], "correct": 1},
                            {"q": "Wie war das Wetter?", "options": ["schlecht", "kalt", "regnerisch", "schön und warm"], "correct": 3},
                            {"q": "Was hat die Schwester gemacht?", "options": ["Fußball gespielt", "ein Buch gelesen", "mit dem Hund gespielt", "gekocht"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"german": "der Urlaub", "english": "vacation", "options": ["work", "vacation", "school", "hospital"]},
                    {"german": "einkaufen", "english": "to shop", "options": ["to shop", "to cook", "to clean", "to study"]},
                    {"german": "das Wetter", "english": "weather", "options": ["time", "weather", "money", "food"]}
                ],
                "grammar": [
                    {"question": "Gestern __ ich ins Kino gegangen.", "options": ["bin", "habe", "war", "hatte"], "correct": 0},
                    {"question": "Der Mann, __ ich gestern getroffen habe, ist mein Nachbar.", "options": ["der", "den", "dem", "dessen"], "correct": 1}
                ]
            },
            "B1": {
                "reading": [
                    {
                        "text": "Die Digitalisierung verändert unsere Arbeitswelt grundlegend. Viele traditionelle Berufe verschwinden, während neue entstehen. Es ist wichtig, dass wir uns kontinuierlich weiterbilden, um mit diesen Veränderungen Schritt zu halten. Unternehmen müssen ihre Mitarbeiter dabei unterstützen, neue Fähigkeiten zu erlernen.",
                        "questions": [
                            {"q": "Was verändert die Arbeitswelt?", "options": ["Die Digitalisierung", "Die Globalisierung", "Die Politik", "Das Klima"], "correct": 0},
                            {"q": "Was ist wichtig für Arbeitnehmer?", "options": ["Mehr Geld verdienen", "Früher in Rente gehen", "Sich weiterbilden", "Weniger arbeiten"], "correct": 2},
                            {"q": "Wer soll Mitarbeiter unterstützen?", "options": ["Die Regierung", "Die Unternehmen", "Die Familie", "Die Freunde"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"german": "die Herausforderung", "english": "challenge", "options": ["opportunity", "challenge", "problem", "solution"]},
                    {"german": "nachhaltig", "english": "sustainable", "options": ["expensive", "sustainable", "temporary", "difficult"]},
                    {"german": "sich entwickeln", "english": "to develop", "options": ["to develop", "to destroy", "to ignore", "to avoid"]}
                ],
                "grammar": [
                    {"question": "Wenn ich mehr Zeit hätte, __ ich mehr reisen.", "options": ["werde", "würde", "will", "wollte"], "correct": 1},
                    {"question": "Das ist das Buch, __ ich dir empfohlen habe.", "options": ["das", "dem", "den", "der"], "correct": 0}
                ]
            },
            "B2": {
                "reading": [
                    {
                        "text": "Die Klimakrise stellt eine der größten Herausforderungen unserer Zeit dar. Wissenschaftler warnen eindringlich vor den Folgen des Klimawandels. Es bedarf einer koordinierten internationalen Anstrengung, um die Erderwärmung zu begrenzen. Sowohl politische Maßnahmen als auch individuelles Handeln sind erforderlich, um eine nachhaltige Zukunft zu gewährleisten.",
                        "questions": [
                            {"q": "Was stellt die Klimakrise dar?", "options": ["Ein kleines Problem", "Eine der größten Herausforderungen", "Eine Chance", "Ein Mythos"], "correct": 1},
                            {"q": "Was ist erforderlich?", "options": ["Nur politische Maßnahmen", "Nur individuelles Handeln", "Beides", "Nichts"], "correct": 2},
                            {"q": "Wovor warnen Wissenschaftler?", "options": ["Vor Naturkatastrophen", "Vor den Folgen des Klimawandels", "Vor Wirtschaftskrisen", "Vor Kriegen"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"german": "die Nachhaltigkeit", "english": "sustainability", "options": ["sustainability", "profitability", "popularity", "availability"]},
                    {"german": "bewältigen", "english": "to cope with", "options": ["to avoid", "to cope with", "to create", "to ignore"]},
                    {"german": "die Auswirkung", "english": "impact", "options": ["cause", "impact", "beginning", "end"]}
                ],
                "grammar": [
                    {"question": "Obwohl es regnete, __ wir spazieren gegangen.", "options": ["sind", "haben", "waren", "hatten"], "correct": 0},
                    {"question": "Der Vorschlag, __ du gemacht hast, ist sehr interessant.", "options": ["der", "den", "dem", "dessen"], "correct": 1}
                ]
            }
        }

    def display_header(self):
        """Display the main header and navigation"""
        st.title("🇩🇪 Deutsch Lernen - German Learning Game")
        st.markdown("### Interactive German Language Learning Platform")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            selected_level = st.selectbox(
                "Select Your Level:",
                options=list(self.levels.keys()),
                format_func=lambda x: f"{x} - {self.levels[x]['name']}",
                index=list(self.levels.keys()).index(st.session_state.current_level)
            )
            st.session_state.current_level = selected_level
        
        with col2:
            st.info(f"**Current Level:** {selected_level}")
            st.write(self.levels[selected_level]['description'])
        
        with col3:
            st.metric("Score", st.session_state.score)
            st.metric("Exercises Completed", st.session_state.total_exercises)

    def reading_comprehension_exercise(self, level: str):
        """Reading comprehension exercise"""
        st.subheader("📖 Reading Comprehension")
        
        if level not in self.content or not self.content[level].get("reading"):
            st.warning("No reading exercises available for this level yet.")
            return
        
        exercise = random.choice(self.content[level]["reading"])
        
        st.markdown("**Read the following text carefully:**")
        st.markdown(f"*{exercise['text']}*")
        
        st.markdown("---")
        st.markdown("**Answer the questions:**")
        
        user_answers = []
        for i, question in enumerate(exercise["questions"]):
            answer = st.radio(
                question["q"],
                options=question["options"],
                key=f"reading_q_{i}_{time.time()}"
            )
            user_answers.append(question["options"].index(answer))
        
        if st.button("Check Answers", key="reading_check"):
            correct = sum(1 for i, q in enumerate(exercise["questions"]) 
                         if user_answers[i] == q["correct"])
            total = len(exercise["questions"])
            
            st.session_state.score += correct
            st.session_state.total_exercises += 1
            st.session_state.user_progress[level] += correct / total
            
            if correct == total:
                st.success(f"Perfect! You got all {total} questions correct! 🎉")
            elif correct >= total * 0.7:
                st.success(f"Great job! You got {correct}/{total} questions correct! 👍")
            else:
                st.warning(f"You got {correct}/{total} questions correct. Keep practicing! 💪")

    def vocabulary_exercise(self, level: str):
        """Vocabulary building exercise"""
        st.subheader("📚 Vocabulary Building")
        
        if level not in self.content or not self.content[level].get("vocabulary"):
            st.warning("No vocabulary exercises available for this level yet.")
            return
        
        vocab_items = random.sample(self.content[level]["vocabulary"], 
                                   min(3, len(self.content[level]["vocabulary"])))
        
        st.markdown("**Choose the correct English translation:**")
        
        user_answers = []
        for i, item in enumerate(vocab_items):
            st.markdown(f"**{item['german']}**")
            answer = st.radio(
                "Select the correct translation:",
                options=item["options"],
                key=f"vocab_{i}_{time.time()}"
            )
            user_answers.append(item["options"].index(answer))
        
        if st.button("Check Vocabulary", key="vocab_check"):
            correct = sum(1 for i, item in enumerate(vocab_items) 
                         if user_answers[i] == item["options"].index(item["english"]))
            total = len(vocab_items)
            
            st.session_state.score += correct
            st.session_state.total_exercises += 1
            st.session_state.user_progress[level] += correct / total
            
            for i, item in enumerate(vocab_items):
                correct_idx = item["options"].index(item["english"])
                if user_answers[i] == correct_idx:
                    st.success(f"✅ {item['german']} = {item['english']}")
                else:
                    st.error(f"❌ {item['german']} = {item['english']} (You selected: {item['options'][user_answers[i]]})")

    def grammar_exercise(self, level: str):
        """Grammar quiz exercise"""
        st.subheader("⚙️ Grammar Quiz")
        
        if level not in self.content or not self.content[level].get("grammar"):
            st.warning("No grammar exercises available for this level yet.")
            return
        
        grammar_items = random.sample(self.content[level]["grammar"], 
                                     min(3, len(self.content[level]["grammar"])))
        
        st.markdown("**Fill in the blanks with the correct option:**")
        
        user_answers = []
        for i, item in enumerate(grammar_items):
            st.markdown(f"**{item['question']}**")
            answer = st.radio(
                "Select the correct option:",
                options=item["options"],
                key=f"grammar_{i}_{time.time()}"
            )
            user_answers.append(item["options"].index(answer))
        
        if st.button("Check Grammar", key="grammar_check"):
            correct = sum(1 for i, item in enumerate(grammar_items) 
                         if user_answers[i] == item["correct"])
            total = len(grammar_items)
            
            st.session_state.score += correct
            st.session_state.total_exercises += 1
            st.session_state.user_progress[level] += correct / total
            
            for i, item in enumerate(grammar_items):
                if user_answers[i] == item["correct"]:
                    st.success(f"✅ {item['question'].replace('__', item['options'][item['correct']])}")
                else:
                    st.error(f"❌ Correct: {item['question'].replace('__', item['options'][item['correct']])} (You selected: {item['options'][user_answers[i]]})")

    def pronunciation_exercise(self, level: str):
        """Pronunciation practice exercise"""
        st.subheader("🗣️ Pronunciation Practice")
        
        if level not in self.content or not self.content[level].get("pronunciation"):
            st.warning("No pronunciation exercises available for this level yet.")
            return
        
        pron_items = random.sample(self.content[level]["pronunciation"], 
                                  min(3, len(self.content[level]["pronunciation"])))
        
        st.markdown("**Practice pronouncing these German words:**")
        st.markdown("*Note: In a full deployment, this would include audio playback and recording features.*")
        
        for i, item in enumerate(pron_items):
            with st.expander(f"Word {i+1}: {item['word']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**German:** {item['word']}")
                    st.markdown(f"**IPA:** {item['ipa']}")
                    st.markdown(f"**Meaning:** {item['meaning']}")
                
                with col2:
                    st.markdown("**Practice Tips:**")
                    st.markdown("• Listen to the pronunciation")
                    st.markdown("• Repeat several times")
                    st.markdown("• Record yourself speaking")
                    
                # Placeholder for audio features
                st.info("🔊 Audio playback would be available here")
                st.info("🎤 Voice recording feature would be available here")
        
        if st.button("Mark as Practiced", key="pronunciation_done"):
            st.session_state.total_exercises += 1
            st.session_state.user_progress[level] += 0.5
            st.success("Great job practicing pronunciation! Keep it up! 🎯")

    def writing_exercise(self, level: str):
        """Writing exercise"""
        st.subheader("✍️ Writing Exercise")
        
        writing_prompts = {
            "A1": [
                "Write 3-4 sentences about yourself (name, age, where you live, what you do).",
                "Describe your family in simple sentences.",
                "Write about your daily routine using present tense."
            ],
            "A2": [
                "Write about your last weekend. What did you do? (Past tense practice)",
                "Describe your hometown. What do you like about it?",
                "Write about your hobbies and free time activities."
            ],
            "B1": [
                "Write your opinion about online learning vs. traditional classroom learning.",
                "Describe a problem in your city and suggest solutions.",
                "Write about your future plans and goals."
            ],
            "B2": [
                "Discuss the advantages and disadvantages of social media in modern society.",
                "Write about environmental challenges and how individuals can contribute to solutions.",
                "Analyze the impact of technology on interpersonal relationships."
            ]
        }
        
        prompt = random.choice(writing_prompts.get(level, writing_prompts["A1"]))
        
        st.markdown("**Writing Prompt:**")
        st.info(prompt)
        
        user_text = st.text_area(
            "Write your response here:",
            height=200,
            key=f"writing_{level}_{time.time()}"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Submit Writing", key="writing_submit"):
                if user_text.strip():
                    word_count = len(user_text.split())
                    st.session_state.total_exercises += 1
                    st.session_state.user_progress[level] += 0.5
                    
                    st.success(f"Writing submitted! Word count: {word_count}")
                    st.info("In a full version, this would include grammar checking and feedback.")
                else:
                    st.warning("Please write something before submitting.")
        
        with col2:
            if user_text:
                word_count = len(user_text.split())
                char_count = len(user_text)
                st.metric("Word Count", word_count)
                st.metric("Character Count", char_count)

    def listening_exercise(self, level: str):
        """Listening comprehension exercise"""
        st.subheader("👂 Listening Comprehension")
        
        listening_scenarios = {
            "A1": [
                {
                    "scenario": "A person introducing themselves",
                    "transcript": "Hallo, ich heiße Thomas. Ich bin 30 Jahre alt und komme aus München. Ich arbeite als Ingenieur.",
                    "questions": [
                        {"q": "Wie heißt die Person?", "options": ["Thomas", "Michael", "Andreas", "Stefan"], "correct": 0},
                        {"q": "Wie alt ist Thomas?", "options": ["25", "30", "35", "40"], "correct": 1}
                    ]
                }
            ],
            "A2": [
                {
                    "scenario": "Conversation about weekend plans",
                    "transcript": "Was machst du am Wochenende? - Ich gehe ins Kino mit meiner Freundin. Und du? - Ich besuche meine Eltern in Hamburg.",
                    "questions": [
                        {"q": "Was macht die erste Person am Wochenende?", "options": ["Sport", "Kino", "Einkaufen", "Kochen"], "correct": 1},
                        {"q": "Wo wohnen die Eltern?", "options": ["Berlin", "München", "Hamburg", "Köln"], "correct": 2}
                    ]
                }
            ],
            "B1": [
                {
                    "scenario": "News report about environmental issues",
                    "transcript": "Experten warnen vor den Folgen des Klimawandels. Die Temperaturen steigen weltweit an. Es ist wichtig, jetzt zu handeln.",
                    "questions": [
                        {"q": "Wovor warnen Experten?", "options": ["Wirtschaftskrise", "Klimawandel", "Arbeitslosigkeit", "Krankheiten"], "correct": 1},
                        {"q": "Was steigt weltweit an?", "options": ["Preise", "Temperaturen", "Arbeitslosigkeit", "Kriminalität"], "correct": 1}
                    ]
                }
            ],
            "B2": [
                {
                    "scenario": "Academic discussion about digitalization",
                    "transcript": "Die Digitalisierung beeinflusst alle Lebensbereiche. Während sie viele Vorteile bietet, entstehen auch neue Herausforderungen für die Gesellschaft.",
                    "questions": [
                        {"q": "Was beeinflusst alle Lebensbereiche?", "options": ["Globalisierung", "Digitalisierung", "Urbanisierung", "Klimawandel"], "correct": 1},
                        {"q": "Was entstehen neben Vorteilen?", "options": ["Probleme", "Herausforderungen", "Kosten", "Risiken"], "correct": 1}
                    ]
                }
            ]
        }
        
        if level not in listening_scenarios:
            st.warning("No listening exercises available for this level yet.")
            return
        
        exercise = random.choice(listening_scenarios[level])
        
        st.markdown(f"**Scenario:** {exercise['scenario']}")
        
        # Placeholder for audio player
        st.info("🔊 Audio player would be here. Click to listen to the German audio.")
        
        with st.expander("Show transcript (for demo purposes)"):
            st.markdown(f"*{exercise['transcript']}*")
        
        st.markdown("**Answer the questions based on what you heard:**")
        
        user_answers = []
        for i, question in enumerate(exercise["questions"]):
            answer = st.radio(
                question["q"],
                options=question["options"],
                key=f"listening_q_{i}_{time.time()}"
            )
            user_answers.append(question["options"].index(answer))
        
        if st.button("Check Listening", key="listening_check"):
            correct = sum(1 for i, q in enumerate(exercise["questions"]) 
                         if user_answers[i] == q["correct"])
            total = len(exercise["questions"])
            
            st.session_state.score += correct
            st.session_state.total_exercises += 1
            st.session_state.user_progress[level] += correct / total
            
            if correct == total:
                st.success(f"Perfect listening skills! You got all {total} questions correct! 🎉")
            elif correct >= total * 0.7:
                st.success(f"Good listening! You got {correct}/{total} questions correct! 👍")
            else:
                st.warning(f"You got {correct}/{total} questions correct. Try listening again! 👂")

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
                accuracy = (total_score / (total_exercises * 3)) * 100  # Assuming avg 3 questions per exercise
                st.metric("Accuracy", f"{accuracy:.1f}%")
            else:
                st.metric("Accuracy", "N/A")
            
            st.metric("Total Score", total_score)
            st.metric("Exercises Completed", total_exercises)

    def run(self):
        """Main application runner"""
        # Initialize session state if needed
        if 'initialized' not in st.session_state:
            st.session_state.initialized = True
        
        # Display header
        self.display_header()
        
        # Sidebar for exercise selection
        st.sidebar.title("Exercise Menu")
        exercise_type = st.sidebar.selectbox(
            "Choose Exercise Type:",
            self.exercise_types
        )
        
        # Display progress in sidebar
        with st.sidebar:
            st.markdown("---")
            self.display_progress()
            
            # Reset progress button
            if st.button("Reset Progress", key="reset_progress"):
                st.session_state.score = 0
                st.session_state.total_exercises = 0
                st.session_state.user_progress = {level: 0 for level in self.levels.keys()}
                st.success("Progress reset!")
                st.rerun()
        
        # Main content area
        st.markdown("---")
        
        current_level = st.session_state.current_level
        
        # Route to appropriate exercise
        if exercise_type == "Reading Comprehension":
            self.reading_comprehension_exercise(current_level)
        elif exercise_type == "Vocabulary Building":
            self.vocabulary_exercise(current_level)
        elif exercise_type == "Grammar Quiz":
            self.grammar_exercise(current_level)
        elif exercise_type == "Pronunciation Practice":
            self.pronunciation_exercise(current_level)
        elif exercise_type == "Writing Exercise":
            self.writing_exercise(current_level)
        elif exercise_type == "Listening Comprehension":
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
    app = GermanLearningGame()
    app.run()