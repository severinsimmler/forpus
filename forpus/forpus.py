from pathlib import Path
from metadata_toolbox.utils import fname2metadata
import json

class Corpus:
    """Convert a plain text corpus to a NLP-specific corpus format.
    
    Instantiate this class, if you have a directory of plain text files (.txt),
    and want to convert the content of those files into a NLP-specific corpus
    format. In most cases, each NLP tool uses its own idiosyncratic input
    format. This class helps you to convert a corpus very easy to the desired
    format.
    
    This class does not store the whole corpus at once in RAM, which is useful
    when handling very large corpora. Documents are streamed from disk in a lazy
    fashion, one document at a time, being processed, and closed before the next
    one. Have a look at :meth:`__init__`, if you are interested in how this is
    implemented.
    
    There is a plenty of formats available:
        * JSON, see :meth:`to_json`.

    Attributes:
        corpus (:obj:`iterable`): An iterable of (``metadata``, ``text``).
            ``metadata`` is a pandas DataFrame containing metadata extracted
            from the filename. ``text`` is the content of the file as string.
        target (:obj:`pathlib.PosixPath`): The target directory. If it does
            not exist, it will be created.
    
    """
    def __init__(self, source, target, fname_pattern='{author}_{title}'):
        """Instatiates :class:`Corpus`.

        This method instatiates all objects of the class :class:`Corpus`. There
        are only few arguments to pass. Have a look at the section below for
        more details.

        Args:
            source (str): The path to the corpus directory, e.g.
                ``/tmp/corpora/test_corpus``.
            target (str): The path to the output directory, e.g.
                ``/tmp/corpora/formatted_test_corpus``.
            fname_pattern (str, optional): The pattern of the corpus's
                filenames. Metadata wil be extracted from the filenames based on
                this pattern. If the pattern is ``None`` or does not match the
                structure, only the basename (without suffix) will be considered
                as metadata. An example for the filename ``parsons_social.txt``
                would be ``{author}_{title}``. ``parsons`` will be recognized as
                author, ``social`` as the title.

        """
        def stream_corpus(path, fname_pattern):
            p = Path(path)
            for file in p.glob('*.txt'):
                with file.open('r', encoding='utf-8') as document:
                    fname = str(file)
                    yield fname2metadata(fname, fname_pattern), document.read()
        self.corpus = stream_corpus(source, fname_pattern)
        self.target = Path(target)
        if not self.target.exists():
            self.target.mkdir()
    
    def to_json(self, onefile=True):
        """Converts the corpus to JSON.

        **JSON** (JavaScript Object Notation) is a lightweight data-interchange
        format. It is easy for humans to read and write. It is easy for machines
        to parse and generate. For more information on this format, follow
        `this link <https://www.json.org/index.html>`_.

        This method converts your plain text corpus to JSON. Besides the content
        of your documents, metadata will be included in the JSON. Have a look at
        :meth:`__init__` for proper metadata recognition.
        
        You have two options:
            1. Write the whole corpus into one single file. In this case, set
                :arg:`onefile` to True. An example could be:
                
                ```json
                {"parsons_system":
                    {"author": "parsons",
                     "title": "system",
                     "text": "Culture, Personality and the Social Systems..."},
                 "parsons_action":
                    {"author": "parsons",
                     "title": "action",
                     "text": "The Sick Role and the Role of the Physician..."}
                 }
                ```
            
            2. Write one file for each document. In this case, set
                :arg:`onefile` to False. An example for the first document could
                be:
                
                ```json
                {"author": "parsons",
                 "title": "system",
                 "text": "Culture, Personality and the Social Systems..."}
                ```

        Args:
            onefile (bool): If True, write the whole corpus in one file.
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
