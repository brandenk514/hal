# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class GoogleNaturalLanguage:
    def __init__(self, text):
        # Instantiates a client
        self.client = language.LanguageServiceClient()

        # The text to analyze
        self.document = types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)

    def classify_request(self):

        # Detects the response of the text
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
            print(u'=' * 20)
            print('name: {0}'.format(entity.name))
            print('type: {0}'.format(entity.type))
            print('metadata: {0}'.format(entity.metadata))
            print('salience: {0}'.format(entity.salience))

    def analyze_syntax(self):

        # Detects the response of the text
        tokens = self.client.analyze_syntax(self.document, encoding_type='UTF32', ).tokens

        pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
                   'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

        for token in tokens:
            print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                                   token.text.content))
