# -*- coding: utf-8 -*-
"""twitter_segment_analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SfH2USU0qq7EVdc8SyKFh0cqKeozjRTN
"""

#Importing necessary libraries
import pandas as pd
import numpy as np
import re
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

!pip install nltk

# Get the English stopwords from the NLTK stopwords dataset
# These are words that are often excluded from text analysis as they typically don't carry much meaning
# and are commonly used (e.g., 'the', 'and', 'is')
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords', download_dir='/usr/share/nltk_data')

stop_words = set(stopwords.words('english'))

df = pd.read_csv('vaccination_tweets.csv')

df.head()

df.info()

df.isnull().sum() #Count the number of missing values in each column of the DataFrame 'df'

df.columns #returns the columns

text_df = df.drop(['id', 'user_name', 'user_location', 'user_description', 'user_created',
       'user_followers', 'user_friends', 'user_favourites', 'user_verified',
       'date', 'hashtags', 'source', 'retweets', 'favorites',
       'is_retweet'], axis=1) #Axis 1 indicats column

#Now we have a dataframe only consisting of the text and index(dropped all unnecessary options)
text_df.head()

print(text_df['text'].iloc[0],"\n")
print(text_df['text'].iloc[1],"\n")
print(text_df['text'].iloc[2],"\n")
print(text_df['text'].iloc[3],"\n")
print(text_df['text'].iloc[4],"\n")

text_df.info()

#re.sub() function allows you to replace occurrences of a pattern in a string with a specified replacement.
def data_processing(text):
    text = text.lower()
    text = re.sub(r"https\S+|www\S+https\S+", '',text, flags=re.MULTILINE)
    text = re.sub(r'\@w+|\#','',text)
    text = re.sub(r'[^\w\s]','',text)
    text_tokens = word_tokenize(text)
    filtered_text = [w for w in text_tokens if not w in stop_words]
    return " ".join(filtered_text) #Joins the filtered words back into a single string, separating them with spaces, and returns the processed text.

nltk.download('punkt')
# Applying the data_processing function to each element in the 'text' column of the DataFrame
text_df['text'] = text_df['text'].apply(data_processing) #.apply() is a function provided by Pandas for DataFrames

text_df = text_df.drop_duplicates('text')
#remove duplicate rows from the DataFrame based on 'text'. It returns a new DataFrame with duplicate rows removed.

stemmer = PorterStemmer()
def stemming(data):
    text = [stemmer.stem(word) for word in data]
    return data

text_df['text'] = text_df['text'].apply(lambda x: stemming(x))
# lamda is used to apply the stemming function to each element in the 'text' column.

text_df.head()

print(text_df['text'].iloc[0],"\n")
print(text_df['text'].iloc[1],"\n")
print(text_df['text'].iloc[2],"\n")
print(text_df['text'].iloc[3],"\n")
print(text_df['text'].iloc[4],"\n")

#As text_df is already a  DataFrame & datatframe has a default integer index, use direct indexing without specifying loc or iloc:
print(text_df['text'][0], "\n")
print(text_df['text'][1], "\n")
print(text_df['text'][2], "\n")
print(text_df['text'][3], "\n")
print(text_df['text'][4], "\n")

text_df.info()

def polarity(text):
    return TextBlob(text).sentiment.polarity

#polarity function calculates and returns the sentiment polarity of the input text using the TextBlob library
#Sentiment polarity is usually calculated using machine learning techniques or pre-trained models. The TextBlob library, which your polarity function utilizes, is one such tool that provides a pre-trained model for sentiment analysis.
#Example:
#For instance, a positive sentence like "I love this product" might have a high positive polarity score (close to 1),
#while a negative sentence like "I hate waiting" might have a high negative polarity score (close to -1).

text_df['polarity'] = text_df['text'].apply(polarity)

text_df.head(10)

def sentiment(label):
    if label <0:
        return "Negative"
    elif label ==0:
        return "Neutral"
    elif label>0:
        return "Positive"

text_df['sentiment'] = text_df['polarity'].apply(sentiment)

text_df.head()

fig = plt.figure(figsize=(5,5))
sns.countplot(x='sentiment', data = text_df)

tags = text_df['sentiment'].value_counts() #.value_counts() is indeed an in-built function in pandas
print(tags)

# Create a figure with a specified size
fig = plt.figure(figsize=(7, 7))
# Define colors for the pie chart
colors = ("yellowgreen", "gold", "red")
# Define properties for wedge (slices) in the pie chart
wp = {'linewidth': 2, 'edgecolor': "black"}
# Count the occurrences of each sentiment category in the 'sentiment' column of the 'text_df' DataFrame
tags = text_df['sentiment'].value_counts()

# Define the degree to which each slice of the pie should be exploded (pulled out)
explode = (0.1, 0.1, 0.1)

# Plot a pie chart using the data from 'tags'
tags.plot(kind='pie', autopct='%1.1f%%', shadow=True, colors=colors,
          startangle=90, wedgeprops=wp, explode=explode, label='')

# Set the title of the pie chart
plt.title('Distribution of sentiments')

# Display the pie chart
plt.show()

pos_tweets = text_df[text_df.sentiment == 'Positive'] # Filter rows in 'text_df' where sentiment is 'Positive'
pos_tweets = pos_tweets.sort_values(['polarity'], ascending=False) # Sort the filtered DataFrame based on the 'polarity' column in descending order
pos_tweets.head() # Display the first few rows of the sorted DataFrame

pos_tweets["text"]

""" nltk.tokenize.word_tokenize function is used to tokenize each sentence into individual words before joining them into the text variable. This ensures that the word cloud is based on individual words rather than entire sentences.

 A word cloud is a data visualization technique that represents textual data in a graphical form, where the size of each word indicates its frequency or importance in the given text. The more frequently a word appears in the text, the larger and bolder it appears in the word cloud. It is a visualization technique that involves simple statistical and graphical methods to represent the frequency of words in a given text.
"""

# Import necessary libraries
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize

# Concatenate all words in the 'text' column of positive tweets
text = ' '.join([word
                 for sentence in pos_tweets['text']  # Loop over each sentence in the 'text' column
                 for word in word_tokenize(sentence)])  # Tokenize each sentence into words and loop over the words

# Create a figure with specified size
plt.figure(figsize=(20, 15), facecolor='None')

# Generate a WordCloud using the concatenated text
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)

# Display the WordCloud with interpolation set to 'bilinear'
plt.imshow(wordcloud, interpolation='bilinear') #interpolation='bilinear' setting is often used to make the display look smoother and more visually appealing.

# Turn off axis for better visualization
plt.axis("off")

# Set the title of the plot
plt.title('Most frequent words in positive tweets', fontsize=19)

# Show the plot
plt.show()

"""Here's a brief explanation of some common interpolation methods:

Nearest-neighbor ('nearest'): Uses the value of the nearest pixel to the non-integer coordinates.

Bilinear ('bilinear'): Calculates the weighted average of the nearest four pixels based on their distances.

Bicubic ('bicubic'): A higher-order interpolation method that uses a cubic polynomial.

Choosing the interpolation method depends on the specific visualization requirements and the desired visual appearance. Bilinear interpolation is a good choice for smoothing out the display of images, including word clouds.
"""

neg_tweets = text_df[text_df.sentiment == 'Negative']
neg_tweets = neg_tweets.sort_values(['polarity'], ascending= False)
neg_tweets.head()

# Concatenate all words in the 'text' column of negative tweets
text = ' '.join([word
                 for sentence in neg_tweets['text']  # Loop over each sentence in the 'text' column
                 for word in word_tokenize(sentence)])  # Tokenize each sentence into words and loop over the words
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in negative tweets', fontsize=19)
plt.show()

neutral_tweets = text_df[text_df.sentiment == 'Neutral']
neutral_tweets = neutral_tweets.sort_values(['polarity'], ascending= False)
neutral_tweets.head()

# Concatenate all words in the 'text' column of neutral tweets
text = ' '.join([word
                 for sentence in neutral_tweets['text']  # Loop over each sentence in the 'text' column
                 for word in word_tokenize(sentence)])  # Tokenize each sentence into words and loop over the words
plt.figure(figsize=(20,15), facecolor='None')
wordcloud = WordCloud(max_words=500, width=1600, height=800).generate(text)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title('Most frequent words in neutral tweets', fontsize=19)
plt.show()

# Create a CountVectorizer object with ngram_range=(1,2)
# This means we are considering unigrams (single words) and bigrams (two consecutive words) as features
vect = CountVectorizer(ngram_range=(1,2)).fit(text_df['text'])

#vect = CountVectorizer(ngram_range=(1,2), max_features=1000).fit(text_df['text'])
#max_features=1000 means that only the top 1000 features (words or word pairs) with the highest term frequencies
#across the entire corpus will be kept.
#If max_features is not specified, it considers all features in the vocabulary.

feature_names = vect.get_feature_names_out()
print("Number of features: {}\n".format(len(feature_names)))
print("First 20 features:\n {}".format(feature_names[:20]))

X = text_df['text'] # Extract the 'text' column from the DataFrame as the feature variable X
Y = text_df['sentiment'] # Extract the 'sentiment' column from the DataFrame as the target variable Y

# Use the fitted CountVectorizer to transform the 'text' data into a bag-of-words representation
# The transform method converts the text data into a sparse matrix where each row represents a document
# and each column represents a unique word or word pair learned during the fitting process
X = vect.transform(X)

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

print("Size of x_train:", (x_train.shape))
print("Size of y_train:", (y_train.shape))
print("Size of x_test:", (x_test.shape))
print("Size of y_test:", (y_test.shape))

#Using logistic regression
logreg = LogisticRegression()
logreg.fit(x_train, y_train)
logreg_pred = logreg.predict(x_test)
logreg_acc = accuracy_score(logreg_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

print(confusion_matrix(y_test, logreg_pred))
print("\n")
print(classification_report(y_test, logreg_pred))

style.use('classic')
cm = confusion_matrix(y_test, logreg_pred, labels=logreg.classes_)
# Create a ConfusionMatrixDisplay object with the confusion matrix and class labels
disp = ConfusionMatrixDisplay(confusion_matrix = cm, display_labels=logreg.classes_)
disp.plot()

from sklearn.model_selection import GridSearchCV

"""GridSearchCV is a method provided by scikit-learn for performing an exhaustive search over a specified parameter grid to find the best set of hyperparameters for a machine learning model. It is used for hyperparameter tuning."""

param_grid={'C':[0.001, 0.01, 0.1, 1, 10]}
#Define a dictionary specifying the hyperparameter grid to search over. In this case,
#it's the regularization parameter C for logistic regression, and the grid includes values [0.001, 0.01, 0.1, 1, 10].
grid = GridSearchCV(LogisticRegression(), param_grid)
grid.fit(x_train, y_train)
#Fit the grid search to the training data (x_train, y_train).
#This step performs an exhaustive search over the specified hyperparameter grid, training and evaluating the logistic
#regression model with different values of C using cross-validation.

print("Best parameters:", grid.best_params_) #output the best hyperparameters found by the grid search
#It will display the best value of C that maximizes the specified scoring metric. T

"""In this case, it will try logistic regression models with C values of 0.001, 0.01, 0.1, 1, and 10, and it will select the one that performs the best.
These best hyperparameters are then used to train the final model.
"""

y_pred = grid.predict(x_test)

logreg_acc = accuracy_score(y_pred, y_test)  #accuracy improves slightly using hyperparameter tuning than without hyperparameter tuning
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

print(confusion_matrix(y_test, y_pred))
print("\n")
print(classification_report(y_test, y_pred))

from sklearn.svm import LinearSVC #trying support vector classifier

SVCmodel = LinearSVC()
SVCmodel.fit(x_train, y_train)

svc_pred = SVCmodel.predict(x_test)
svc_acc = accuracy_score(svc_pred, y_test)
print("test accuracy: {:.2f}%".format(svc_acc*100))

print(confusion_matrix(y_test, svc_pred))
print("\n")
print(classification_report(y_test, svc_pred))

grid = {
    'C':[0.01, 0.1, 1, 10],
    'kernel':["linear","poly","rbf","sigmoid"],
    'degree':[1,3,5,7],
    'gamma':[0.01,1]
}
grid = GridSearchCV(SVCmodel, param_grid)
grid.fit(x_train, y_train)

y_pred = grid.predict(x_test)

logreg_acc = accuracy_score(y_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

logreg_acc = accuracy_score(y_pred, y_test)
print("Test accuracy: {:.2f}%".format(logreg_acc*100))

"""We see that support vector classifier performs slightly better than logistic regresion giving a better accuracy"""