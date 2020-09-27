from bitstring import BitArray

FILE = "Chaves de Criptografia.txt"


def read_keys():
    with open(FILE, "r") as f:
        tmp_keys = [line for line in f.readlines()]

    keys = []
    for key in tmp_keys:
        hex_string = key.rstrip("\n")[1:-1]
        bits = BitArray(hex=hex_string)
        keys.append(bits)

    return keys[:-1]


def print_result(results: list, test: str):
    print(f"Results for {test}")
    for idx, result in enumerate(results):
        key_idx = str(idx + 1).zfill(2)
        result_str = "passed" if result else "rejected"
        
        print(f"Key {key_idx}: {result_str}")
        

def monobit_test(keys: list):
    result = []
    for key in keys:
        count = 0
        for character in key:
            if character:
                count += 1

        if 9654 < count < 10346:
            result.append(True)
        else:
            result.append(False)

    print_result(result, 'Monobit')


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def poker_test(keys: list):
    result = []
    for key in keys:
        occurrences = dict()
        poker_list = chunks(key, 4)
        for chunk in poker_list:
            if chunk.bin in occurrences.keys():
                occurrences[chunk.bin] += 1
            else:
                occurrences[chunk.bin] = 0

        f = [occurrence ** 2 for occurrence in occurrences.values()]
        x = (16 / 5000) * sum(f) - 5000
        if 1.03 < x < 57.4:
            result.append(True)
        else:
            result.append(False)

    print_result(result, 'Poker Test')


def get_runs(key: list):
    runs = dict()
    run_number = 1
    previous_bit = None
    for idx, bit in enumerate(key):
        if previous_bit is None:
            runs[run_number] = {'start': idx}

        elif previous_bit != bit:
            end = {'end': idx - 1}
            runs[run_number].update(end)

            run_number += 1
            runs[run_number] = {'start': idx}

        if idx == len(key) - 1:
            end = {'end': idx}
            runs[run_number].update(end)

        previous_bit = bit
            
    return runs
    

def runs_test(keys: list):
    run_table = {
        1: (2267, 2733),
        2: (1079, 1421),
        3: (502, 748),
        4: (223, 402),
        5: (90, 223),
        6: (90, 233),
    }
    
    result = []
    for key in keys:
        runs = get_runs(key)
        
        is_valid = True
        for run in runs:
            start = runs[run]['start']
            end = runs[run]['end']
            
            length = end - start + 1
            length = 6 if length > 6 else length
            
            start_expected, end_expected = run_table[length]
            
            if not (start_expected <= start <= end <= end_expected):
                is_valid = False
        
        result.append(is_valid)
                
    print_result(result, 'Runs Test')

    
def long_run_test(keys: list):
    result = []
    for key in keys:
        runs = get_runs(key)
        
        is_valid = True
        for run in runs:
            start = runs[run]['start']
            end = runs[run]['end']
            
            length = end - start + 1
            
            if length >= 34:
                is_valid = False
                break
        
        result.append(is_valid)
            
    print_result(result, 'Long Run Test')


if __name__ == "__main__":
    keys = read_keys()
    
    monobit_test(keys)
    poker_test(keys)
    runs_test(keys)
    long_run_test(keys)