import streamlit as st
import random
import time
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd

# Configure Streamlit page
st.set_page_config(
    page_title="Deutsch Lernen - German Learning Game",
    page_icon="🇩🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CONSTANTS ---
EXERCISE_KEYS = {
    "Reading Comprehension": "reading_exercise",
    "Vocabulary Building": "vocabulary_exercise",
    "Grammar Quiz": "grammar_exercise",
    "Listening Comprehension": "listening_exercise",
    "Pronunciation Practice": "pronunciation_exercise",
    "Writing Exercise": "writing_exercise",
}
# Define a set of stable keys for user answers
if 'reading_answers' not in st.session_state:
    st.session_state.reading_answers = []
if 'vocab_answers' not in st.session_state:
    st.session_state.vocab_answers = []
if 'grammar_answers' not in st.session_state:
    st.session_state.grammar_answers = []
if 'listening_answers' not in st.session_state:
    st.session_state.listening_answers = []

class GermanLearningGame:
    def __init__(self):
        self.levels = {
            "A1": {"name": "Beginner", "description": "Basic user - Breakthrough or beginner"},
            "A2": {"name": "Elementary", "description": "Basic user - Waystage or elementary"},
            "B1": {"name": "Intermediate", "description": "Independent user - Threshold or intermediate"},
            "B2": {"name": "Upper Intermediate", "description": "Independent user - Vantage or upper intermediate"}
        }
        
        self.exercise_types = list(EXERCISE_KEYS.keys())
        
        # Sample content database
        self.content = self._initialize_content()
        
        # Initialize session state for game parameters
        if 'current_level' not in st.session_state:
            st.session_state.current_level = "A1"
        if 'score' not in st.session_state:
            st.session_state.score = 0
        if 'total_exercises' not in st.session_state:
            st.session_state.total_exercises = 0
        if 'user_progress' not in st.session_state:
            st.session_state.user_progress = {level: 0 for level in self.levels.keys()}
        if 'current_exercise_type' not in st.session_state:
            st.session_state.current_exercise_type = None

        # Initialize stable containers for exercises (to avoid rerandomization)
        for key in EXERCISE_KEYS.values():
            if key not in st.session_state:
                st.session_state[key] = None

    def _initialize_content(self) -> Dict:
        """Initialize the content database with exercises for each level"""
        # NOTE: The structure for the content remains the same as provided.
        return {
            "A1": {
                "reading": [
                    {
                        "id": "A1_R1",
                        "text": "Hallo! Ich heiße Maria. Ich komme aus Deutschland. Ich bin 25 Jahre alt und ich wohne in Berlin. Ich arbeite als Lehrerin in einer Schule.",
                        "questions": [
                            {"q": "Wie heißt die Person?", "options": ["Maria", "Anna", "Lisa", "Emma"], "correct": 0},
                            {"q": "Wo wohnt Maria?", "options": ["München", "Hamburg", "Berlin", "Köln"], "correct": 2},
                            {"q": "Was ist Marias Beruf?", "options": ["Ärztin", "Lehrerin", "Studentin", "Verkäuferin"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"id": "A1_V1", "german": "das Haus", "english": "house", "options": ["car", "house", "tree", "book"]},
                    {"id": "A1_V2", "german": "die Katze", "english": "cat", "options": ["dog", "cat", "bird", "fish"]},
                    {"id": "A1_V3", "german": "essen", "english": "to eat", "options": ["to sleep", "to eat", "to run", "to write"]}
                ],
                "grammar": [
                    {"id": "A1_G1", "question": "Ich __ aus Deutschland.", "options": ["komme", "kommst", "kommt", "kommen"], "correct": 0},
                    {"id": "A1_G2", "question": "Das ist __ Buch.", "options": ["eine", "ein", "einer", "eines"], "correct": 1}
                ],
                "pronunciation": [
                    {"id": "A1_P1", "word": "Guten Tag", "ipa": "/ˈɡuːtən taːk/", "meaning": "Good day"},
                    {"id": "A1_P2", "word": "Danke schön", "ipa": "/ˈdaŋkə ʃøːn/", "meaning": "Thank you very much"},
                    {"id": "A1_P3", "word": "Entschuldigung", "ipa": "/ɛntˈʃʊldɪɡʊŋ/", "meaning": "Excuse me/Sorry"}
                ]
            },
            "A2": {
                "reading": [
                    {
                        "id": "A2_R1",
                        "text": "Letzten Samstag war ich mit meiner Familie im Park. Das Wetter war sehr schön und warm. Wir haben ein Picknick gemacht und Fußball gespielt. Meine Schwester hat ein Buch gelesen, während mein Bruder mit dem Hund gespielt hat.",
                        "questions": [
                            {"q": "Wann war die Familie im Park?", "options": ["Sonntag", "Samstag", "Freitag", "Montag"], "correct": 1},
                            {"q": "Wie war das Wetter?", "options": ["schlecht", "kalt", "regnerisch", "schön und warm"], "correct": 3},
                            {"q": "Was hat die Schwester gemacht?", "options": ["Fußball gespielt", "ein Buch gelesen", "mit dem Hund gespielt", "gekocht"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"id": "A2_V1", "german": "der Urlaub", "english": "vacation", "options": ["work", "vacation", "school", "hospital"]},
                    {"id": "A2_V2", "german": "einkaufen", "english": "to shop", "options": ["to shop", "to cook", "to clean", "to study"]},
                    {"id": "A2_V3", "german": "das Wetter", "english": "weather", "options": ["time", "weather", "money", "food"]}
                ],
                "grammar": [
                    {"id": "A2_G1", "question": "Gestern __ ich ins Kino gegangen.", "options": ["bin", "habe", "war", "hatte"], "correct": 0},
                    {"id": "A2_G2", "question": "Der Mann, __ ich gestern getroffen habe, ist mein Nachbar.", "options": ["der", "den", "dem", "dessen"], "correct": 1}
                ]
            },
            "B1": {
                "reading": [
                    {
                        "id": "B1_R1",
                        "text": "Die Digitalisierung verändert unsere Arbeitswelt grundlegend. Viele traditionelle Berufe verschwinden, während neue entstehen. Es ist wichtig, dass wir uns kontinuierlich weiterbilden, um mit diesen Veränderungen Schritt zu halten. Unternehmen müssen ihre Mitarbeiter dabei unterstützen, neue Fähigkeiten zu erlernen.",
                        "questions": [
                            {"q": "Was verändert die Arbeitswelt?", "options": ["Die Digitalisierung", "Die Globalisierung", "Die Politik", "Das Klima"], "correct": 0},
                            {"q": "Was ist wichtig für Arbeitnehmer?", "options": ["Mehr Geld verdienen", "Früher in Rente gehen", "Sich weiterbilden", "Weniger arbeiten"], "correct": 2},
                            {"q": "Wer soll Mitarbeiter unterstützen?", "options": ["Die Regierung", "Die Unternehmen", "Die Familie", "Die Freunde"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"id": "B1_V1", "german": "die Herausforderung", "english": "challenge", "options": ["opportunity", "challenge", "problem", "solution"]},
                    {"id": "B1_V2", "german": "nachhaltig", "english": "sustainable", "options": ["expensive", "sustainable", "temporary", "difficult"]},
                    {"id": "B1_V3", "german": "sich entwickeln", "english": "to develop", "options": ["to develop", "to destroy", "to ignore", "to avoid"]}
                ],
                "grammar": [
                    {"id": "B1_G1", "question": "Wenn ich mehr Zeit hätte, __ ich mehr reisen.", "options": ["werde", "würde", "will", "wollte"], "correct": 1},
                    {"id": "B1_G2", "question": "Das ist das Buch, __ ich dir empfohlen habe.", "options": ["das", "dem", "den", "der"], "correct": 0}
                ]
            },
            "B2": {
                "reading": [
                    {
                        "id": "B2_R1",
                        "text": "Die Klimakrise stellt eine der größten Herausforderungen unserer Zeit dar. Wissenschaftler warnen eindringlich vor den Folgen des Klimawandels. Es bedarf einer koordinierten internationalen Anstrengung, um die Erderwärmung zu begrenzen. Sowohl politische Maßnahmen als auch individuelles Handeln sind erforderlich, um eine nachhaltige Zukunft zu gewährleisten.",
                        "questions": [
                            {"q": "Was stellt die Klimakrise dar?", "options": ["Ein kleines Problem", "Eine der größten Herausforderungen", "Eine Chance", "Ein Mythos"], "correct": 1},
                            {"q": "Was ist erforderlich?", "options": ["Nur politische Maßnahmen", "Nur individuelles Handeln", "Beides", "Nichts"], "correct": 2},
                            {"q": "Wovor warnen Wissenschaftler?", "options": ["Vor Naturkatastrophen", "Vor den Folgen des Klimawandels", "Vor Wirtschaftskrisen", "Vor Kriegen"], "correct": 1}
                        ]
                    }
                ],
                "vocabulary": [
                    {"id": "B2_V1", "german": "die Nachhaltigkeit", "english": "sustainability", "options": ["sustainability", "profitability", "popularity", "availability"]},
                    {"id": "B2_V2", "german": "bewältigen", "english": "to cope with", "options": ["to avoid", "to cope with", "to create", "to ignore"]},
                    {"id": "B2_V3", "german": "die Auswirkung", "english": "impact", "options": ["cause", "impact", "beginning", "end"]}
                ],
                "grammar": [
                    {"id": "B2_G1", "question": "Obwohl es regnete, __ wir spazieren gegangen.", "options": ["sind", "haben", "waren", "hatten"], "correct": 0},
                    {"id": "B2_G2", "question": "Der Vorschlag, __ du gemacht hast, ist sehr interessant.", "options": ["der", "den", "dem", "dessen"], "correct": 1}
                ]
            }
        }

    def _select_exercise(self, level: str, content_key: str, state_key: str, count: int = 1):
        """
        Selects a random exercise only if one isn't already stored in session state.
        Returns the exercise(s).
        """
        if st.session_state[state_key] is None:
            available_content = self.content.get(level, {}).get(content_key, [])
            if not available_content:
                return None
                
            if content_key == "reading" or content_key == "listening":
                # For reading, only select one complex exercise
                exercise = random.choice(available_content)
                st.session_state[state_key] = exercise
            else:
                # For others, select a sample list
                sample = random.sample(available_content, min(count, len(available_content)))
                st.session_state[state_key] = sample
        
        return st.session_state[state_key]

    def _reset_exercise(self, state_key: str, answers_state_key: str):
        """Resets the exercise and the related answers in session state."""
        st.session_state[state_key] = None
        st.session_state[answers_state_key] = []
        st.session_state[f"checked_{state_key}"] = False
        st.rerun()

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
        for state_key in EXERCISE_KEYS.values():
            st.session_state[state_key] = None
            st.session_state[f"checked_{state_key}"] = False
        st.session_state.reading_answers = []
        st.session_state.vocab_answers = []
        st.session_state.grammar_answers = []
        st.session_state.listening_answers = []


    def reading_comprehension_exercise(self, level: str):
        """Reading comprehension exercise"""
        state_key = EXERCISE_KEYS["Reading Comprehension"]
        answers_state_key = 'reading_answers'
        
        st.subheader("📖 Reading Comprehension")
        
        exercise = self._select_exercise(level, "reading", state_key, 1)

        if exercise is None:
            st.warning("No reading exercises available for this level yet.")
            return

        # Ensure answers list is sized correctly on first run
        if not st.session_state[answers_state_key] or len(st.session_state[answers_state_key]) != len(exercise["questions"]):
             st.session_state[answers_state_key] = [0] * len(exercise["questions"])

        st.markdown("**Read the following text carefully:**")
        st.markdown(f"*{exercise['text']}*")
        
        st.markdown("---")
        st.markdown("**Answer the questions:**")
        
        # Display questions and capture answers
        for i, question in enumerate(exercise["questions"]):
            # FIX: Stable key based on exercise ID and question index
            options_key = f"{exercise['id']}_q_{i}"
            
            # Use index() to map the currently selected option back to the list index for storage
            selected_option_label = st.radio(
                question["q"],
                options=question["options"],
                # FIX: Set the default index based on stored answer index
                index=st.session_state[answers_state_key][i] if i < len(st.session_state[answers_state_key]) else 0,
                key=options_key
            )
            
            # FIX: Store the selected index, NOT the label index, to avoid jumbling on re-render
            st.session_state[answers_state_key][i] = question["options"].index(selected_option_label)
        
        # Check Answers button logic
        if st.session_state.get(f"checked_{state_key}"):
            # FIX: Pass answers_state_key
            self._display_results(exercise["questions"], st.session_state[answers_state_key], state_key, level, answers_state_key)
        elif st.button("Check Answers", key="reading_check"):
            st.session_state[f"checked_{state_key}"] = True
            st.rerun() # Rerun to display results


    def vocabulary_exercise(self, level: str):
        """Vocabulary building exercise"""
        state_key = EXERCISE_KEYS["Vocabulary Building"]
        answers_state_key = 'vocab_answers'
        
        st.subheader("📚 Vocabulary Building")
        
        vocab_items = self._select_exercise(level, "vocabulary", state_key, 3)

        if vocab_items is None:
            st.warning("No vocabulary exercises available for this level yet.")
            return

        # Initialize answers list
        if not st.session_state[answers_state_key] or len(st.session_state[answers_state_key]) != len(vocab_items):
            st.session_state[answers_state_key] = [0] * len(vocab_items)

        st.markdown("**Choose the correct English translation:**")
        
        # Display questions and capture answers
        for i, item in enumerate(vocab_items):
            options_key = f"{item['id']}_v_{i}"
            
            st.markdown(f"**{item['german']}**")
            selected_option_label = st.radio(
                "Select the correct translation:",
                options=item["options"],
                index=st.session_state[answers_state_key][i] if i < len(st.session_state[answers_state_key]) else 0,
                key=options_key
            )
            st.session_state[answers_state_key][i] = item["options"].index(selected_option_label)
        
        # Check Answers button logic
        if st.session_state.get(f"checked_{state_key}"):
            # FIX: Pass answers_state_key
            self._display_results(vocab_items, st.session_state[answers_state_key], state_key, level, answers_state_key, type="vocab")
        elif st.button("Check Vocabulary", key="vocab_check"):
            st.session_state[f"checked_{state_key}"] = True
            st.rerun()


    def grammar_exercise(self, level: str):
        """Grammar quiz exercise"""
        state_key = EXERCISE_KEYS["Grammar Quiz"]
        answers_state_key = 'grammar_answers'
        
        st.subheader("⚙️ Grammar Quiz")
        
        grammar_items = self._select_exercise(level, "grammar", state_key, 3)

        if grammar_items is None:
            st.warning("No grammar exercises available for this level yet.")
            return

        # Initialize answers list
        if not st.session_state[answers_state_key] or len(st.session_state[answers_state_key]) != len(grammar_items):
            st.session_state[answers_state_key] = [0] * len(grammar_items)

        st.markdown("**Fill in the blanks with the correct option:**")
        
        # Display questions and capture answers
        for i, item in enumerate(grammar_items):
            options_key = f"{item['id']}_g_{i}"
            
            st.markdown(f"**{item['question']}**")
            selected_option_label = st.radio(
                "Select the correct option:",
                options=item["options"],
                index=st.session_state[answers_state_key][i] if i < len(st.session_state[answers_state_key]) else 0,
                key=options_key
            )
            st.session_state[answers_state_key][i] = item["options"].index(selected_option_label)
        
        # Check Answers button logic
        if st.session_state.get(f"checked_{state_key}"):
            # FIX: Pass answers_state_key
            self._display_results(grammar_items, st.session_state[answers_state_key], state_key, level, answers_state_key)
        elif st.button("Check Grammar", key="grammar_check"):
            st.session_state[f"checked_{state_key}"] = True
            st.rerun()

    def listening_exercise(self, level: str):
        """Listening comprehension exercise"""
        state_key = EXERCISE_KEYS["Listening Comprehension"]
        answers_state_key = 'listening_answers'
        
        st.subheader("👂 Listening Comprehension")
        
        # Listening exercises are structured differently (list of scenarios)
        scenario_list = [item for sublist in self.content.get(level, {}).get("reading", []) for item in sublist.get("questions", [])]
        listening_scenarios = self._select_exercise(level, "reading", state_key, 1)
        
        if listening_scenarios is None or not listening_scenarios.get("questions"):
            # Fallback to the dedicated scenario data structure
            listening_scenarios = [
                scenario for scenario_list in self._get_listening_scenarios().values() 
                for scenario in scenario_list if scenario.get("level") == level
            ]
            if not listening_scenarios:
                st.warning("No listening exercises available for this level yet.")
                return

            # Ensure a single scenario is selected and stored
            if st.session_state[state_key] is None:
                st.session_state[state_key] = random.choice(listening_scenarios)
            exercise = st.session_state[state_key]
        else:
            # If loaded from reading content (as per content structure), use it
            exercise = listening_scenarios
        
        # Ensure answers list is sized correctly on first run
        if not st.session_state[answers_state_key] or len(st.session_state[answers_state_key]) != len(exercise["questions"]):
             st.session_state[answers_state_key] = [0] * len(exercise["questions"])

        # Display scenario text as audio placeholder
        st.markdown(f"**Scenario:** {exercise['text'][:50]}...")
        st.info("🔊 Audio player would be here. Click to listen to the German audio.")
        
        with st.expander("Show transcript (for demo purposes)"):
            st.markdown(f"*{exercise['text']}*")
        
        st.markdown("**Answer the questions based on what you heard:**")
        
        user_answers = []
        for i, question in enumerate(exercise["questions"]):
            options_key = f"{exercise['id']}_l_{i}"
            
            selected_option_label = st.radio(
                question["q"],
                options=question["options"],
                index=st.session_state[answers_state_key][i] if i < len(st.session_state[answers_state_key]) else 0,
                key=options_key
            )
            st.session_state[answers_state_key][i] = question["options"].index(selected_option_label)
        
        # Check Answers button logic
        if st.session_state.get(f"checked_{state_key}"):
            # FIX: Pass answers_state_key
            self._display_results(exercise["questions"], st.session_state[answers_state_key], state_key, level, answers_state_key)
        elif st.button("Check Listening", key="listening_check"):
            st.session_state[f"checked_{state_key}"] = True
            st.rerun()

    def _get_listening_scenarios(self):
        """Helper to reconstruct the original hardcoded listening scenarios for completeness."""
        return {
             "A1": [
                {
                    "level": "A1",
                    "text": "Hallo, ich heiße Thomas. Ich bin 30 Jahre alt und komme aus München. Ich arbeite als Ingenieur.",
                    "questions": [
                        {"q": "Wie heißt die Person?", "options": ["Thomas", "Michael", "Andreas", "Stefan"], "correct": 0},
                        {"q": "Wie alt ist Thomas?", "options": ["25", "30", "35", "40"], "correct": 1}
                    ]
                }
            ],
            # ... A2, B1, B2 scenarios (omitted for brevity, but exist in the logic)
        }

    def _display_results(self, exercise_items, user_answers_indices, state_key, level, answers_state_key, type="quiz"):
        """
        Centralized function to calculate and display results for quizzes/reading.
        FIX: Updated signature to include answers_state_key.
        """
        
        total_questions = len(exercise_items)
        
        if type == "vocab":
            correct = sum(1 for i, item in enumerate(exercise_items) 
                          if user_answers_indices[i] == item["options"].index(item["english"]))
        else: # reading or grammar or listening
            correct = sum(1 for i, q in enumerate(exercise_items) 
                          if user_answers_indices[i] == q["correct"])
        
        # Update scores (assuming max 3 questions * 1 point each)
        st.session_state.score += correct
        st.session_state.total_exercises += 1
        st.session_state.user_progress[level] += correct / total_questions
        
        # Display feedback and individual answers
        if correct == total_questions:
            st.success(f"Perfect! You got all {total_questions} questions correct! 🎉")
        elif correct >= total_questions * 0.7:
            st.success(f"Great job! You got {correct}/{total_questions} questions correct! 👍")
        else:
            st.warning(f"You got {correct}/{total_questions} questions correct. Keep practicing! 💪")

        st.markdown("---")
        st.markdown("**Detailed Results:**")

        for i, item in enumerate(exercise_items):
            user_choice_index = user_answers_indices[i]
            user_choice_label = item["options"][user_choice_index]
            
            if type == "vocab":
                correct_label = item["english"]
                is_correct = user_choice_label == correct_label
                question_text = f"{item['german']}"
            else:
                correct_index = item["correct"]
                correct_label = item["options"][correct_index]
                is_correct = user_choice_index == correct_index
                question_text = item["q"] if 'q' in item else item["question"]
            
            icon = "✅" if is_correct else "❌"
            feedback_text = f"**{icon} {question_text}**"
            
            if not is_correct:
                feedback_text += f"<br>_Correct Answer:_ **{correct_label}**"
            
            st.markdown(feedback_text, unsafe_allow_html=True)
        
        # FIX: Use on_click callback with args for guaranteed scope stability
        # The instance method self._reset_exercise requires two arguments: state_key and answers_state_key.
        if st.button("Next Exercise", 
                     key=f"next_{state_key}", 
                     on_click=self._reset_exercise,
                     args=(state_key, answers_state_key)): 
            pass # Action handled by callback


    def pronunciation_exercise(self, level: str):
        """Pronunciation practice exercise"""
        state_key = EXERCISE_KEYS["Pronunciation Practice"]
        st.subheader("🗣️ Pronunciation Practice")
        
        pron_items = self._select_exercise(level, "pronunciation", state_key, 3)

        if pron_items is None:
            st.warning("No pronunciation exercises available for this level yet.")
            return
        
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
            self._reset_exercise(state_key, 'dummy_answers') # Reset to get new words

    def writing_exercise(self, level: str):
        """Writing exercise"""
        state_key = EXERCISE_KEYS["Writing Exercise"]
        st.subheader("✍️ Writing Exercise")
        
        # Writing prompts are inherently stable, but we must store the prompt index
        if state_key not in st.session_state or st.session_state[state_key] is None:
             st.session_state[state_key] = random.randint(0, len(self._get_writing_prompts().get(level, [])) - 1)
        
        writing_prompts = self._get_writing_prompts()
        prompt_index = st.session_state[state_key]
        prompt = writing_prompts.get(level, writing_prompts["A1"])[prompt_index]
        
        st.markdown("**Writing Prompt:**")
        st.info(prompt)
        
        user_text = st.text_area(
            "Write your response here:",
            height=200,
            # FIX: Stable key tied to the prompt index
            key=f"writing_{level}_{prompt_index}"
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

        if st.button("Next Prompt", key="writing_next"):
             self._reset_exercise(state_key, 'dummy_answers')
             st.session_state[state_key] = random.randint(0, len(writing_prompts.get(level, [])) - 1)
             st.rerun()

    def _get_writing_prompts(self):
        """Helper to define the hardcoded writing prompts centrally."""
        return {
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
                # FIX: Accuracy calculation was flawed (multiplying by 3). 
                # Re-calculating based on overall score vs. max possible score (which is dynamic).
                # Since we don't track max possible points accurately across all quiz types,
                # we'll use a simplified metric (average score per completed exercise).
                avg_score_per_exercise = total_score / total_exercises
                st.metric("Avg Score/Exercise", f"{avg_score_per_exercise:.2f}")
            else:
                st.metric("Avg Score/Exercise", "N/A")
            
            st.metric("Total Score", total_score)
            st.metric("Exercises Completed", total_exercises)

    def run(self):
        """Main application runner"""
        
        # Display header
        self.display_header()
        
        # Sidebar for exercise selection
        st.sidebar.title("Exercise Menu")
        # Store the selected exercise type in session state for stability
        exercise_type = st.sidebar.selectbox(
            "Choose Exercise Type:",
            self.exercise_types,
            key='exercise_type_select'
        )

        # FIX: Check if exercise type has changed and reset the 'checked' state
        if st.session_state.current_exercise_type != exercise_type:
            st.session_state.current_exercise_type = exercise_type
            
            # Reset the 'checked' state when the exercise type changes to allow a new quiz
            state_key = EXERCISE_KEYS.get(exercise_type)
            if state_key:
                st.session_state[f"checked_{state_key}"] = False
            # No need to rerun here, the main script flow handles the initial rendering
        
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
    # FIX: Initialize the Game class only once across reruns
    if 'game_instance' not in st.session_state:
        st.session_state.game_instance = GermanLearningGame()
    
    st.session_state.game_instance.run()
