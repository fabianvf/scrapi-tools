#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from scrapi_tools.document import RawDocument, NormalizedDocument
from scrapi_tools.exceptions import MissingAttributeError
import datetime


class TestRawDocument(unittest.TestCase):

    def test_legal(self):
        attributes = {
            'doc': 'A legal document',
            'doc_id': '7',
            'source': 'also 7',
            'filetype': 'supersmart'
        }
        try:
            raw_doc = RawDocument(attributes)
        except MissingAttributeError:
            assert False

        assert raw_doc.get('doc') == 'A legal document'
        assert raw_doc.get('doc_id') == '7'
        assert raw_doc.get('source') == 'also 7'
        assert raw_doc.get('filetype') == 'supersmart'

    def test_illegal(self):
        attributes = {
            'doc': 'A legal document',
            'source': 'also 7',
            'filetype': 'supersmart'
        }
        try:
            RawDocument(attributes)
        except MissingAttributeError:
            assert True
            return
        assert False


class TestNormalizedDocument(unittest.TestCase):

    def test_legal(self):
        attributes = {
            'title': 'My super important research project',
            'contributors': ['all, literally', 'queen, of'],
            'id': '7',
            'properties': {
            },
            'source': 'still 7',
            'timestamp': str(datetime.datetime.now())
        }
        try:
            normalized_doc = NormalizedDocument(attributes)
        except MissingAttributeError:
            assert False

        assert normalized_doc.get('title') == attributes.get('title')
        assert normalized_doc.get('id') == '7'
        assert normalized_doc.get('source') == 'still 7'
        assert normalized_doc.get('contributors') == ['all, literally', 'queen, of']
        assert normalized_doc.get('timestamp') == attributes.get('timestamp')

    def test_illegal(self):
        attributes = {
            'title': 'My super important research project',
            'contributors': ['all, literally', 'queen, of'],
            'properties': {
            },
            'source': 'still 7',
            'timestamp': str(datetime.datetime.now())
        }
        try:
            NormalizedDocument(attributes)
        except MissingAttributeError:
            assert True
            return
        assert False
