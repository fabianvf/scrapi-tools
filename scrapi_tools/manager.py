import datetime
from document import NormalizedDocument, RawDocument


class _Registry(object):

    """
        A registry for consumers. It creates a dictionary with a service as the key,
        and a dictionary containing the two callables 'consume' and 'normalize'
        as the value. Registration fails if consume or normalize are not callable.
    """

    def __init__(self):
        self.consumers = {}

    def register(self, label, consume, normalize):

        if not callable(consume) or not callable(normalize):
            raise TypeError

        self.consumers[label] = {
            'consume': consume,
            'normalize': normalize,
        }

    def __getitem__(self, key):
        return self.consumers[key]


def lint(consume, normalize):
    """
        Runs the consume and normalize functions, ensuring that
        they match the requirements of scrAPI.
    """
    errors = {}
    output = consume()
    if not isinstance(output, list):
        errors.add("consume() does not return type list")
        return errors

    normalized_output = []
    for doc in output:
        if not isinstance(doc, RawDocument):
            errors.add("consume() does not return a list of type [RawDocument]")
        else:
            normalized_output.append(normalize(doc, datetime.datetime.now))

    for doc in normalized_output:
        if not isinstance(doc, NormalizedDocument):
            errors.add("normalize does not return type NormalizedDocument")
        else:
            try:
                title = doc.get("title")
                contributors = doc.get("contributors")
                id = doc.get("id")
                source = doc.get("source")
                if not isinstance(title, str):
                    errors.add("Normalize does not return a string for the title")
                if not isinstance(contributors, dict) or contributors.get("email") is None or contributors.get("full_name") is None:
                    errors.add("Normalize does not return contributors as a dictionary of {email: {EMAIL}, full_name: {FULL_NAME}}")
                if not isinstance(id, str):
                    errors.add("Normalize does not return a string for the unique identifier")
                if not isinstance(source, str):
                    errors.add("Normalize does not return a string for the source")
            except AttributeError:
                errors.add("Was not able to retrieve information from the NormalizedFile using '.get()'")
    return errors
