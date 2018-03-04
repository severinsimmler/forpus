from pathlib import Path
from metadata_toolbox import utils as mdt

class Corpus:
    def __init__(self, source, target, fname_pattern='{author}_{title}'):
        def stream_corpus(path, fname_pattern):
            p = Path(path)
            for file in p.glob('*.txt'):
                with file.open() as document:
                    yield mdt.fname2metadata(file, fname_pattern), document.read()
        self.corpus = stream_corpus(source, fname_pattern)
        self.target = target
