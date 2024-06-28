from keras.datasets import imdb
from keras import models, layers
import numpy as np

class neuralnet:
    def __init__(self, model_path, num_words=10000):
        self.num_words = num_words
        self.model = models.load_model(model_path)
        self.word_index = imdb.get_word_index()
    
    def preprocess_sentence(self, sentence):
        words = sentence.lower().split()
        tokenized = [self.word_index.get(word, 2) for word in words]  # 2 is the index for 'unknown' words
        tokenized = [index if index < self.num_words else 2 for index in tokenized]  # Ensure num_words limit
        return tokenized
    
    def vectorize_sequence(self, sequence):
        result = np.zeros((1, self.num_words))
        result[0, sequence] = 1.
        return result
    
    def predict_sentiment(self, sentence):
        tokenized_sentence = self.preprocess_sentence(sentence)
        vectorized_sentence = self.vectorize_sequence(tokenized_sentence)
        prediction = self.model.predict(vectorized_sentence)
        return prediction[0][0]