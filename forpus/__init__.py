"""
Forpus is a Python library for processing plain text corpora to various corpus formats. In most cases, each NLP tool uses its own idiosyncratic input format. This library helps you to convert a corpus very easy to the desired format.

It is called Forpus, because you are **for**matting a cor**pus**, but this is also a genus of parrot in the family Psittacidae.

This library supports conversions to
* JSON
* Document-term matrix
* Graph
    * GEXF
    * GML
    * GraphML
    * Pajek
    * SparseGraph6
    * YAML
* David Blei's LDA-C
* Thorsten Joachims' SVMlight


Check out this example:

>>> from forpus import forpus
>>> corpus = forpus.Corpus(source='plaintext_corpus',
...                        target='formatted_corpus')
>>> corpus.to_json()

"""

from forpus.forpus import Corpus
