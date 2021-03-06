from pathlib import Path
import json
from collections import Counter
import pandas as pd
import networkx as nx
from metadata_toolbox.utils import fname2metadata


class Corpus(object):
    """Converts a plain text corpus into a NLP-specific corpus format.

    Construct this class, if you have a directory of plain text files (.txt),
    and want to convert the content of those files into a NLP-specific corpus
    format. In most cases, each NLP tool uses its own idiosyncratic input
    format. This class helps you to convert a corpus very easy to the desired
    format.

    This class does not store the whole corpus at once in RAM, which is useful
    when handling very large corpora. Documents are streamed from disk in a
    lazy fashion, one document at a time, and closed before the next one is
    opened. Have a look at :meth:`stream_corpus`, if you are interested in how
    this is implemented.

    There is a plenty of formats available:
        * JSON, see :meth:`to_json`
        * Document-term matrix, see :meth:`to_document_term_matrix()`
        * Graph, see :meth:`to_graph`
            * GEXF
            * GML
            * GraphML
            * Pajek
            * SparseGraph6
            * YAML
        * David Blei's LDA-C, see :meth:`to_ldac()`
        * Thorsten Joachims' SVMlight, see :meth:`to_svmlight()`

    Once instantiated, you can convert the corpus **only once**. The concept of
    this library is to construct **one class for each target format**. For
    example:

    >>> CorpusJSON = Corpus(source='corpus', target='corpus_json')
    >>> CorpusJSON.to_json()
    >>> CorpusTEI = Corpus(source='corpus', target='corpus_tei')
    >>> CorpusTEI.to_tei()

    and so on...

    This should **help you** to keep an overview and avoid storing all kind of
    different corpus formats in the same directory.

    Args:
        source (:obj:`str`): The path to the corpus directory. This can be an
            absolute or relative path.
        target (:obj:`str`): The path to the output directory. Same as above,
            either an absolute or relative path.
        fname_pattern (:obj:`str`, optional): The pattern of the corpus's
            filenames. Metadata wil be extracted from the filenames based on
            this pattern. If the pattern is ``None`` or does not match the
            structure, only the basename (without suffix) will be considered as
            metadata. An example for the filename ``parsons_social.txt`` would
            be ``{author}_{title}``. ``parsons`` will be recognized as author,
            ``social`` as the title.

    Attributes:
        source (:obj:`str`): The path to the corpus directory. This can be an
            absolute or relative path.
        target (:obj:`str`): The path to the output directory. Same as above,
            either an absolute or relative path.
        pattern (:obj:`str`, optional): The pattern of the corpus's filenames.
            Metadata wil be extracted from the filenames based on this pattern.
            If the pattern is ``None`` or does not match the structure, only
            the basename (without suffix) will be considered as metadata. An
            example for the filename ``parsons_social.txt`` would be
            ``{author}_{title}``. ``parsons`` will be recognized as author,
            ``social`` as the title.
        corpus (:obj:`iterable`): This is an iterable of ``(metadata, text)``.
            ``metadata`` is a :obj:`pandas.DataFrame` containing metadata
            extracted from the filename. ``text`` is the content of the file as
            :obj:`str`.

    """
    def __init__(self, source, target, fname_pattern='{author}_{title}'):
        """Instatiates :class:`Corpus`.

        This method instatiates all objects of the class :class:`Corpus`. There
        are only few arguments to pass. Have a look at the docstring of
        :class:`Corpus` for more details.

        """
        self.source = source
        self.pattern = fname_pattern
        self.corpus = self.stream_corpus()
        self.target = Path(target)
        if not self.target.exists():
            self.target.mkdir()

    def stream_corpus(self):
        """Streams a text corpus from disk.

        This method is used to instantiate the :obj:`corpus`. Each file in the
        directory :obj:`source` will be opened and yielded in a for loop.

        Yields:
            A tuple of ``(metadata, text)``. ``metadata`` is a pandas DataFrame
            containing metadata extracted from the filename. ``text`` is the
            content of the file as :obj:`str`.

        """
        p = Path(self.source)
        for file in p.glob('*.txt'):
            with file.open('r', encoding='utf-8') as document:
                fname = str(file)
                try:
                    metadata = fname2metadata(fname, self.pattern)
                except ValueError:
                    metadata = pd.DataFrame([file.stem], columns=['stem'], index=[fname])
                yield metadata, document.read()

    def to_json(self, onefile=True):
        """Converts the corpus into JSON.

        **JSON** (JavaScript Object Notation) is a lightweight data-interchange
        format. It is easy for humans to read and write. It is easy for
        machines to parse and generate. For more information on this format,
        follow `this link <https://www.json.org/index.html>`_.

        This method converts your plain text corpus to JSON. Besides the
        content of your documents, **metadata will be included** in the JSON.
        Have a look at the basic description of :class:`Corpus` for proper
        metadata recognition.

        You have **two options**:
            1. In case you want to write the whole corpus into one single file,
            set the parameter ``onefile`` to True. **Be aware, the whole corpus
            will be in RAM**.

            2. If ``onefile`` is False, there will be one JSON file for each
            document.

        Args:
            onefile (:obj:`bool`): If True, write the whole corpus in one file.
                Otherwise each document will be written to single files.

        Returns:
            None, but writes the formatted corpus to disk.

        """
        if onefile:
            corpus_json = dict()
        for meta, text in self.corpus:
            stem = Path(meta.index[0]).stem
            document_json = meta.to_dict('record')[0]
            document_json['text'] = text
            if onefile:
                corpus_json[stem] = document_json
            else:
                document_json['stem'] = stem
                p = Path(self.target, stem + '.json')
                with p.open('w', encoding='utf-8') as file:
                    json.dump(document_json, file)
        if onefile:
            p = Path(self.target, 'corpus.json')
            with p.open('w', encoding='utf-8') as file:
                json.dump(corpus_json, file)

    def to_document_term_matrix(self, tokenizer, counter, **preprocessing):
        """Converst the corpus into a document-term matrix.

        A **document-term matrix** or term-document matrix is a mathematical
        matrix that describes the frequency of terms that occur in a collection
        of documents. In a document-term matrix, rows correspond to documents
        in the collection and columns correspond to terms.

        Args:
            tokenizer (:obj:`function`): This must be a function for
                tokenization. You could use a simple regex function or from
                `NLTK <http://www.nltk.org>`_.
            counter (:obj:`function`): This must be a function which counts
                elements of an iterable. There are various schemes for
                determining the value that each entry in the matrix should
                take. One such scheme is
                `tf-idf <https://en.wikipedia.org/wiki/Tf-idf>`_. But you can
                simply use the :class:`Counter` provided in the Python
                standard library.
            \*\*preprocessing (:obj:`function`, optional): This can be one or
                even more functions which take the output of your tokenizer
                function as input. So, you could write a function which counts
                the terms in your corpus and removes the 100 most frequent
                words.

        Returns:
            None, but writes the formatted corpus to disk.

        """
        document_term_matrix = pd.DataFrame()
        metadata = pd.DataFrame()
        for meta, text in self.corpus:
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            frequencies = pd.Series(counter(tokens))
            frequencies.name = Path(meta.index[0]).stem
            document_term_matrix = document_term_matrix.append(frequencies)
            stem = Path(meta.index[0]).stem
            meta['stem'] = stem
            metadata = metadata.append(meta)
        matrix_sum = document_term_matrix.sum()
        sorted_matrix = matrix_sum.sort_values(ascending=False)
        document_term_matrix = document_term_matrix.loc[:, sorted_matrix.index]
        document_term_matrix = document_term_matrix.fillna(0)
        document_term_matrix.to_csv(Path(self.target, 'corpus.matrix'))
        metadata.to_csv(Path(self.target, 'corpus.metadata'))

    def to_graph(self, tokenizer, counter, variant='gexf', **preprocessing):
        """Converst the corpus into a graph.

        In mathematics, and more specifically in graph theory, a graph is a
        structure amounting to a set of objects in which some pairs of the
        objects are in some sense *related*. This method creates nodes
        (*objects*) for each document (basically the filename), as well as for
        each type in the corpus. Each document node has one or more attributes
        based on the metadata extracted from the filenames. If a type appears
        in a document, there will be an directed edge between document node and
        type node. Each edge has an attribute with type frequency within the
        document.

        You can convert the graph to various graph-specific XML formats:
            * `GEXF <https://gephi.org/gexf/format/>`_
            * `GML <https://gephi.org/users/supported-graph-formats/gml-\
            format/>`_
            * `GraphML <http://graphml.graphdrawing.org/>`_
            * `Pajek <http://vlado.fmf.uni-lj.si/pub/networks/pajek/>`_
            * `SparseGraph6 <https://networkx.github.io/documentation/networkx\
            -1.10/reference/readwrite.sparsegraph6.html>`_
            * `YAML <http://yaml.org/>`_

        Args:
            tokenizer (:obj:`function`): This must be a function for
                tokenization. You could use a simple regex function or from
                `NLTK <http://www.nltk.org>`_.
            counter (:obj:`function`): This must be a function which counts
                elements of an iterable. There are various schemes for
                determining the value that each entry in the matrix should
                take. One such scheme is
                `tf-idf <https://en.wikipedia.org/wiki/Tf-idf>`_. But you can
                simply use the :class:`Counter` provided in the Python
                standard library.
            variant (:obj:`str`): This must be the kind of XML foramt you want
                to convert the graph to. Possible values are ``gexf``, ``gml``,
                ``graphml``, ``pajek``, ``graph6``, and ``yaml``.
            \*\*preprocessing (:obj:`function`, optional): This can be one or
                even more functions which take the output of your tokenizer
                function as input. So, you could write a function which counts
                the terms in your corpus and removes the 100 most frequent
                words.

        Returns:
            None, but writes the formatted corpus to disk.

        """
        G = nx.DiGraph()
        for meta, text in self.corpus:
            stem = Path(meta.index[0]).stem
            G.add_node(stem, **meta.to_dict('record')[0])
            tokens = tokenizer(text)
            frequencies = counter(tokens)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            for token in tokens:
                G.add_edge(token, stem, frequency=frequencies[token])
        if variant == 'gexf':
            nx.write_gexf(G, Path(self.target, 'corpus.gexf'))
        elif variant == 'gml':
            nx.write_gml(G, Path(self.target, 'corpus.gml'))
        elif variant == 'graphml':
            nx.write_graphml(G, Path(self.target, 'corpus.graphml'))
        elif variant == 'pajek':
            nx.write_pajek(G, Path(self.target, 'corpus.pajek'))
        elif variant == 'graph6':
            nx.write_graph6(G, Path(self.target, 'corpus.graph6'))
        elif variant == 'yaml':
            nx.write_yaml(G, Path(self.target, 'corpus.yaml'))
        else:
            raise ValueError("The variant '{0}' is not supported."
                             "Use 'gexf', 'gml', 'graphml', 'pajek',"
                             "'graph6' or 'yaml'.".format(variant))

    def to_ldac(self, tokenizer, counter, **preprocessing):
        """Converts the corpus into the LDA-C format.

        In the LDA-C corpus format, each document is succinctly represented as
        a sparse vector of word counts. Each line is of the form:

        ``[M] [term_1]:[count] [term_2]:[count] ...  [term_N]:[count]``

        where ``[M]`` is the number of unique terms in the document, and the
        ``[count]`` associated with each term is how many times that term
        appeared in the document. Note that ``[term_1]`` is an integer which
        indexes the term; it is not a string. This will be in the file
        ``corpus.ldac``.

        The vocabulary, exactly one term per line, will be in the file
        ``corpus.tokens``. Furthermore, metadata extracted from the filenames
        will be in the file ``corpus.metadata``.

        Args:
            tokenizer (:obj:`function`): This must be a function for
                tokenization. You could use a simple regex function or from
                `NLTK <http://www.nltk.org>`_.
            counter (:obj:`function`): This must be a function which counts
                elements of an iterable. There are various schemes for
                determining the value that each entry should take. One such
                scheme is `tf-idf <https://en.wikipedia.org/wiki/Tf-idf>`_.
                But you can simply use the :class:`Counter` provided in the
                Python standard library.
            \*\*preprocessing (:obj:`function`, optional): This can be one or
                even more functions which take the output of your tokenizer
                function as input. So, you could write a function which counts
                the terms in your corpus and removes the 100 most frequent
                words.

        Returns:
            None, but writes three files to disk.

        """
        corpus_ldac = Path(self.target, 'corpus.ldac')
        if corpus_ldac.exists():
            corpus_ldac.unlink()
        vocabulary = pd.Series()
        metadata = pd.DataFrame()
        for meta, text in self.corpus:
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            frequencies = counter(tokens)
            instance = [str(len(frequencies))]
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary)
            instance.extend(['{0}:{1}'.format(vocabulary[token],
                                              frequencies[token])
                                              for token in frequencies])
            if not corpus_ldac.exists():
                with corpus_ldac.open('w', encoding='utf-8') as file:
                    file.write(' '.join(instance) + '\n')
            else:
                with corpus_ldac.open('a', encoding='utf-8') as file:
                    file.write(' '.join(instance) + '\n')
            stem = Path(meta.index[0]).stem
            meta['basename'] = stem
            metadata = metadata.append(meta)
        corpus_vocab = Path(self.target, 'corpus.tokens')
        with corpus_vocab.open('w', encoding='utf-8') as file:
            file.write('\n'.join(vocabulary.index))
        metadata.to_csv(Path(self.target, 'corpus.metadata'))

    def to_svmlight(self, tokenizer, counter, classes, **preprocessing):
        """Converts the corpus into the SVMlight format.

        In the SVMlight corpus format, each document is succinctly represented
        as a sparse vector of word counts. Each line is of the form:

        ``[c] [term_1]:[count] [term_2]:[count] ... [term_N]:[count]``

        where ``[c]`` is the identifier of the instance class (in the context
        of topic modeling this is 0 for all instances), and the ``[count]``
        associated with each term is how many times that term appeared in the
        document. Note that ``[term_1]`` is an integer which indexes the
        term; it is not a string. This will be in the file ``corpus.svmlight``.

        The vocabulary, exactly one term per line, will be in the file
        ``corpus.tokens``. Furthermore, metadata extracted from the filenames
        will be in the file ``corpus.metadata``.

        Args:
            tokenizer (:obj:`function`): This must be a function for
                tokenization. You could use a simple regex function or from
                `NLTK <http://www.nltk.org>`_.
            counter (:obj:`function`): This must be a function which counts
                elements of an iterable. There are various schemes for
                determining the value that each entry should take. One such
                scheme is `tf-idf <https://en.wikipedia.org/wiki/Tf-idf>`_.
                But you can simply use the :class:`Counter` provided in the
                Python standard library.
            classes (:obj:`iterable`): An iterable of the classes of the
                documents. For instance, +1 as the target value marks a
                positive example, -1 a negative example respectively.
            \*\*preprocessing (:obj:`function`, optional): This can be one or
                even more functions which take the output of your tokenizer
                function as input. So, you could write a function which counts
                the terms in your corpus and removes the 100 most frequent
                words.

        Returns:
            None, but writes three files to disk.

        """
        corpus_svmlight = Path(self.target, 'corpus.svmlight')
        if corpus_svmlight.exists():
            corpus_svmlight.unlink()
        vocabulary = pd.Series()
        metadata = pd.DataFrame()
        for corpus, cl in zip(self.corpus, classes):
            text = corpus[1]
            meta = corpus[0]
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            frequencies = counter(tokens)
            instance = [str(cl)]
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary) + 1
            instance.extend(['{0}:{1}'.format(vocabulary[token],
                                              frequencies[token])
                                              for token in frequencies])
            if not corpus_svmlight.exists():
                with corpus_svmlight.open('w', encoding='utf-8') as file:
                    file.write(' '.join(instance) + '\n')
            else:
                with corpus_svmlight.open('a', encoding='utf-8') as file:
                    file.write(' '.join(instance) + '\n')
            stem = Path(meta.index[0]).stem
            meta['basename'] = stem
            metadata = metadata.append(meta)
        corpus_vocab = Path(self.target, 'corpus.tokens')
        with corpus_vocab.open('w', encoding='utf-8') as file:
            file.write('\n'.join(vocabulary.index))
        metadata.to_csv(Path(self.target, 'corpus.metadata'))
