def validar_strings(strings: str) -> bool:
    strings = strings.strip()
    return (len(strings) > 0 and len(strings) <= 255)

def validar_int(intergers: str) -> bool:
    try:
        numero = int(intergers)
        return numero >= 0
    except ValueError:
        return False

def validar_float(floats: str) -> bool:
    try:
        numero = float(floats)
        return numero >= 0
    except ValueError:
        return False

