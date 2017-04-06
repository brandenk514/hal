from textblob.classifiers import NaiveBayesClassifier
from textblob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer
import random
import os
import formatter as f
import geonamescache as geo
import pickle
import time


class NaturalLanguage:
    def __init__(self):
        self.features_set = []
        self.application_tag = "application"
        self.timezone_tag = "timezone"
        self.location_tag = "location"
        self.weather_tomorrow_tag = "weather tomorrow"
        self.weather_tag = "weather"
        self.distance_tag = "distance"
        self.current_distance_from_tag = "distance from current loc"
        self.elevation_tag = "elevation"
        self.train_hal()

        random.shuffle(self.features_set)
        split = int(len(self.features_set)) - int(len(self.features_set) / 4)
        train_set, test_set = self.features_set[:split], self.features_set[split:]
        print("Full list: " + str(len(self.features_set)))
        print("Training set: " + str(len(train_set)))
        print("Test set: " + str(len(test_set)))

        t0 = time.time()
        if os.path.isfile('request_classifier.pickle'):
            self.classifier = self.load_classifier()
        else:
            print("training...")
            self.classifier = Blobber(analyzer=NaiveBayesAnalyzer(), classifier=NaiveBayesClassifier(train_set))
            print("Done")

        t1 = time.time()
        print("Training took: " + str(t1 - t0))  # ~294.56 -> ~0.25
        t2 = time.time()
        self.save_classifier(self.classifier)
        t3 = time.time()
        print("Classification took: " + str(t3-t2))  # ~98.47

    def classify_phrase(self, tb_phrase):
        print(self.classifier(tb_phrase).classify())
        return self.classifier(tb_phrase).classify()

    def train_hal(self):
        for app in os.listdir("/Applications/"):
            self.features_set.append(self.train_application_request(app))
            self.features_set.append(self.train_different_weather_request())
        for country in self.get_list_countries():
            self.features_set.append(self.train_location_request(country))
            self.features_set.append(self.train_timezone_request(country))
            self.features_set.append(self.train_distance_current_request(country))
            self.features_set.append(self.train_weather_request(country))
            self.features_set.append(self.train_weather_tomorrow_request(country))
            self.features_set.append(self.train_elevation_request(country))
            self.features_set.append(self.train_elevation_request_high(country))
            self.features_set.append(self.train_elevation_request_tall(country))
        for state in self.get_state_list():
            self.features_set.append(self.train_location_request(state))
            self.features_set.append(self.train_timezone_request(state))
            self.features_set.append(self.train_distance_current_request(state))
            self.features_set.append(self.train_weather_request(state))
            self.features_set.append(self.train_weather_tomorrow_request(state))
            self.features_set.append(self.train_elevation_request(state))
            self.features_set.append(self.train_elevation_request_high(state))
            self.features_set.append(self.train_elevation_request_tall(state))
        for i in range(0, len(self.get_state_list()) - 1):
            self.features_set.append(
                self.train_distance_request(self.get_state_list()[i], self.get_state_list()[i + 1]))
        for i in range(0, len(self.get_list_countries()) - 1):
            self.features_set.append(self.train_distance_request(self.get_list_countries()[i],
                                                                 self.get_list_countries()[i + 1]))

    def train_application_request(self, app):
        return "Open " + f.Formatter().remove_app_suffix(app), self.application_tag

    def train_location_request(self, location):
        return "Where is " + location, self.location_tag

    def train_weather_request(self, location):
        return "What is the weather in " + location, self.weather_tag

    def train_timezone_request(self, location):
        return "What timezone is " + location + "in", self.timezone_tag

    def train_weather_tomorrow_request(self, location):
        return "What is weather tomorrow in " + location, self.weather_tomorrow_tag

    def train_distance_request(self, location_from, location_to):
        return "What is the distance between " + location_from + " and " + location_to, self.distance_tag

    def train_distance_current_request(self, location_to):
        return "How far it is to " + location_to, self.current_distance_from_tag

    def train_elevation_request(self, location):
        return "What is the elevation of " + location, self.elevation_tag

    def train_elevation_request_tall(self, location):
        return "How tall is " + location, self.elevation_tag

    def train_elevation_request_high(self, location):
        return "How high is " + location, self.elevation_tag

    def train_different_weather_request(self):
        request = [
            ("Will it rain tomorrow", self.weather_tomorrow_tag),
            ("Is it going to rain tomorrow", self.weather_tomorrow_tag),
            ("Will it be sunny tomorrow", self.weather_tomorrow_tag),
            ("Is it cold outside", self.weather_tag),
            ("What is the weather", self.weather_tag),
            ("What is the weather today", self.weather_tag),
            ("How cold is it outside", self.weather_tag),
            ("How hot is it going to bree today", self.weather_tag),
            ("What is the weather tomorrow", self.weather_tomorrow_tag),
            ("What is the weather like today", self.weather_tag),
        ]
        i = random.randint(0, len(request) - 1)
        return request[i]

    def get_list_countries(self):
        gc = geo.GeonamesCache().get_countries_by_names()
        countries = []
        for key in gc.keys():
            countries.append(key)
        return countries

    def get_state_list(self):
        gc = geo.GeonamesCache().get_us_states_by_names()
        states = []
        for key in gc.keys():
            states.append(key)
        return states

    def save_classifier(self, classifier):
        file = open('request_classifier.pickle', 'wb')
        pickle.dump(classifier, file, -1)
        file.close()

    def load_classifier(self):
        file = open('request_classifier.pickle', 'rb')
        classifier = pickle.load(file)
        file.close()
        return classifier

if __name__ == '__main__':
    nl = NaturalLanguage()
    nl.classify_phrase("What is the weather in San Antonio")
