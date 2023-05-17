__all__ = (
    'even_odd',
)


def even_odd(arr: list[int]) -> float:
    """
    Функция возвращает отношение суммы четных элементов массив к сумме нечетных
    Пример:
    even_odd([1, 2, 3, 4, 5]) == 0.8889
    """
    odd_sum: int = 0
    even_sum: int = 0
    for num in arr:
        if num % 2 == 0:
            odd_sum += num
        else:
            even_sum += num
    if odd_sum == 0 or even_sum == 0:
        return 0
    return odd_sum / even_sum
