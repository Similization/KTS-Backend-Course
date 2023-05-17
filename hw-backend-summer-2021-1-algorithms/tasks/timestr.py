__all__ = (
    'seconds_to_str',
)


def seconds_to_str(seconds: int) -> str:
    """
    Функция должна вернуть текстовое представление времени
    20 -> 20s
    60 -> 01m00s
    65 -> 01m05s
    3700 -> 01h01m40s
    93600 -> 01d02h00m00s
    """
    result: str = ''
    minutes: int = int(seconds / 60)
    hours: int = int(minutes / 60)
    days: int = int(hours / 24)

    if days:
        result += '{:02d}d'.format(days)
        result += '{:02d}h'.format(hours % 24)
        result += '{:02d}m'.format(minutes % 60)
    elif hours % 24:
        result += '{:02d}h'.format(hours % 24)
        result += '{:02d}m'.format(minutes % 60)
    elif minutes % 60:
        result += '{:02d}m'.format(minutes % 60)
    return result + '{:02d}s'.format(seconds % 60)

print(seconds_to_str(93600))
