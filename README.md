===========
scrAPI tools
===========

scrapi-tools provides a set of tools for interfacing with scrAPI. Currently,
these tools are focused on creating consumers and ensuring that those consumers
are compatible with the current iteration of scrAPI.

Typical usage looks like this:
```python
    #!/usr/bin/env python

    from scrapi-tools.consumers import BaseConsumer, RawFile, NormalizedFile


    class MyServiceConsumer(BaseConsumer):

        def __init__(self):
        # Do stuff

        def consume(self):
            results = # Get stuff from your service
            return [RawFile(result) for result in results]

        def normalize(self, raw_doc, timestamp):
            doc_attributes = # Do stuff to raw_doc
            return NormalizedFile(doc_attributes)


    my_object = MyServiceConsumer()
    my_object.lint()
```
This will check the output of your consume and normalize functions,
ensuring that they are outputting documents of the correct type.
