===========
scrAPI tools
===========

scrapi-tools provides a set of tools for interfacing with scrAPI. Currently,
these tools are focused on creating consumers and ensuring that those consumers
are compatible with the current iteration of scrAPI.

Typical usage looks like this:

__consumer.py__
```python
#!/usr/bin/env python

from scrapi_tools import lint
from scrapi_tool.document import RawDocument, NormalizedDocument


def consume():
    results = # Get stuff from your service
    return [RawDocument(result) for result in results]  # A list of RawDocuments

def normalize(raw_doc, timestamp):
    doc_attributes = # get stuff from raw_doc
    return NormalizedDocument(doc_attributes)

if __name__ == '__main__':
    lint(consume, normalize) 
```
lint will check the output of your consume and normalize functions,
ensuring that they are outputting documents of the correct type.


__\_\_init\_\_.py__
```python
from scrapi_tools import registry
from consumer import consume, normalize

registry.register('example', consume, normalize)

```

