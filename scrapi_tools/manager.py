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
            try:
                normalized_output.append(normalize(doc, datetime.datetime.now()))
            except Exception as e:
                errors.add(e)

    for doc in normalized_output:
        if not isinstance(doc, NormalizedDocument):
            errors.add("normalize does not return type NormalizedDocument")
        else:
            try:
                errors = _check_values(doc, errors)
            except AttributeError as e:
                errors.add(str(e))
                errors.add("Was not able to retrieve information from the NormalizedFile using '.get()'")

    return return_string(errors)


def _check_values(doc, errors):
    title = doc.get("title")
    contributors = doc.get("contributors")
    _id = doc.get("id")
    source = doc.get("source")
    if not isinstance(title, str) and not isinstance(title, unicode):
        errors.add("Normalize does not return a string for the title, returned {} instead".format(type(title)))
    if not isinstance(contributors, list):
        errors.add("Normalize does not return contributors as a list, returns type {} instead".format(type(contributors)))
    else:
        for contributor in contributors:
            try:
                if contributor.get("email") is None or contributor.get("full_name") is None:
                    errors.add("Normalize does not return contributors as a list of dict(email: EMAIL, full_name: FULL_NAME)."
                               " Has type [{}] instead".format(type(contributor)))
            except AttributeError:
                errors.add("Normalize does not return contributors as a list of dict(email: EMAIL, full_name: FULL_NAME)."
                           " Has type [{}] instead".format(type(contributor)))

    if not isinstance(_id, dict) or not _id.get('service_id') or not _id.get('url'):
        errors.add("Normalize does not return a dict with a service id and url for the unique identifier,"
                   "returned {_type} with service_id: {sid} and url: {url} instead".format(_type=type(_id), sid=_id.get('service_id'), url=_id.get('url')))
    if not isinstance(source, str) and not isinstance(_id, unicode):
        errors.add("Normalize does not return a string for the source, returned {} instead".format(type(source)))
    return errors


def return_string(errors):
    return_string = '' if len(errors) > 0 else "No errors encountered!"
    for error in list(errors):
        return_string += str(error) + '\n'

    return return_string
