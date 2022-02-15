import ast
from random import choice
from requests import request
from typing import List

class Anecdot():
    """Библиотека позволяющая получить случайный анекдот
    `Типы`:
    1 - Анекдот;
    2 - Рассказы;
    3 - Стишки;
    4 - Афоризмы;
    5 - Цитаты;
    6 - Тосты;
    8 - Статусы;
    11 - Анекдот (+18);
    12 - Рассказы (+18);
    13 - Стишки (+18);
    14 - Афоризмы (+18);
    15 - Цитаты (+18);
    16 - Тосты (+18);
    18 - Статусы (+18);
    """
    def __init__(self, modes: List[int]=[1]) -> None:
        """Конструктор класса

        Args:
            `modes (List[int], optional)`: Лист типов анекдотов. По умолчанию [1].

        Raises:
            `Exception`: Неверный аргумент.
        """
        self._url = 'http://rzhunemogu.ru/RandJSON.aspx?CType='
        if isinstance(modes, list) and all(isinstance(x, int) for x in modes) and all(1<=x<=18 for x in modes):
            self._modes = modes
        else:
            raise Exception('Wrong Argument!')
        
    @property
    def modes(self) -> List[int]:
        """Поле типов.

        Returns:
            `List[int]`: возвращает список типов.
        """
        return self._modes

    @modes.setter
    def modes(self, values: List[int]):
        """Сеттер поля типов.

        Args:
           `values (List[int])`: Значения типов в списке.

        Raises:
            `Exception`: Неверный аргумент.
        """
        if isinstance(values, list):
            for _ in values:
                if not isinstance(_, int) or (1 <= _ <= 18):
                    raise Exception('Wrong Argument!')
        self._modes = values

    def get_random(self, mode: int=None) -> str:
        """Получение случайного анекдота.

        Args:
            `mode (int, optional)`: `Опционально.` Тип анекдота. По умолчанию None.

        Returns:
            str: Текст анекдота.
        """
        if mode and isinstance(mode, int) and (1 >=mode <= 18):
            r = request(method='GET', url=f'{self._url}{mode}')
        elif self.modes:
            r = request(method='GET', url=f'{self._url}{choice(self.modes)}')
        txt = r.text
        txt = txt.replace('{"content":"', '')
        txt = txt.replace('"}','')
        return txt
        
print('kinda sus')