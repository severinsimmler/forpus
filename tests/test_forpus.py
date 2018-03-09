from pathlib import Path
from unittest import TestCase
import re
from collections import Counter
import sys
sys.path.append('..')
from forpus import forpus

def tokenizer(document):
    return re.compile('\w+').findall(document.lower())

def drop_stopwords(tokens, stopwords=['the', 'a', 'of']):
    return [token for token in tokens if token not in stopwords]

class TestJson(TestCase):
    def setUp(self):
        pass

    def test_conversion_onefile(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_json(onefile=True)
        generated_file = Path('output', 'corpus.json')
        self.assertTrue(generated_file.exists())
    
    def test_conversion_multiple_files(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_json(onefile=False)
        peter = Path('output', 'peter_doc1.json')
        paul = Path('output', 'paul_doc2.json')
        mary = Path('output', 'mary_doc3.json')
        self.assertTrue(peter.exists() and paul.exists() and mary.exists())
    
    def test_metadata_exception(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output',
                               fname_pattern='{author}/{title}')
        with self.assertRaises(ValueError):
            corpus.to_json()

class TestDocumentTermMatrix(TestCase):
    def setUp(self):
        pass

    def test_conversion(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_document_term_matrix(tokenizer=tokenizer,
                                       counter=Counter,
                                       drop_stopwords=drop_stopwords)
        generated_file = Path('output', 'corpus.matrix')
        metadata = Path('output', 'corpus.metadata')
        self.assertTrue(generated_file.exists() and metadata.exists())

class TestDocumentTermMatrix(TestCase):
    def setUp(self):
        pass

    def test_conversion(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_graph(tokenizer=tokenizer,
                        variant='gexf',
                        drop_stopwords=drop_stopwords)
        generated_file = Path('output', 'corpus.gexf')
        self.assertTrue(generated_file.exists())
    
    def test_exception(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        with self.assertRaises(ValueError):
            corpus.to_graph(tokenizer=tokenizer,
                            variant='notsupported')

class TestLdaC(TestCase):
    def setUp(self):
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')
        self.generated_file1 = Path('output', 'corpus.ldac')
        self.generated_file2 = Path('output', 'corpus.tokens')
        self.metadata = Path('output', 'corpus.metadata')

    def test_conversion(self):
        self.corpus.to_ldac(tokenizer=tokenizer,
                            counter=Counter,
                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())

class TestSvmLight(TestCase):
    def setUp(self):
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')
        self.classes = [0 for n in range(3)]
        self.generated_file1 = Path('output', 'corpus.svmlight')
        self.generated_file2 = Path('output', 'corpus.tokens')
        self.metadata = Path('output', 'corpus.metadata')

    def test_conversion(self):
        self.corpus.to_svmlight(tokenizer=tokenizer,
                                classes=self.classes,
                                counter=Counter,
                                drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
