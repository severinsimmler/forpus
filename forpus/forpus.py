from pathlib import Path
from metadata_toolbox.utils import fname2metadata
import json
import pandas as pd
from collections import Counter


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
        * JSON, see :meth:`to_json`.
        * TEI XML, see :meth:`to_tei`.

    Once instantiated, you can convert the corpus **only once**. The concept of
    this library is to instantiate **one class for each target format**. For
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
                yield fname2metadata(fname, self.pattern), document.read()

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
            set the parameter ``onefile`` to True.

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

    def to_ldac(self, tokenizer, **preprocessing):
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
        ``corpus.vocab``. Furthermore, metadata extracted from the filenames
        will be in the file ``corpus.metadata``.
        
        Args:
            tokenizer (:obj:`function`): This must be a function for
                tokenization. You could use a simple regex function or from
                `NLTK <http://www.nltk.org>`_.
            \*\*preprocessing (:obj:`function`, optional): This can be one or
                even more functions which take the output of your tokenizer
                function as input. So, you could write a function which counts
                the terms in your corpus and removes the 100 most frequent
                words.

        Returns:
            None, but writes three files to disk.
        
        """
        vocabulary = dict()
        instances = list()
        metadata = pd.DataFrame()
        for meta, text in self.corpus:
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            frequencies = Counter(tokens)
            instance = [str(len(frequencies))]
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary)
            instance.extend(['{0}:{1}'.format(vocabulary[token],
                                              frequencies[token])
                                              for token in frequencies])
            instances.append(' '.join(instance))
            metadata = metadata.append(meta)
        corpus_ldac = Path(self.target, 'corpus.ldac')
        with corpus_ldac.open('w', encoding='utf-8') as file:
            file.write('\n'.join(instances))
        corpus_vocab = Path(self.target, 'corpus.vocab')
        with corpus_vocab.open('w', encoding='utf-8') as file:
            file.write('\n'.join(vocabulary.keys()))
        metadata.to_csv(Path(self.target, 'corpus.metadata'))

    def to_graph(self, tokenizer, variant='gexf', **preprocessing):
        G = nx.Graph()
        for meta, text in self.corpus:
            stem = Path(meta.index[0]).stem
            G.add_node(stem, **meta.to_dict('record')[0])
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            edges = [(token, stem) for token in tokens]
            G.add_edges_from(edges)
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
            raise ValueError("The variant '{0}' is not supported".format(variant))
    
    def to_document_term_matrix(self, tokenizer, **preprocessing):
        document_term_matrix = pd.DataFrame()
        metadata = pd.DataFrame()
        for meta, text in self.corpus:
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            frequencies = pd.Series(Counter(tokens))
            frequencies.name = Path(meta.index[0]).stem
            document_term_matrix = document_term_matrix.append(frequencies)
            stem = Path(meta.index[0]).stem
            meta['stem'] = stem
            metadata = metadata.append(meta)
        document_term_matrix = document_term_matrix.loc[:, document_term_matrix.sum().sort_values(ascending=False).index]
        document_term_matrix.fillna(0).to_csv(Path(self.target, 'corpus.matrix'))
        metadata.to_csv(Path(self.target, 'corpus.metadata'))
    
    def to_svmlight(self, tokenizer, **preprocessing):
        vocabulary = dict()
        instances = list()
        metadata = pd.DataFrame()
        for meta, text in self.corpus:
            tokens = tokenizer(text)
            if preprocessing:
                for func in preprocessing.values():
                    tokens = func(tokens)
            frequencies = Counter(tokens)
            instance = [str(0)]
            for token in tokens:
                if token not in vocabulary:
                    vocabulary[token] = len(vocabulary) + 1
            instance.extend(['{0}:{1}'.format(vocabulary[token],
                                              frequencies[token])
                                              for token in frequencies])
            instances.append(' '.join(instance))
            stem = Path(meta.index[0]).stem
            meta['stem'] = stem
            metadata = metadata.append(meta)
        corpus_ldac = Path(self.target, 'corpus.svmlight')
        with corpus_ldac.open('w', encoding='utf-8') as file:
            file.write('\n'.join(instances))
        corpus_vocab = Path(self.target, 'corpus.vocab')
        with corpus_vocab.open('w', encoding='utf-8') as file:
            file.write('\n'.join(vocabulary.keys()))
        metadata.to_csv(Path(self.target, 'corpus.metadata'))
