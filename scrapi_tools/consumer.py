#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    A collection of handy classes for writing consumers
"""
from exceptions import MissingAttributeError
import datetime


class BaseConsumer(object):

    """
        A basic consumer, containing the basic structure required
        for a scrAPI consumer. When writing a consumer, you should
        subclass this.
    """

    def __init__(self):
        raise NotImplementedError

    def consume(self):
        """
            :: -> [RawFile]
        """
        raise NotImplementedError

    def normalize(self, raw_file, timestamp):
        """
            :: ( RawFile, DateTime ) -> NormalizedFile
        """
        raise NotImplementedError

    def lint(self):
        """
            Runs the consume and normalize functions, ensuring that
            they match the requirements of scrAPI.
        """
        errors = []
        output = self.consume()
        if not isinstance(output, list):
            errors.append("consume() does not return type list")
            return errors

        normalized_output = []
        for doc in output:
            if not isinstance(output, RawFile):
                errors.append("consume() does not return a list of type [RawFile]")
            else:
                normalized_output.append(self.normalize(doc, datetime.datetime.now))

        for doc in normalized_output:
            if not isinstance(doc, NormalizedFile):
                errors.append("normalize does not return type NormalizedFile")
        return errors


class RawFile(object):

    """
        For raw file objects. Automatically lints input to ensure
        compatibility with scrAPI.
    """

    def __init__(self, attributes):
        self.REQUIRED_FIELDS = ['doc', 'doc_id', 'source', 'filetype']

        if None in [attributes.get(field) for field in self.REQUIRED_FIELDS]:
            raise MissingAttributeError("RawFile object can not be created because a required"
                                        " field is not present. \n\tRequired fields are {0}"
                                        "\n\tGiven fields are {1}".format(self.REQUIRED_FIELDS, attributes.keys()))
        self.attributes = attributes

    def get(self, attribute):
        """
            Maintains compatibility with previous dictionary implementation of scrAPI
            :: str -> str
        """
        return self.attributes.get(attribute)


class NormalizedFile(object):

    """
        For normalized file objects. Automatically lints input to
        ensure comaptibility with scrAPI.
    """

    def __init__(self, attributes):
        self.REQUIRED_FIELDS = ['title', 'contributors', 'id', 'source', 'timestamp']

        if None in [attributes.get(field) for field in self.REQUIRED_FIELDS]:
            raise MissingAttributeError("NormalizedFile object can not be created because a required"
                                        " field is not present. \n\tRequired fields are {0}"
                                        "\n\tGiven fields are {1}".format(self.REQUIRED_FIELDS, attributes.keys()))

        self.attributes = attributes

    def get(self, attribute):
        """
            Maintains compatibility with previous dictionary implementation of scrAPI
            :: str -> (str | [str])
        """
        return self.attributes.get(attribute)
