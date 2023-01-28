from numpy import nan


def column_name_conv(name: str) -> str:
    return ''.join([f'_{n.lower()}' if n.isupper() else n for n in name])


def tconst_conv(tconst: str) -> int:
    return int(tconst[2:])


def list_conv(string: str) -> str:
    return string.split(',') if string != '\\N' else nan


def title_type_conv(string: str) -> str:
    return string.upper()
