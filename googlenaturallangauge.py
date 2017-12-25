# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


class GoogleNaturalLanguage:

    def classify_request(self, text):
        # Instantiates a client
        client = language.LanguageServiceClient()

        # The text to analyze
        document = types.Document(
            content=text,
            type=language.enums.Document.Type.PLAIN_TEXT)

        # Detects the response of the text
        response = client.analyze_entities(document, encoding_type='UTF32', )

        for entity in response.entities:
            print(u'=' * 20)
            print('name: {0}'.format(entity.name))
            print('type: {0}'.format(entity.type))
            print('metadata: {0}'.format(entity.metadata))
            print('salience: {0}'.format(entity.salience))
