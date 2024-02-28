#!/pi/bin/env python3

import sys

def hex_to_binary(hex_data):
    try:
        if len(hex_data) % 2 != 0:
            raise ValueError("Length of hex data is not even.")
        return bytes.fromhex(hex_data)
    except ValueError as e:
        print(f"Error in conversion: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python hex_to_binary.py <hexdata>", file=sys.stderr)
        sys.exit(1)

    hex_data = sys.argv[1].strip()

    if len(hex_data) == 0:
        print("No hex data provided.", file=sys.stderr)
        sys.exit(1)

    binary_data = hex_to_binary(hex_data)

    if len(binary_data) == 0:
        print("No binary data generated.", file=sys.stderr)
        sys.exit(1)

    # Output the binary data to stdout
    sys.stdout.buffer.write(binary_data)

if __name__ == "__main__":
    main()
