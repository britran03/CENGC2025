import zipfile
from collections import deque
import conversions as conv


def generate_conversions():
    """Defines a list of transformation functions to be applied."""
    # Each item is a tuple: (name_of_transformation, function_lambda)
    transforms = []

    # String <-> Base64
    transforms.append(("String to Base64", lambda s: conv.convert_string_to_base64(s)))
    transforms.append(("Base64 to String", lambda s: conv.convert_base64_to_string(s)))

    # String <-> Number (Base 2, 10, 16)
    for base in [2, 10, 16]:
        transforms.append(
            (
                f"String to Base-{base}",
                lambda s, b=base: conv.convert_string_to_number(s, b),
            )
        )
        transforms.append(
            (
                f"Base-{base} to String",
                lambda s, b=base: conv.convert_number_to_string(s, b),
            )
        )

    # Number <-> Number (cross-base conversions)
    for from_b in [2, 10, 16, 64]:
        for to_b in [2, 10, 16, 64]:
            if from_b != to_b:
                transforms.append(
                    (
                        f"Base-{from_b} to Base-{to_b}",
                        lambda s, f=from_b, t=to_b: conv.convert_number_base(s, f, t),
                    )
                )

    return transforms


def test_transformations(
    zip_path: str, initial_string: str, max_depth: int = 3
) -> tuple[str, list[str]]:
    """
    Tries to find the password for a ZIP file by applying a chain of transformations.
    """
    try:
        zip_file = zipfile.ZipFile(zip_path)
    except (FileNotFoundError, zipfile.BadZipFile) as e:
        print(f"Couldn't open zip file: {e}")
        return "", [""]

    # Depth first search, with the input, depth, and conversion history
    queue = deque([(initial_string, 0, [])])
    # Keep track of values we've already tried to avoid redundant work
    tried_passwords = {initial_string}

    transformations = generate_conversions()

    while queue:
        current_val, depth, history = queue.popleft()

        try:
            zip_file.extractall(pwd=current_val.encode("utf-8"))
            print(f"Password found: {current_val}")
            print(f"Transformation chain: {' -> '.join(history) or 'None'}")
            return current_val, history
        except Exception:
            pass

        # Stop at the max search depth
        if depth >= max_depth:
            continue

        # Try a new transofmration on the data
        for name, func in transformations:
            try:
                new_val = func(current_val)
                # If transformation is successful and result is new
                if new_val and new_val not in tried_passwords:
                    tried_passwords.add(new_val)
                    new_history = history + [name]
                    queue.append((new_val, depth + 1, new_history))
                    print(f"  -> Queued: {' -> '.join(new_history)}")
            except Exception:
                continue

    print("Password not found within the specified depth.")
    return "", [""]
