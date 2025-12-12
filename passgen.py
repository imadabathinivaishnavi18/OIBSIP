import secrets
import string
import sys

MIN_LENGTH = 8
DEFAULT_LENGTH = 12
AMBIGUOUS = "O0l1"


def make_charset(use_symbols=True, drop_ambiguous=False):
    chars = string.ascii_letters + string.digits
    if use_symbols:
        chars += string.punctuation  # from Python's string.punctuation constant [web:7]
    if drop_ambiguous:
        chars = "".join(ch for ch in chars if ch not in AMBIGUOUS)
    return chars


def generate_password(length, use_symbols=True, drop_ambiguous=False):
    if length < MIN_LENGTH:
        raise ValueError(f"Length must be at least {MIN_LENGTH}.")

    charset = make_charset(use_symbols, drop_ambiguous)
    while True:
        pwd = "".join(secrets.choice(charset) for _ in range(length))
        if (any(c.islower() for c in pwd)
                and any(c.isupper() for c in pwd)
                and any(c.isdigit() for c in pwd)
                and (not use_symbols or any(c in string.punctuation for c in pwd))):
            return pwd


def ask_length(default=DEFAULT_LENGTH):
    raw = input(f"Enter password length (default={default}): ").strip()
    if not raw:
        return default
    try:
        val = int(raw)
        if val <= 0:
            raise ValueError
        return val
    except ValueError:
        print(f"Invalid length. Using default: {default}", file=sys.stderr)
        return default


def ask_yes_no(msg, default=True):
    suffix = " [Y/n]: " if default else " [y/N]: "
    ans = input(msg + suffix).strip().lower()
    if not ans:
        return default
    if ans in ("y", "yes"):
        return True
    if ans in ("n", "no"):
        return False
    print("Answer not understood, keeping default.", file=sys.stderr)
    return default


def strength_hint(length):
    if length < 10:
        return "Weak"
    if length < 14:
        return "Moderate"
    if length < 20:
        return "Strong"
    return "Very strong"


def main():
    print("Secure Password Generator\n")
    length = ask_length()
    use_symbols = ask_yes_no("Include punctuation symbols?", True)
    drop_amb = ask_yes_no("Exclude confusing characters (O, 0, l, 1)?", False)

    try:
        pwd = generate_password(length, use_symbols, drop_amb)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    print("\nPassword:", pwd)
    print("Strength:", strength_hint(length))


if __name__ == "__main__":
    main()
