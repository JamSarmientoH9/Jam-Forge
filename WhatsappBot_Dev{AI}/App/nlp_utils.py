import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import spacy

class TextProcessor:
    def __init__(self, use_spacy=True):
        self.use_spacy = use_spacy
        
        if use_spacy:
            try:
                self.nlp = spacy.load('es_dep_news_trf')
            except Exception as e:
                print(f"Error cargando el modelo de spacy model: {e}")
                self.use_spacy = False
                self.nlp = None
        else:
            nltk.download('punkt')
            nltk.download('wordnet')
            nltk.download('stopwords')
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))

    def clean_text(self, text):
        """
        Clean the input text by removing special characters and converting to lowercase.
        """
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text.lower()

    def tokenize(self, text):
        """
        Tokenize the input text into individual words.
        """
        if self.use_spacy:
            doc = self.nlp(text)
            return [token.text for token in doc]
        else:
            return word_tokenize(text)

    def remove_stopwords(self, tokens):
        """
        Remove stopwords from the list of tokens.
        """
        if self.use_spacy:
            return [token for token in tokens if not self.nlp.vocab[token].is_stop]
        else:
            return [token for token in tokens if token not in self.stop_words]

    def lemmatize(self, tokens):
        """
        Lemmatize the list of tokens.
        """
        if self.use_spacy:
            doc = self.nlp(' '.join(tokens))
            return [token.lemma_ for token in doc]
        else:
            return [self.lemmatizer.lemmatize(token) for token in tokens]

    def preprocess(self, text):
        """
        Preprocess the input text by cleaning, tokenizing, removing stopwords, and lemmatizing.
        """
        cleaned_text = self.clean_text(text)
        tokens = self.tokenize(cleaned_text)
        tokens_without_stopwords = self.remove_stopwords(tokens)
        lemmatized_tokens = self.lemmatize(tokens_without_stopwords)
        return ' '.join(lemmatized_tokens)

    def get_named_entities(self, text):
        """
        Extract named entities from the text (spaCy only).
        """
        if self.use_spacy:
            doc = self.nlp(text)
            return [(ent.text, ent.label_) for ent in doc.ents]
        else:
            raise NotImplementedError("Named Entity Recognition is only available with spaCy")

    def get_pos_tags(self, text):
        """
        Get part-of-speech tags for the text.
        """
        if self.use_spacy:
            doc = self.nlp(text)
            return [(token.text, token.pos_) for token in doc]
        else:
            tokens = word_tokenize(text)
            return nltk.pos_tag(tokens)


# Example usage
if __name__ == "__main__":
    # Using spaCy
    spacy_processor = TextProcessor(use_spacy=True)
    text = "The quick brown fox jumps over the lazy dog."
    print("Processed text (spaCy):", spacy_processor.preprocess(text))
    print("Named Entities (spaCy):", spacy_processor.get_named_entities(text))
    print("POS Tags (spaCy):", spacy_processor.get_pos_tags(text))

    # Using NLTK
    nltk_processor = TextProcessor(use_spacy=False)
    print("Processed text (NLTK):", nltk_processor.preprocess(text))
    print("POS Tags (NLTK):", nltk_processor.get_pos_tags(text))
