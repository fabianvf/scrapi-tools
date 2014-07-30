from scrapi_tools import registry, lint
from scrapi_tools.document import RawDocument, NormalizedDocument
import datetime


def consume():
    # get my data somehow
    data = {
        'doc': "I sure am a document\nSome guy, some other guy\nExample\n7",
        'source': 'Example',
        'doc_id': '7',
        'filetype': 'ex',
    }
    return [RawDocument(data)]


def normalize(doc, timestamp):
    data = {
        'title': doc.get('doc').split('\n')[0],
        'source': doc.get('source'),
        'id': doc.get('doc_id'),
        'contributors': doc.get('doc').split('\n')[1].split(),
        'timestamp': datetime.datetime.now()
    }
    return NormalizedDocument(data)

registry.register('example', consume, normalize)

if __name__ == "__main__":
    print(lint(consume, normalize))
