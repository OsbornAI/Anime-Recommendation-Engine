from collections import Counter
import string

# What is our model going to contain?
# What architecture should we use?
# For my saved model I might need to include a .gitignore

# Just for this case we might want to store this on the server and parse it through accordingly
# Create a bag of words from all of our training examples to be stored elsewhere 
# If our word is not in the bag of words then we will remove it
# We then encode our words into numbers for each sequence
# We then feed in our words into our model to make a classification of where it should be recommended

# Model architecture:
#   - We will have a stateful LSTM which has a batch size of one for the embedding layer
#   - This will output a prediction which we will store along with our values
#   - On our training when the user interacts with the item, we will train on our batch, attempting to minimize a contrastive loss function

class Model:
    def __init__(self, anime_df):
        # We need to go through and make a word list here
        phrase_list = []

        # Consider the names, the studios, the licensors, the producers, the genres and the descriptions of each show, concatenate them together
        anime_df['name_english'].apply(lambda x: self.__appendList(x, phrase_list))
        anime_df['name_japanese'].apply(lambda x: self.__appendList(x, phrase_list))
        anime_df['studios'].apply(lambda x: self.__appendList(x, phrase_list))
        anime_df['licensors'].apply(lambda x: self.__appendList(x, phrase_list))
        anime_df['producers'].apply(lambda x: self.__appendList(x, phrase_list))
        anime_df['genres'].apply(lambda x: self.__appendList(x, phrase_list))
        anime_df['description'].apply(lambda x: self.__appendList(x, phrase_list))

        phrases = " ".join(phrase_list).split(' ')
        self.__words = {phrase[0]: i + 1 for i, phrase in enumerate(Counter(phrases).most_common())} # We will set our words to begin at one so we have the option of padding with zeros if we want

        print(len(self.__words))

    def __cleanPhrase(self, phrase):
        phrase = phrase.strip()
        phrase = phrase.lower()
        phrase = "".join([char for char in phrase if char in string.ascii_letters + ' '])

        return phrase

    def __appendList(self, raw_string, append_list):
        try:
            split = raw_string.split(',')
            split = [self.__cleanPhrase(phrase) for phrase in split]

            for item in split:
                append_list.append(item)

        except:
            pass

    def processPhrase(self, phrase):
        phrase = self.__cleanPhrase(phrase)
        word_keys = self.__words.keys()
        encoded_phrase = [self.__words[word] if word in word_keys else 0 for word in phrase.split(' ')]

        return encoded_phrase # No padding is required since we are using stateful LSTM's

    