import pyminizip # this one is faster, but has false positives on extraction
import zipfile # this one is slow, but no false positives so far

# archive parameters
archive = 'enc.zip'
# outputs to cwd

# password parameters
max_len = 4 # maximum length a password can have
start = 97 # low symbol a password can have. 97 is a
end = 122 # high sumbol a password can have. 122 is z

cur_len = 1
alpha = end - start + 1
counter = 0
finished = False

while not finished:
    # try archive
    try:
        # a = i%(26**1)//(26**0)
        # b = i%(26**2)//(26**1)
        # c = i%(26**3)//(26**2)
        # then just add 97 to each, turn to char and concatenate
        password = ''.join([chr(i+start) for i in [counter%(alpha**i)//(alpha**(i-1)) for i     in range(cur_len, 0, -1)]])
        print('\b'*cur_len, end='')
        print(password, end='')
        # this will go into exception, if password is incorrect
        pyminizip.uncompress(archive, password, None, 1)
        with zipfile.ZipFile(archive) as f:
            f.extractall(pwd=bytes(password, 'utf-8'))
        # so this is reached only if password is correct
        print(f'\npassword found: {password}')
        finished = True
    except Exception:
        pass

    # iterate
    if counter == alpha**max_len-1: # we reached zzz... of maximum length
        print('\nFailed')
        finished = True
    if counter == alpha**cur_len-1: # we reached zz.. for current length
        # since a~0, we want to increase length and run once more on the same
        # numbers, but with one more symbol this time
        counter -= alpha**cur_len # otherwise jumps to b in first symbol, so
        cur_len += 1
    counter += 1
