#!/usr/bin/env python3

from pathlib import Path
from unittest import TestCase
from nltk import tokenize, FreqDist
import re
from collections import Counter
import sys
sys.path.append('..')
from forpus import forpus

def tokenizer(document):
    return re.compile('\w+').findall(document.lower())

def drop_stopwords(tokens, stopwords=['the', 'a', 'of']):
    return [token for token in tokens if token not in stopwords]

class TestJSON(TestCase):
    def setUp(self):
        self.output = Path('output')
        self.output.mkdir()
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')

    def test_conversion_onefile(self):
        self.corpus.to_json(onefile=True)
        generated_file = Path('output', 'corpus.json')
        self.assertTrue(generated_file.exists())
    
    def test_conversion_multiple_files(self):
        self.corpus.to_json(onefile=False)
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
    
    def tearDown(self):
        for file in self.output.iterdir():
            file.unlink()
        self.output.rmdir()

class TestDocumentTermMatrix(TestCase):
    def setUp(self):
        self.generated_file = Path('output', 'corpus.matrix')
        self.metadata = Path('output', 'corpus.metadata')
        self.output = Path('output')
        self.output.mkdir()
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')

    def test_conversion(self):
        self.corpus.to_document_term_matrix(tokenizer=tokenizer,
                                            counter=Counter,
                                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists() and
                        self.metadata.exists())
    
    def test_third_party_tokenizer(self):
        self.corpus.to_document_term_matrix(tokenizer=tokenize.wordpunct_tokenize,
                                            counter=Counter,
                                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists() and
                        self.metadata.exists())
    
    def test_third_party_counter(self):
        self.corpus.to_document_term_matrix(tokenizer=tokenizer,
                                            counter=FreqDist,
                                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists() and
                        self.metadata.exists())
    
    def tearDown(self):
        for file in self.output.iterdir():
            file.unlink()
        self.output.rmdir()

class TestGraph(TestCase):
    def setUp(self):
        self.generated_file = Path('output', 'corpus.gexf')
        self.output = Path('output')
        self.output.mkdir()
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')

    def test_conversion(self):
        self.corpus.to_graph(tokenizer=tokenizer,
                             counter=Counter,
                             variant='gexf',
                             drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists())
    
    def test_exception(self):
        with self.assertRaises(ValueError):
            self.corpus.to_graph(tokenizer=tokenizer,
                                 counter=Counter,
                                 variant='notsupported')

    def test_third_party_tokenizer(self):
        self.corpus.to_graph(tokenizer=tokenize.wordpunct_tokenize,
                             counter=Counter,
                             drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists())
    
    def test_third_party_counter(self):
        self.corpus.to_graph(tokenizer=tokenizer,
                             counter=FreqDist,
                             drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists())

    def tearDown(self):
        for file in self.output.iterdir():
            file.unlink()
        self.output.rmdir()

class TestLdaC(TestCase):
    def setUp(self):
        self.generated_file1 = Path('output', 'corpus.ldac')
        self.generated_file2 = Path('output', 'corpus.tokens')
        self.metadata = Path('output', 'corpus.metadata')
        self.output = Path('output')
        self.output.mkdir()
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')

    def test_conversion(self):
        self.corpus.to_ldac(tokenizer=tokenizer,
                            counter=Counter,
                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
    
    def test_third_party_tokenizer(self):
        self.corpus.to_ldac(tokenizer=tokenize.wordpunct_tokenize,
                            counter=Counter,
                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
    
    def test_third_party_counter(self):
        self.corpus.to_ldac(tokenizer=tokenizer,
                            counter=FreqDist,
                            drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())

    def tearDown(self):
        for file in self.output.iterdir():
            file.unlink()
        self.output.rmdir()

class TestSvmLight(TestCase):
    def setUp(self):
        self.classes = [0 for n in range(3)]
        self.generated_file1 = Path('output', 'corpus.svmlight')
        self.generated_file2 = Path('output', 'corpus.tokens')
        self.metadata = Path('output', 'corpus.metadata')
        self.output = Path('output')
        self.output.mkdir()
        self.corpus = forpus.Corpus(source='corpus',
                                    target='output')

    def test_conversion(self):
        self.corpus.to_svmlight(tokenizer=tokenizer,
                                classes=self.classes,
                                counter=Counter,
                                drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
                        
    def test_third_party_tokenizer(self):
        self.corpus.to_svmlight(tokenizer=tokenize.wordpunct_tokenize,
                                classes=self.classes,
                                counter=Counter,
                                drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
    
    def test_third_party_counter(self):
        self.corpus.to_svmlight(tokenizer=tokenizer,
                                classes=self.classes,
                                counter=FreqDist,
                                drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())

    def tearDown(self):
        for file in self.output.iterdir():
            file.unlink()
        self.output.rmdir()
