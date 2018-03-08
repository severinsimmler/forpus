from pathlib import Path
from metadata_toolbox.utils import fname2metadata
import json


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
        """Converts the corpus to JSON.

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
        for metadata, text in self.corpus:
            stem = Path(metadata.index[0]).stem
            document_json = metadata.to_dict('record')[0]
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

    def to_tei(self):
        """
        cf. http://adrien.barbaresi.eu/blog/parsing-converting-lxml-html-
        tei.html
        """
        pass
