# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import types


class GoogleNaturalLanguage:
    def __init__(self, text):
        # Instantiates a client
        self.client = language.LanguageServiceClient()

        # The text to analyze
        self.document = types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)

        self.classified_text = {}
        self.syntax_tokens = [()]

    def classify_request(self):

        """
        Take in a string and returns the classification of important entities
        :return:
        """

        # Detects the response of the text
        try:
            response = self.client.analyze_entities(self.document, encoding_type='UTF32', )

            """
            0 = 'UNKNOWN'
            1 = 'PERSON'
            2 = 'LOCATION'
            3 = 'ORGANIZATION'
            4 = 'EVENT'
            5 = 'WORK_OF_ART'
            6 = 'CONSUMER_GOOD'
            7 = 'OTHER'
            """

            for entity in response.entities:
                self.classified_text['name'] = entity.name
                self.classified_text['type'] = entity.type
                # print(self.classified_text)
            return self.classified_text
        except:
            print("Classification error")

    def analyze_syntax(self):
        """
        Takes in a string and returns the syntax from Google API
        :return:
        """

        # Detects the response of the text
        try:
            tokens = self.client.analyze_syntax(self.document, encoding_type='UTF32', ).tokens

            pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
                       'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

            for token in tokens:
                # print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag], token.text.content))
                self.syntax_tokens.append((pos_tag[token.part_of_speech.tag], token.text.content))
                # print(self.syntax_tokens)
                return self.syntax_tokens
        except:
            print("Analyzing syntax error")
