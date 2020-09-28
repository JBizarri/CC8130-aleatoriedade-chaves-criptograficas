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


def print_result(tests_results: list):
    tests_names = [test_result['name'] for test_result in tests_results]
    print(f"{'Keys':8}", end='\t')
    for test_name in tests_names:
        print(f"{test_name:15}", end='\t')
    results = [test_result['result'] for test_result in tests_results]
    count = 0
    for result in zip(*results):
        key_index = str(count + 1).zfill(2)
        print(f"\n{'Key '}{key_index:4}", end='\t')
        for r in result:
            r = 'Pass' if r else 'Reject'
            print(f"{r:15}", end='\t')

        count += 1


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

    return {'name': 'Monobit Test', 'result': result}


def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def poker_test(keys: list):
    result = []
    for key in keys:
        occurrences = dict()
        poker_list = chunks(key, 4)
        for chunk in poker_list:
            if chunk.bin in occurrences.keys():
                occurrences[chunk.bin] += 1
            else:
                occurrences[chunk.bin] = 1

        f = [occurrence ** 2 for occurrence in occurrences.values()]
        x = (16 / 5000) * sum(f) - 5000
        if 1.03 < x < 57.4:
            result.append(True)
        else:
            result.append(False)

    return {'name': 'Poker Test', 'result': result}


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


def get_occurences_in_runs(runs: dict):
    occurences = dict()
    for run in runs:
        start = runs[run]['start']
        end = runs[run]['end']

        length = end - start + 1
        length = 6 if length > 6 else length
        if length in occurences.keys():
            occurences[length] += 1
        else:
            occurences[length] = 1

    return occurences


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
        occurrences = get_occurences_in_runs(runs)
        is_valid = True
        for length, occurrence in occurrences.items():
            interval_min, interval_max = run_table.get(length)

            if not (interval_min <= occurrence <= interval_max):
                is_valid = False
                break

        result.append(is_valid)

    return {'name': 'Runs Test', 'result': result}


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

    return {'name': 'Long Run Test', 'result': result}


if __name__ == "__main__":
    keys = read_keys()

    print("Running tests...")
    tests = [monobit_test, poker_test, runs_test, long_run_test]

    results = [test(keys) for test in tests]
    print_result(results)
