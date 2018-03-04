from pathlib import Path
from metadata_toolbox.utils import fname2metadata, metadata2fname
import json

class Corpus:
    def __init__(self, source, target, fname_pattern='{author}_{title}'):
        def stream_corpus(path, fname_pattern):
            p = Path(path)
            for file in p.glob('*.txt'):
                with file.open('r', encoding='utf-8') as document:
                    yield fname2metadata(str(file), fname_pattern), document.read()
        self.corpus = stream_corpus(source, fname_pattern)
        self.target = target
    
    def to_json(self, onefile=True):
        """Short description.
        
        Args:
            onefile (bool): Description.
        
        Returns:
            None.
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
