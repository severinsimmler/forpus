![Logo](docs/images/logo.png)

[![Build Status](https://travis-ci.org/severinsimmler/forpus.svg?branch=master)](https://travis-ci.org/severinsimmler/forpus)


[Forpus](https://severinsimmler.github.io/forpus) is a Python library for processing plain text corpora to various corpus formats. In most cases, each NLP tool uses its own idiosyncratic input format. This library helps you to convert a corpus very easy to the desired format.

> It is called Forpus, because you are **for**matting a cor**pus**, but this is also a genus of parrot in the family Psittacidae.

This library supports **conversions** to
* [JSON](https://www.json.org/index.html)
* [Document-term matrix](https://en.wikipedia.org/wiki/Document-term_matrix)
* Graph
    * [GEXF](https://gephi.org/gexf/format/)
    * [GML](https://gephi.org/users/supported-graph-formats/gml-format/)
    * [GraphML](http://graphml.graphdrawing.org/)
    * [Pajek](http://vlado.fmf.uni-lj.si/pub/networks/pajek/)
    * [SparseGraph6](https://networkx.github.io/documentation/networkx-1.10/reference/readwrite.sparsegraph6.html)
    * [YAML](http://yaml.org/)
* David Blei's [LDA-C](https://github.com/blei-lab/lda-c/blob/master/readme.txt)
* Thorsten Joachims' [SVM<sup>light<sup>](http://svmlight.joachims.org/)

## Requirements
Forpus requires **Python 3.6** and some additional libraries:
* `pandas`, at least v0.21.1.
* `networkx`, at least v2.0.
* `metadata-toolbox`, at least v0.1.

See [Getting Started](https://severinsimmler.github.io/forpus/gettingstarted.html) for how to install Forpus.

## Resources
* [Forpus website](https://severinsimmler.github.io/forpus)
* [Forpus API documentation](https://severinsimmler.github.io/forpus/gen/forpus.html)
* [Forpus tutorial](https://github.com/severinsimmler/forpus/blob/master/notebooks/A%20Walk%20Through%20Forpus.ipynb)
