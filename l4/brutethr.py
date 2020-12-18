import pyminizip # this one is faster, but has false positives on extraction
import zipfile # this one is slow, but no false positives so far
from threading import Thread

# archive parameters
archive = 'enc.zip'
# outputs to cwd

# password parameters
max_len = 4 # maximum length a password can have
start = 97 # low symbol a password can have. 97 is a
end = 122 # high sumbol a password can have. 122 is z

# how many combinations to check per thread
options_per_thread = 10000

alpha = end - start + 1

class MyCustomException(Exception):
    pass

def iterate(stac, endc, l):
    finished = False
    c = stac
    endc -= 1
    l -= 1

    while not finished:
        # try archive
        try:
            # a = i%(26**1)//(26**0)
            # b = i%(26**2)//(26**1)
            # c = i%(26**3)//(26**2)
            # then just add 97 to each, turn to char and concatenate
            pwd = ''.join([chr(i+start) for i in [c%(alpha**i)//(alpha**(i-1))
            for i in range(l+1, 0, -1)]])
            # this will go into exception, if password is incorrect
            pyminizip.uncompress(archive, pwd, None, 1)
            with zipfile.ZipFile(archive) as f:
                f.extractall(pwd=bytes(pwd, 'utf-8'))
            # so this is reached only if password is correct
            finished = True
            print(f'password found: {pwd}')
        except Exception:
            pass

        # iterate
        if c == endc: # we reached zzz... of maximum length
            finished = True
        c += 1

thr = []
for i in range(1, max_len+1):
    opt = alpha**i
    gc = 0
    while opt > gc:
        thr.append(Thread(target=iterate, args=[gc, gc+min(options_per_thread, opt-gc), i]))
        gc += options_per_thread

    print(f'Checking length {i}. Total {len(thr)} threads created')

for i in thr:
    i.start()

for i in thr:
    i.join()
