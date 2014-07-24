#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from scrapi_tools.consumer import RawFile, NormalizedFile
from scrapi_tools.exceptions import MissingAttributeError
import datetime


class TestRawFile(unittest.TestCase):

    def test_legal(self):
        attributes = {
            'doc': 'A legal document',
            'doc_id': '7',
            'source': 'also 7',
            'filetype': 'supersmart'
        }
        try:
            raw_file = RawFile(attributes)
        except MissingAttributeError:
            assert False

        assert raw_file.get('doc') == 'A legal document'
        assert raw_file.get('doc_id') == '7'
        assert raw_file.get('source') == 'also 7'
        assert raw_file.get('filetype') == 'supersmart'

    def test_illegal(self):
        attributes = {
            'doc': 'A legal document',
            'source': 'also 7',
            'filetype': 'supersmart'
        }
        try:
            RawFile(attributes)
        except MissingAttributeError:
            assert True
            return
        assert False


class TestNormalizedFile(unittest.TestCase):

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
            normalized_file = NormalizedFile(attributes)
        except MissingAttributeError:
            assert False

        assert normalized_file.get('title') == attributes.get('title')
        assert normalized_file.get('id') == '7'
        assert normalized_file.get('source') == 'still 7'
        assert normalized_file.get('contributors') == ['all, literally', 'queen, of']
        assert normalized_file.get('timestamp') == attributes.get('timestamp')

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
            NormalizedFile(attributes)
        except MissingAttributeError:
            assert True
            return
        assert False
