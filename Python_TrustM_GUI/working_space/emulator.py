'''
To emulate the function of xxd with a python script
'''
#!/usr/bin/env python3

import sys

def format_hex_line(offset, bytes_line):
    # Create pairs of two hexadecimal characters
    hex_pairs = [f'{byte:02x}' for byte in bytes_line]
    # Group these pairs in fours, join with a space
    hex_part = ' '.join([''.join(hex_pairs[i:i+2]) for i in range(0, len(hex_pairs), 2)])
    ascii_part = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in bytes_line)
    space_padding = ' ' * (39 - len(hex_part))  # Adjust the number of spaces for alignment
    return f'{offset:08x}: {hex_part:<39} {ascii_part}'





def xxd_emulator(file_path):
    with open(file_path, 'rb') as file:
        offset = 0
        while True:
            bytes_line = file.read(16)
            if not bytes_line:
                break
            print(format_hex_line(offset, bytes_line))
            offset += 16

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python3 script.py filename", file=sys.stderr)
        sys.exit(1)
    xxd_emulator(sys.argv[1])
