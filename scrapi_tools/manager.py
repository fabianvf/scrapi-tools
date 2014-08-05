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
    errors = set()
    output = consume()
    if len(output) == 0:
        errors.add("consume() returned an empty list")
    if not isinstance(output, list):
        errors.add("consume() does not return type list")
        return errors

    normalized_output = []
    for doc in output:
        if not isinstance(doc, RawDocument):
            errors.add("consume() does not return a list of type [RawDocument]")
        else:
            normalized_output.append(normalize(doc, datetime.datetime.now()))

    for doc in normalized_output:
        if not isinstance(doc, NormalizedDocument):
            errors.add("normalize does not return type NormalizedDocument")
        else:
            try:
                errors = _check_values(doc, errors)
            except AttributeError:
                errors.add("Was not able to retrieve information from the NormalizedFile using '.get()'")
    return errors


def _check_values(doc, errors):
    title = doc.get("title")
    contributors = doc.get("contributors")
    id = doc.get("id")
    source = doc.get("source")
    if not isinstance(title, str) and not isinstance(title, unicode):
        errors.add("Normalize does not return a string for the title, returned {} instead".format(type(title)))
    if not isinstance(contributors, list):
        errors.add("Normalize does not return contributors as a list, returns type {} instead".format(type(contributors)))
    else:
        for contributor in contributors:
            if contributor.get("email") is None or contributor.get("full_name") is None:
                errors.add("Normalize does not return contributors as a list of dict(email: EMAIL, full_name: FULL_NAME)."
                           " Has type [{}] instead".format(type(contributor)))
    if not isinstance(id, str) and not isinstance(id, unicode):
        errors.add("Normalize does not return a string for the unique identifier, returned {} instead".format(type(id)))
    if not isinstance(source, str) and not isinstance(id, unicode):
        errors.add("Normalize does not return a string for the source, returned {} instead".format(type(source)))
    return errors
