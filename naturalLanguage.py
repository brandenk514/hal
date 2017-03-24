from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob


class NaturalLanguage:
    def __init__(self):
        # self.classifier = NaiveBayesClassifier()
        feature_set = []

    def train_hal(self):
        weather_tag = "weather"
        location_tag = "location"
        train = [
            ("What is the weather?", weather_tag),
            ("What is the weather in Baltimore?", weather_tag),
            ("What is the weather in Copenhagen, Denmark tomorrow?", weather_tag),
            ("What is the weather in San Antonio?", weather_tag),
            ("Is it going to rain today?", weather_tag),
            ("Is it going to rain tomorrow?", weather_tag),
            ("Where is Morocco?", location_tag),
            ("Where is Copenhagen?", location_tag),
            ("where is Texas?", location_tag),
            ("Where is Denver?", location_tag),
            ("Where is Mount Everest?", location_tag),
            ("Where is Baltimore?", location_tag)
        ]

        test = [
            ('Where is Denmark?', location_tag),
            ("What is the weather tomorrow?", weather_tag),
            ("What is the weather in Scotland?", weather_tag),
            ("Where is Nova Scotia?", location_tag),
            ("Where is Canada?", location_tag),
            ("Will it rain tomorrow?", weather_tag)
        ]

        cl = NaiveBayesClassifier(train)

        print(cl.classify("Is it going to rain next week?"))
        print(cl.classify("Where is India?"))

        print(cl.accuracy(test))


if __name__ == '__main__':
    nl = NaturalLanguage()
    nl.train_hal()
