import sys
import os
import random
import tempfile
from gtts import gTTS
import nltk
from nltk.corpus import wordnet as wn
import time

nltk.download('wordnet')

def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

def pick_random_word(file_path):
    with open(file_path, 'r') as file:
        words = file.read().split()
        return random.choice(words)

def get_word_details(word):
    # Preprocess the word
    word = word.lower().strip()

    # Check if the word is in WordNet
    synsets = wn.synsets(word)
    
    if synsets:
        synset = synsets[0]
        definition = synset.definition()
        word_with_definition = f"{word}: {definition}"
        return word_with_definition
    else:
        return None  # Return None if no definition is found

def play_spelling_game():
    dictionary_file_path = 'cleaned_dictionary.txt'
    correct_guesses = 0
    incorrect_guesses = 0
    
    for _ in range(10):
        while True:
            random_word = pick_random_word(dictionary_file_path)
            word_and_definition = get_word_details(random_word)
            if word_and_definition:
                break  # Exit the loop if a word with definition is found
        
        print("Listen to the definition and spell the word.")
        
        # Split the word and definition
        word, definition = word_and_definition.split(': ', 1)
        
        # Convert the word to speech
        word_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3").name
        text_to_speech(word, word_audio_file)
        
        # Convert the definition to speech
        definition_audio_file = tempfile.NamedTemporaryFile(suffix=".mp3").name
        text_to_speech(definition, definition_audio_file)
        
        repeat = 'yes'
        while repeat == 'yes':
            # Play the word audio
            os.system("start " + word_audio_file)
            time.sleep(2)  # Adjust the delay time as needed
            
            # Play the definition audio
            os.system("start " + definition_audio_file)
            time.sleep(2)
            
            # Ask if the user wants to repeat
            repeat = input("Would you like to hear the word and definition again? (yes/no): ").lower()
        
        # Ask the user to spell the word
        guess = input("Listen to the definition and spell the word: ").lower()
        
        # Check if the user's guess matches the word
        if guess == random_word.lower():
            print("Congratulations! You spelled the word correctly.")
            correct_guesses += 1
        else:
            print(f"Sorry, the correct spelling of the word was '{random_word}'. Better luck next time!")
            incorrect_guesses += 1
    
    print("\nGame Over!")
    print("Correct guesses:", correct_guesses)
    print("Incorrect guesses:", incorrect_guesses)

play_spelling_game()