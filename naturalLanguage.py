from textblob.classifiers import NaiveBayesClassifier
import textblob
import random
import formatter
import geonamescache as geo
import pickle
import os


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
        self.system_tag = "system"
        self.name_tag = "name"
        self.train_hal()

        random.shuffle(self.features_set)
        split = int(len(self.features_set)) - int(len(self.features_set) / 4)
        train_set, test_set = self.features_set[:split], self.features_set[split:]
        if os.path.isfile('request_classifier.pickle'):
            self.classifier = self.load_classifier()  # Load classifier so training does not have to occur on every run
        else:
            print(len(self.features_set))
            print("Training...")
            self.classifier = NaiveBayesClassifier(train_set)
            print(self.classifier.accuracy(test_set))
            print("Done")
        self.save_classifier(self.classifier)

    def classify_phrase(self, tb_phrase):
        """
        Classifies a string
        :param tb_phrase: 
        :return: 
        """
        return self.classifier.classify(tb_phrase)

    def classifier_prob(self, phrase, classification):
        """
        Returns the probability of a string being classified as a given classification
        :param phrase: 
        :param classification: 
        :return: 
        """
        return self.classifier.prob_classify(phrase).prob(classification)

    def train_hal(self):
        """
        Creates a feature set for HAl to train on using location from the geonamescache package 
        :return: 
        """
        for app in os.listdir("/Applications/"):
            self.features_set.append(self.train_application_request(app))
        for i in range(0, len(self.get_state_list()) - 1):
            self.features_set.append(
                self.train_distance_request(self.get_state_list()[i], self.get_state_list()[i + 1]))
        for i in range(0, len(self.get_list_countries()) - 1):
            self.features_set.append(self.train_distance_request(self.get_list_countries()[i],
                                                                 self.get_list_countries()[i + 1]))
            self.features_set.append(self.train_distance_request_from(self.get_list_countries()[i],
                                                                      self.get_list_countries()[i + 1]))
        # for n in self.get_people_names():
        # self.features_set.append(self.train_names(n))
        for country in self.get_list_countries():
            self.features_set.append(self.train_location_request(country))
            self.features_set.append(self.train_timezone_request(country))
            self.features_set.append(self.train_distance_current_request(country))
            self.features_set.append(self.train_weather_request(country))
            self.features_set.append(self.train_weather_like_tomorrow_request(country))
            self.features_set.append(self.train_weather_tomorrow_request(country))
            self.features_set.append(self.train_elevation_request(country))
            self.features_set.append(self.train_elevation_request_high(country))
            self.features_set.append(self.train_elevation_request_tall(country))
            self.features_set.append(self.train_time_request(country))
            self.features_set.append(self.train_time_request2(country))
            self.features_set.append(self.train_time_distance_request(country))
            for i in self.train_different_phrased_request():
                self.features_set.append(i)

    def train_application_request(self, app):
        return "open " + formatter.Formatter().remove_app_suffix(app), self.application_tag

    def train_location_request(self, location):
        return "where is " + location, self.location_tag

    def train_weather_request(self, location):
        return "what is the weather in " + location, self.weather_tag

    def train_timezone_request(self, location):
        return "what time zone is " + location + " in", self.timezone_tag

    def train_time_request2(self, location):
        return "what is the time in " + location, self.timezone_tag

    def train_time_request(self, location):
        return "what time is it in " + location, self.timezone_tag

    def train_weather_tomorrow_request(self, location):
        return "what is weather tomorrow in " + location, self.weather_tomorrow_tag

    def train_weather_like_tomorrow_request(self, location):
        return "what is weather tomorrow in " + location + " like", self.weather_tomorrow_tag

    def train_distance_request(self, location_from, location_to):
        return "what is the distance between " + location_from + " and " + location_to, self.distance_tag

    def train_distance_request_from(self, location_from, location_to):
        return "what is the distance from " + location_from + " to " + location_to, self.distance_tag

    def train_distance_current_request(self, location_to):
        return "how far it is to " + location_to, self.current_distance_from_tag

    def train_time_distance_request(self, location_to):
        return "how long will it take to get to " + location_to, self.current_distance_from_tag

    def train_elevation_request(self, location):
        return "what is the elevation of " + location, self.elevation_tag

    def train_elevation_request_tall(self, location):
        return "how tall is " + location, self.elevation_tag

    def train_elevation_request_high(self, location):
        return "how high is " + location, self.elevation_tag

    def train_names(self, name):
        i = random.randint(0, 1)
        if i == 0:
            return "my name is " + name, self.name_tag
        else:
            return "you can call me " + name, self.name_tag

    def train_different_phrased_request(self):
        request = [
            ("will it rain tomorrow", self.weather_tomorrow_tag),
            ("is it going to rain tomorrow", self.weather_tomorrow_tag),
            ("will it be sunny tomorrow", self.weather_tomorrow_tag),
            ("is it cold outside", self.weather_tag),
            ("what is the weather", self.weather_tag),
            ("what is the weather today", self.weather_tag),
            ("how cold is it outside", self.weather_tag),
            ("how hot is it going to be today", self.weather_tag),
            ("what is the weather tomorrow", self.weather_tomorrow_tag),
            ("what is the weather like today", self.weather_tag),
            ("what timezone am I in", self.timezone_tag),
            ("what time is it", self.timezone_tag),
            ("what is the temperature", self.weather_tag),
            ("where am I?", self.location_tag),
            ("what is my name?", self.name_tag)
        ]
        # i = random.randint(0, len(request) - 1)
        return request  # [i]

    @staticmethod
    def get_list_countries():
        gc = geo.GeonamesCache().get_countries_by_names()
        countries = []
        for key in gc.keys():
            countries.append(key)
        return countries

    @staticmethod
    def get_state_list():
        gc = geo.GeonamesCache().get_us_states_by_names()
        states = []
        for key in gc.keys():
            states.append(key)
        return states

    @staticmethod
    def save_classifier(classifier):
        """
        Takes in a classifier and pickle it
        :param classifier: 
        :return: 
        """
        file = open('request_classifier.pickle', 'wb')
        pickle.dump(classifier, file, -1)
        file.close()

    @staticmethod
    def load_classifier():
        """
        Load a classifier from a pickle to speed up training
        :return: 
        """
        try:
            file = open('request_classifier.pickle', 'rb')
            classifier = pickle.load(file)
            file.close()
            return classifier
        except EOFError:
            return "An error occurred while loading the classifier"

    @staticmethod
    def phrase_to_textblob(phrase):
        return textblob.TextBlob(phrase).tags

    @staticmethod
    def find_location(textblob_phrase):
        """
        Takes in a tagged textblob phrase 
        :param textblob_phrase: 
        :return: the location with "NNP" or "VB" tagged to it
        """
        location = []
        for p in textblob_phrase:
            if p[1] == "NNP" or p[1] == "VB":
                location.append(p[0])
        return " ".join(location)

    @staticmethod
    def get_people_names():
        with open('names.txt', 'r') as f:
            names = [line.strip().capitalize() for line in f]
        return names

    @staticmethod
    def get_name(text_blob_phrase):
        """
        Takes in a tagged textblob phrase 
        :param text_blob_phrase: 
        :return: the word with "NNP" tagged to it
        """

        if len(text_blob_phrase) == 1:
            for p in text_blob_phrase:
                return p[0]
        else:
            for p in text_blob_phrase:
                if p[1] == "NNP":
                    return p[0]
