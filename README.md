# Anime Analysis

<br />

## An analysis of the first 15000 anime listed on [MyAnimeList](https://myanimelist.net/topanime.php)'s top rated page.

<br />

### Section 1 - Dataset Creation
This section features the creation of the dataset of the top 15000 anime listed on [MyAnimeList](https://myanimelist.net/topanime.php)'s top rated page, where it is saved to CSV files for later.
 - Scrape each page on the website and store all of the page's data in it's own CSV file
 - For every anime on the page, go through and scrape it's data then store it in it's respective CSV
 
<br />

### Section 2 - Data handling and cleaning
This section deals with the importing and creation of the raw dataframe containing the data from all of the CSV's, then cleaning this dataset and creating functions which can perform specific parses on the data for each section we need it without removing too many rows that could of been used otherwise.
 - Append the data from all of the CSV's to a single dataframe
 - Convert the columns to their correct types
 - Create a function which can parse the score column
 - Creation a function which can parse the broadcast time column
 - Create a function which can parse the episode length column
 - Create a function which can parse the aired time column
 
<br />

### Section 3 - Analysis of the data
This section deals with analysing and drawing insights out of the data to answer the questions asked.
 - Find what was the highest rated show across all of it's scorers
 - Find the most popular genre
 - Find the best time of a month to launch a show to maximize watchers
 - Find the best time to broadcast a show to maximize watchers
 - Find the studios that have the best ratings across their scorers
 - Find the licensors that have the best ratings across their scorers
 
<br />

### Section 4 - Data preprocessing for the model
This section deals with processing the data for the model and creating a dataset that we can use to train the model which predicts if a show will be above or below the mean rating.
 - Create a function which will remove bad characters from a word
 - Create a function which takes in a dataframe containing the data and outputs a block of text for the model, and the labels for that text
 - Encode the text into numerical form to be processed by the model
 - Remove outlier text sizes and pad or truncate text to fit the size for the model
 - Convert the labels to 1 or 0 based on if the score is respectively above or below the mean score
 
<br />

### Section 5 - Dataset allocation
This section deals with creating properly sized datasets to be fed through the model.
 - Remove the remainder of the dataset that prevents its length from being divisible by 10
 - Create the training dataset out of 80% of the data
 - Create the validation dataset out of 10% of the remaining data
 - Create the test dataset out of the the remaning 10% of the data

<br />

### Section 6 - Model building
This section deals with building the model class and the functions that come along with it.
 - Create a bidirectional LSTM network which gets fed into a dense layer with a ReLU, which gets fed into a sigmoid layer which outputs a probability of it being above or below the mean rating
 - Add loading and saving functions for the model
 - Add functions which can provide analytics of how the data performs during training
 
<br />

### Section 7 - Model training
This section deals with the training of the model on the data created.
 - Train the model on the train dataset
 - Save the model for later user

<br />

### Section 8 - Model analysis
This section deals with the analysis of the models performance during training.
 - Evaluate the model on the test dataset and show the loss and accuracy
 - Plot the history of the accuracy and loss for every epoch on the training set during training
 - Plot the history of the accuracy and loss for every epoch on the validation set during training

<br />

### Section 9 - Model testing
This section deals with testing the model on the test data created.
 - Aanalyse some samples from the test data
 - Create a function which parses custom data to predict if the show will be above or below the mean

#### Credit
 - The data from this project came from [MyAnimeList](https://myanimelist.net/topanime.php)'s top rated page
 - This project was created by [Ben Osborn](https://github.com/BenOsborn) for [OsbornAI](https://github.com/OsbornAI)
