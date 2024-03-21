import json
import sys

def main():
    data = json.load(sys.stdin)
    per = data['error_rate']
    wer = 1 - data['exact_match']
    print(f'{per:.2f} & {wer:.2f}')

if __name__ == '__main__':
    main()
