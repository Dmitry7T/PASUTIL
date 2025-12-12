import hashlib

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def tracking(time):
    original_hash = get_file_hash(f"pasutil1/jsons/{time}.txt")

    while True:
        current_hash = get_file_hash('pasutil1/jsons/my_file.txt')
        if current_hash != original_hash:
            print('Файл изменен!')
            break