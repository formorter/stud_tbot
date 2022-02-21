from typing import Any, Dict, List, Union
from tinydb import Query, TinyDB


class Database():
    """Класс-обёртка `TinyDB`

    `Пример использования`:

    d = Database()

    d.insert({'field1':'value1', 'field2':'value2',...,'field_n':'value_n'})

    print(d.all()) # отобразить базу
    """
    def __init__(self, db: Union[TinyDB,str]=None) -> None:
        """Конструктор базы данных

        Args:
            `db (TinyDB | str, optional)`: Путь до базы данных или объект базы данных.
            При None, создает базу данных с путём `db.json`. По умолчанию `None`.
        """
        if not isinstance(db, TinyDB):
            if isinstance(db, str):
                db = TinyDB(db)
            elif not db:
                db = TinyDB('db.json')
        self._db = db

    def search(self, query: Union[Dict,Query]) -> List[Dict]:
        """Позволяет найти все вхождения в базе данных, по соответствующему запросу.
        Запрос выглядит как `{'field': 'value'}`.

        Args:
            `query (Dict | Query)`: Словарь пары поле-значение или объект запроса.

        Returns:
            `List[Dict]`: Словарь всех вхождений.
        """
        if not isinstance(query, Query):
            return self._db.search(Query()[list(query)[0]] == list(query.values())[0])
        return self._db.search(query)

    def all(self, field: str=None) -> List[Any]:
        """Возвращает все документы из базы данных или все значения поля.

        Args:
            `field (str, optional)`: `Опционально`. Возвращает все значения указанного поля.
            По умолчанию `None`.

        Returns:
            `List[Any]`: Список всех документов или список значений поля.
        """
        _all = self._db.all()
        if field:
            query = []
            for _ in _all:
                query.append(_[field])
            return query
        return _all

    def get(self, query: Union[Dict,Query]) -> Dict:
        """Возвращает первое вхождения документа из базы данных, по соответствующему запросу.
        Запрос выглядит как `{'field': 'value'}`.

        Args:
            `query (Dict | Query)`: Словарь пары поле-значение или объект запроса.

        Returns:
            `Dict`: Словарь найденного вхождения
        """
        if not isinstance(query, Query):
            return self._db.get(Query()[list(query)[0]] == list(query.values())[0])
        return self._db.get(query)

    def remove(self, query: Union[Dict,Query]):
        """Удаляет документ из базы данных, по соответствующему запросу.
        Запрос выглядит как `{'field': 'value'}`.

        Args:
            `query (Dict | Query)`:  Словарь пары поле-значение или объект запроса.
        """
        if not isinstance(query, Query):
            self._db.remove(Query()[list(query)[0]] == list(query.values())[0])
        self._db.remove(query)

    def update(self, fields: Dict, query: Union[Dict, Query]):
        """Изменяет документы в базе данных, удовлетворяющие запросу.
        Запрос выглядит как `{'field': 'value'}`.

        Args:
            `fields (Dict)`: Словарь новых данных.
            `query (Dict | Query)`: Словарь пары поле-значение или объект запроса.
        """
        if not isinstance(query, Query):
            self._db.update(fields, Query()[list(query)[0]] == list(query.values())[0])
        self._db.update(fields, query)

    def insert(self, fields: Union[Dict,List[Dict]]):
        """Добавляет в базу данных новый документ.

        Args:
            `fields (Dict)`: Новый документ.
        """
        if isinstance(fields, Dict):
            self._db.insert(fields)
        elif isinstance(fields, list):
            self._db.insert_multiple(fields)
        