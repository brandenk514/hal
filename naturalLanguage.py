from textblob.classifiers import NaiveBayesClassifier
import random


class NaturalLanguage:
    def __init__(self):
        self.features_set = self.train_hal()
        random.shuffle(self.features_set)
        split = int(len(self.features_set)) - int(len(self.features_set) / 4)
        train_set, test_set = self.features_set[:split], self.features_set[split:]
        print(len(train_set))
        print(len(test_set))
        self.classifier = NaiveBayesClassifier(train_set)
        print(self.classifier.accuracy(test_set))

    def classify_phrase(self, phrase):
        classified = self.classifier.classify(phrase)
        phrase_tuple = (phrase, classified)
        if phrase_tuple not in self.features_set:
            self.features_set.append(phrase_tuple)
        print(classified)
        return classified

    def train_hal(self):
        weather_tag = "weather"
        location_tag = "location"
        elevation_tag = "elevation"
        distance_tag = "distance"
        timezone_tag = "timezone"
        application_tag = "application"
        return [
            ("What is the weather", weather_tag),
            ("What is the weather in Baltimore", weather_tag),
            ("What is the weather in Copenhagen, Denmark tomorrow", weather_tag),
            ("What is the weather in San Antonio", weather_tag),
            ("Is it going to rain today", weather_tag),
            ("Is it going to rain tomorrow", weather_tag),
            ("Where is Morocco", location_tag),
            ("Where is Copenhagen", location_tag),
            ("where is Texas", location_tag),
            ("Where is Denver", location_tag),
            ("Where is Mount Everest", location_tag),
            ("Where is Baltimore", location_tag),
            ('Where is Denmark', location_tag),
            ("What is the weather tomorrow", weather_tag),
            ("What is the weather in Scotland", weather_tag),
            ("Where is Nova Scotia", location_tag),
            ("Where is Canada", location_tag),
            ("Will it rain tomorrow", weather_tag),
            ("How tall is mount Everest", elevation_tag),
            ("What is the elevation of baltimore", elevation_tag),
            ("How far is it to California", distance_tag),
            ("What is the distance between New York and Los Angeles", distance_tag),
            ("What timezone am I in", timezone_tag),
            ("Open Safari", application_tag),
            ("Open Notes", application_tag),
            ("Open Disk Utility", application_tag),
            ("What is the distance to D.C.", distance_tag),
            ("Will it be sunny tomorrow", weather_tag),
            ("How cold is it outside", weather_tag),
            ("Where is the Statue of Liberty", location_tag),
            ("Where am I", location_tag),
            ("What is the weather today", weather_tag),
            ("What is the weather tomorrow", weather_tag),
            ("How far is it to Disney World", distance_tag),
            ("How far is it to Disney Land", distance_tag),
            ("What is the distance to San Antonio", distance_tag),
            ("How high is Matterhorn", elevation_tag),
            ("How tall is the Empire State Building", elevation_tag),
            ("Open Unity", application_tag),
            ("What is the elevation of Baltimore", elevation_tag),
            ("What is the elevation of Moscow", elevation_tag),
            ("What time is Baltimore in", timezone_tag),
            ("What timezone is Russia in", timezone_tag),
            ("What timezone is Mexico City in", timezone_tag),
            ("What timezone is Atlanta in", timezone_tag),
        ]

if __name__ == '__main__':
    nl = NaturalLanguage()
    nl.classify_phrase("What timezone is California in")
