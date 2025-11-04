filepath = 'pasutil1\symbols\\'
with open(filepath + 'crypto.txt', 'r', encoding='utf-8') as f:
    crypto = eval(f.read().strip())
with open(filepath + 'forex.txt', 'r', encoding='utf-8') as f:
    forex = eval(f.read().strip())
with open(filepath + 'index.txt', 'r', encoding='utf-8') as f:
    index = eval(f.read().strip())
