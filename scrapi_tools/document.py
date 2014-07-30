from exceptions import MissingAttributeError


class BaseDocument(object):

    """
        For file objects. Automatically lints input to ensure
        compatibility with scrAPI.
    """

    REQUIRED_FIELDS = []

    def __init__(self, attributes):

        if None in [attributes.get(field) for field in self.REQUIRED_FIELDS]:
            raise MissingAttributeError("{2} object can not be created because a required"
                                        " field is not present. \n\tRequired fields are {0}"
                                        "\n\tGiven fields are {1}".format(self.REQUIRED_FIELDS, attributes.keys(), self.__class__.__name__))
        self.attributes = attributes

    def get(self, attribute):
        """
            Maintains compatibility with previous dictionary implementation of scrAPI
            :: str -> str
        """
        return self.attributes.get(attribute)


class RawDocument(BaseDocument):

    REQUIRED_FIELDS = ['doc', 'doc_id', 'source', 'filetype']


class NormalizedDocument(BaseDocument):

    REQUIRED_FIELDS = ['title', 'contributors', 'id', 'source', 'timestamp']
