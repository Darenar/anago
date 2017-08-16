import os
import unittest

from anago.data.reader import DataSet, extract_data, load_glove_vocab, load_word_embeddings
from anago.data.preprocess import WordPreprocessor


class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.filename = os.path.join(os.path.dirname(__file__), '../data/conll2003/en/test.txt')

    def test_extract(self):
        sents, labels = extract_data(self.filename)
        self.assertTrue(len(sents) == len(labels))

    def test_dataset(self):
        sents, labels = extract_data(self.filename)
        d = DataSet(sents, labels)
        sents, labels = d.next_batch(batch_size=32)
        self.assertTrue(len(sents) == len(labels))

    def test_dataset_with_preprocessing(self):
        X, y = extract_data(self.filename)
        d = DataSet(X, y)
        sents, tags = d.next_batch(batch_size=1)
        word, tag = sents[0][0], tags[0][0]
        self.assertIsInstance(word, str)
        self.assertIsInstance(tag, str)

        p = WordPreprocessor()
        p = p.fit(X, y)
        d = DataSet(X, y, preprocessor=p)
        sents, tags = d.next_batch(batch_size=1)
        chars, words = sents[0]
        word, char, tag = words[0], chars[0][0], tags[0][0]
        self.assertIsInstance(word, int)
        self.assertIsInstance(char, int)
        self.assertIsInstance(tag, int)

    def test_load_glove_vocab(self):
        self.DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
        filename = os.path.join(self.DATA_DIR, 'glove.50d.txt')
        vocab = load_glove_vocab(filename)
        true_vocab = {'the', ',', '.'}
        self.assertEqual(vocab, true_vocab)

    def test_load_word_embeddings(self):
        self.DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
        filename = os.path.join(self.DATA_DIR, 'glove.50d.txt')
        vocab = load_glove_vocab(filename)
        vocab = {w: i for i, w in enumerate(vocab)}
        dim = 50
        embeddings = load_word_embeddings(vocab, filename, dim=dim)
        self.assertEqual(embeddings.shape[1], dim)

        dim = 10
        embeddings = load_word_embeddings(vocab, filename, dim=dim)
        self.assertEqual(embeddings.shape[1], dim)

        dim = 1000
        actual_dim = 50
        embeddings = load_word_embeddings(vocab, filename, dim=dim)
        self.assertNotEqual(embeddings.shape[1], dim)
        self.assertEqual(embeddings.shape[1], actual_dim)