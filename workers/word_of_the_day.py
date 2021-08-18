class WordOfTheDay:
    word, url = "", ""
    part_of_speech, definitions, examples, source_texts, source_links, date = [], [], [], [], [], []

    def initialize(self, word, part_of_speech, definitions, examples, source_texts, source_links, url, date):
        self.word = word
        self.part_of_speech = part_of_speech
        self.definitions = definitions
        self.examples = examples
        self.source_texts = source_texts
        self.source_links = source_links
        self.url = url
        self.date = date
        return self

    def __iter__(self):
        return iter((self.word, self.part_of_speech, self.definitions,
                     self.examples, self.source_texts, self.source_links, self.url, self.date))
