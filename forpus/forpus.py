from pathlib import Path
from metadata_toolbox.utils import fname2metadata, metadata2fname
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
    fashion, one document at a time, processed, and closed before the next one.
    Have a look at :meth:`__init__`, if you are interested in how this is
    implemented.
    
    There is a plenty of formats available:
        * JSON, see :meth:`to_json`.

    Attributes:
        corpus (:obj:`iterable`): An iterable of (``metadata``, ``text``).
            ``metadata`` is a pandas DataFrame containing metadata extracted
            from the filename. ``text`` is the content of the file as string.
        target (str): The target directory. If it does not exist, it will be
            created.
    
    """
    def __init__(self, source, target, fname_pattern='{author}_{title}'):
        """Example of docstring on the __init__ method.

        The __init__ method may be documented in either the class level
        docstring, or as a docstring on the __init__ method itself.

        Either form is acceptable, but the two should not be mixed. Choose one
        convention to document the __init__ method and be consistent with it.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1 (str): Description of `param1`.
            param2 (:obj:`int`, optional): Description of `param2`. Multiple
                lines are supported.
            param3 (:obj:`list` of :obj:`str`): Description of `param3`.

        """
        def stream_corpus(path, fname_pattern):
            p = Path(path)
            for file in p.glob('*.txt'):
                with file.open('r', encoding='utf-8') as document:
                    yield fname2metadata(str(file), fname_pattern), document.read()
        self.corpus = stream_corpus(source, fname_pattern)
        self.target = Path(target)
        if not self.target.exists():
            self.target.mkdir()
    
    def to_json(self, onefile=True):
        """Class methods are similar to regular functions.

        Note:
            Do not include the `self` parameter in the ``Args`` section.

        Args:
            param1: The first parameter.
            param2: The second parameter.

        Returns:
            True if successful, False otherwise.

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
