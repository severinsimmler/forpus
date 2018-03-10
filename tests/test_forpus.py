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
        self.generated_file = Path('output', 'corpus.matrix')
        self.metadata = Path('output', 'corpus.metadata')

    def test_conversion(self):
        if self.generated_file.exists():
            self.generated_file.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_document_term_matrix(tokenizer=tokenizer,
                                       counter=Counter,
                                       drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists() and
                        self.metadata.exists())
    
    def test_third_party_tokenizer(self):
        if self.generated_file.exists():
            self.generated_file.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_document_term_matrix(tokenizer=tokenize.wordpunct_tokenize,
                                       counter=Counter,
                                       drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists() and
                        self.metadata.exists())
    
    def test_third_party_counter(self):
        if self.generated_file.exists():
            self.generated_file.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_document_term_matrix(tokenizer=tokenizer,
                                       counter=FreqDist,
                                       drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists() and
                        self.metadata.exists())

class TestGraph(TestCase):
    def setUp(self):
        self.generated_file = Path('output', 'corpus.gexf')

    def test_conversion(self):
        if self.generated_file.exists():
            self.generated_file.unlink()
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_graph(tokenizer=tokenizer,
                        variant='gexf',
                        drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists())
    
    def test_exception(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        with self.assertRaises(ValueError):
            corpus.to_graph(tokenizer=tokenizer,
                            variant='notsupported')

    def test_third_party_tokenizer(self):
        if self.generated_file.exists():
            self.generated_file.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_graph(tokenizer=tokenize.wordpunct_tokenize,
                        counter=Counter,
                        drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists())
    
    def test_third_party_counter(self):
        if self.generated_file.exists():
            self.generated_file.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_graph(tokenizer=tokenizer,
                        counter=FreqDist,
                        drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file.exists())

class TestLdaC(TestCase):
    def setUp(self):
        self.generated_file1 = Path('output', 'corpus.ldac')
        self.generated_file2 = Path('output', 'corpus.tokens')
        self.metadata = Path('output', 'corpus.metadata')

    def test_conversion(self):
        if self.generated_file1.exists():
            self.generated_file1.unlink()
        if self.generated_file2.exists():
            self.generated_file2.unlink()
        if self.metadata.exists():
            self.metadata.unlink()
            
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_ldac(tokenizer=tokenizer,
                       counter=Counter,
                       drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
    
    def test_third_party_tokenizer(self):
        if self.generated_file1.exists():
            self.generated_file1.unlink()
        if self.generated_file2.exists():
            self.generated_file2.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_ldac(tokenizer=tokenize.wordpunct_tokenize,
                       counter=Counter,
                       drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
    
    def test_third_party_counter(self):
        if self.generated_file1.exists():
            self.generated_file1.unlink()
        if self.generated_file2.exists():
            self.generated_file2.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_ldac(tokenizer=tokenizer,
                       counter=FreqDist,
                       drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())

class TestSvmLight(TestCase):
    def setUp(self):
        self.classes = [0 for n in range(3)]
        self.generated_file1 = Path('output', 'corpus.svmlight')
        self.generated_file2 = Path('output', 'corpus.tokens')
        self.metadata = Path('output', 'corpus.metadata')

    def test_conversion(self):
        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_svmlight(tokenizer=tokenizer,
                           classes=self.classes,
                           counter=Counter,
                           drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
                        
    def test_third_party_tokenizer(self):
        if self.generated_file1.exists():
            self.generated_file1.unlink()
        if self.generated_file2.exists():
            self.generated_file2.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_svmlight(tokenizer=tokenize.wordpunct_tokenize,
                           classes=self.classes,
                           counter=Counter,
                           drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
    
    def test_third_party_counter(self):
        if self.generated_file1.exists():
            self.generated_file1.unlink()
        if self.generated_file2.exists():
            self.generated_file2.unlink()
        if self.metadata.exists():
            self.metadata.unlink()

        corpus = forpus.Corpus(source='corpus',
                               target='output')
        corpus.to_svmlight(tokenizer=tokenizer,
                           classes=self.classes,
                           counter=FreqDist,
                           drop_stopwords=drop_stopwords)
        self.assertTrue(self.generated_file1.exists() and
                        self.generated_file2.exists() and
                        self.metadata.exists())
