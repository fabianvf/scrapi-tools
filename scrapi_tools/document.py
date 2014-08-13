from exceptions import MissingAttributeError


class BaseDocument(object):

    """
        For file objects. Automatically lints input to ensure
        compatibility with scrAPI.
    """

    REQUIRED_FIELDS = set()

    def __init__(self, attributes):

        if None in [attributes.get(field) for field in self.REQUIRED_FIELDS]:
            raise MissingAttributeError(
                "{cls} object can not be created because a required"
                " field is not present. \n\tRequired fields are {fields}"
                "\n\tGiven fields are {given}"
                "\n\tMissing fields are: {missing}"
                .format(
                    fields=self.REQUIRED_FIELDS,
                    given=attributes.keys(),
                    cls=self.__class__.__name__,
                    missing=list(self.REQUIRED_FIELDS.difference(set(attributes.keys())))
                )
            )
        self.attributes = attributes

    def get(self, attribute):
        """
            Maintains compatibility with previous dictionary implementation of scrAPI
            :: str -> str
        """
        return self.attributes.get(attribute)


class RawDocument(BaseDocument):

    REQUIRED_FIELDS = set(['doc', 'doc_id', 'source', 'filetype'])


class NormalizedDocument(BaseDocument):

    REQUIRED_FIELDS = set(['title', 'contributors', 'id', 'source', 'timestamp', 'description', 'tags', 'date_created'])

    def __init__(self, attributes):
        BaseDocument.__init__(self, attributes)

        for _id in attributes.get('id').keys():
            attributes['id'][_id] = str(attributes['id'][_id])

        if not isinstance(self.get('tags'), list):
            raise TypeError("self.attributes['tags']: Expected <type 'list'>, received {}".format(type(self.get('tags'))))

        if not isinstance(self.get('contributors'), list):
            raise TypeError("self.attributes['contributors']: Expected <type 'list'>, received {}".format(type(self.get('contributors'))))
        elif not isinstance(self.get('contributors')[0], dict):
            raise TypeError("self.attributes['contributors'][0]: Expected <type 'dict'>, received {}".format(type(self.get('contributors')[0])))

        if not isinstance(self.get('id'), dict):
            raise TypeError("self.attributes['id']: Expected <type 'dict'>, received {}".format(type(self.get('id'))))
