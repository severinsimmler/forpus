from pathlib import Path

class Corpus:
    def __init__(self, source, target):
        def stream_corpus(path):
            p = Path(path)
            for file in p.glob('*.txt'):
                with file.open() as document:
                    yield document.read()
