import random
import tokenizer
import tqdm
import time
import pickle

source = 'test-source.txt'
tok = tokenizer.CharacterTokenizer
tokens_before_seek=5

def dictchoice(d):
    return random.choice(list(d))

try:
    with open(source + '.tokens-' + tok.name + '.pickle', 'rb') as o:
        token_positions = pickle.load(o)
except FileNotFoundError:
    token_positions = dict()
    tok_reader = tok()
    with open(source) as file:
        @tok_reader.on_token_fetched
        def token_fetched(token):
            if not token in token_positions:
                token_positions[token] = list()
            token_positions[token].append(file.tell())

        file.seek(0, 2)
        with tqdm.tqdm(total=file.tell()) as pb:
            file.seek(0, 0)
            chunk = file.read(1)
            while chunk:
                pb.update(len(chunk))
                tok_reader.read(chunk)
                chunk = file.read(1)
    with open(source + '.tokens-' + tok.name + '.pickle', 'wb') as o:
        pickle.dump(token_positions, o)

tok_writer = tok()
with open(source) as file:
    last_token = dictchoice(token_positions)
    def trigger_seek():
        time.sleep(1)
        next_position = random.choice(token_positions[last_token])
        file.seek(next_position, 0)
        global tokens_left
        tokens_left = tokens_before_seek

    trigger_seek()

    @tok_writer.on_token_fetched
    def token_fetched(token):
        print(token, end=tok_writer.sep, flush=True)
        global last_token
        last_token = token
        global tokens_left
        tokens_left -= 1
        if tokens_left == 0:
            trigger_seek()
    while 1:
        tok_writer.read(file.read(1))
