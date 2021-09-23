class Tokenizer:
    def __init__(self):
        self.on_token_funcs = []

    def read(self, chunk):
        raise NotImplementedError

    def token_fetched(self, token):
        for func in self.on_token_funcs:
            func(token)

    def on_token_fetched(self, func):
        self.on_token_funcs.append(func)
        return func

class CharacterTokenizer(Tokenizer):
    sep = ''
    name = 'char'

    def __init__(self):
        super().__init__()
        self.last_symbol_was_space = False

    def read(self, chunk):
        if len(chunk) != 1:
            for char in chunk:
                self.read(char)
        else:
            if chunk.isspace():
                if not self.last_symbol_was_space:
                    self.token_fetched(' ')
                self.last_symbol_was_space = True
            else:
                self.last_symbol_was_space = False
                self.token_fetched(chunk)

class WordTokenizer(Tokenizer):
    sep = ' '
    name = 'word'
    def __init__(self):
        super().__init__()
        self.word_buffer = []

    def read(self, chunk):
        if len(chunk) != 1:
            for char in chunk:
                self.read(char)
        else:
            if chunk.isspace():
                if self.word_buffer:
                    self.token_fetched(''.join(self.word_buffer))
                    self.word_buffer.clear()
            else:
                self.word_buffer.append(chunk)
