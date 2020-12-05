# What is our model going to contain?
# What architecture should we use?
# For my saved model I might need to include a .gitignore

# Just for this case we might want to store this on the server and parse it through accordingly
# Create a bag of words from all of our training examples to be stored elsewhere 
# If our word is not in the bag of words then we will remove it
# We then encode our words into numbers for each sequence
# We then feed in our words into our model to make a classification of where it should be recommended

# We will use siamese networks with stateful features to determine if two vectors are the same
# We will feed in our input into these networks to make the prediction and then output them

class Model:
    def __init__(self):
        pass