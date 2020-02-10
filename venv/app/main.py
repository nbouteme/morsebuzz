import serial;
import time;

ser = serial.Serial('/dev/ttyACM0', timeout=1.0)


def morsedecoder():
    mdict = {
        'A': '.-', 'B': '-...',
        'C': '-.-.', 'D': '-..', 'E': '.',
        'F': '..-.', 'G': '--.', 'H': '....',
        'I': '..', 'J': '.---', 'K': '-.-',
        'L': '.-..', 'M': '--', 'N': '-.',
        'O': '---', 'P': '.--.', 'Q': '--.-',
        'R': '.-.', 'S': '...', 'T': '-',
        'U': '..-', 'V': '...-', 'W': '.--',
        'X': '-..-', 'Y': '-.--', 'Z': '--..',
        '1': '.----', '2': '..---', '3': '...--',
        '4': '....-', '5': '.....', '6': '-....',
        '7': '--...', '8': '---..', '9': '----.',
        '0': '-----', ', ': '--..--', '.': '.-.-.-',
        '?': '..--..', '/': '-..-.', '-': '-....-',
        '(': '-.--.', ')': '-.--.-'
    }
    # -.-. --- ..-
    inv_dict = {v: k for k, v in mdict.items()}
    vals = [v for k, v in mdict.items()]
    b = ""
    while len([x for x in vals if str(x).startswith(b)]) > 1:
        inp = yield
        if inp == ' ':
            break;
        b += str(inp)
    if b in inv_dict:
        return inv_dict[b]
    return None

print("Starting...");
md = morsedecoder();
next(md)

while True:
    arr = ser.read(1);
    b = int.from_bytes(arr, "little")
    if len(arr) == 0:
        try:
            md.send(' ')
        except StopIteration as e:
            if e.value:
                print(e.value, end="")
        md = morsedecoder()
        next(md)
        continue;
    if b == 1:
        t = time.time()
    if b == 0:
        el = time.time() - t
        try:
            md.send('-' if el > 0.2 else '.')
        except StopIteration as e:
            if e.value:
                print(e.value, end="")
            md = morsedecoder()
            next(md)
