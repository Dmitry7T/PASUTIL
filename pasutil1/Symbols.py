filepath = 'pasutil1\symbols\\'
with open(filepath + 'crypto.txt', 'r') as f:
    crypto = eval(f.read().strip())
with open(filepath + 'forex.txt', 'r') as f:
    forex = eval(f.read().strip())
with open(filepath + 'index.txt', 'r') as f:
    index = eval(f.read().strip())
