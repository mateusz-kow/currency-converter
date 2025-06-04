#### Autor: Mateusz Kowalski

- `example_currency_rates.json` - lokalne źródło danych z kursami walut
- `database.json` - baza danych z zapisanymi kursami walut i wynikami przeliczeń (tryb dev).
- `database.db` - baza danych SQLite z zapisanymi kursami walut i wynikami przeliczeń (tryb prod).
- `app.log` - plik z logami działania aplikacji.
- `requirements.txt` - lista bibliotek wymaganych przez projekt.
- `task/__main__.py` - główny skrypt uruchomieniowy aplikacji.
- `task/currency_converter.py` - moduł odpowiedzialny za logikę przeliczania walut.
- `task/database_updater.py` - moduł odpowiedzialny za zapisywanie wyników do bazy danych.
- `task/connectors/database/json.py` - konektor do obsługi bazy danych w formacie JSON.
- `task/connectors/database/sql.py` - konektor do obsługi bazy danych SQLite przy użyciu SQLAlchemy.
- `task/connectors/source/local/file_reader.py` - konektor do odczytu kursów z pliku lokalnego.
- `task/connectors/source/remote/api_connector.py` - konektor do pobierania kursów z API NBP.
- `task/utils/args_parser.py` - moduł do parsowania argumentów wejściowych programu.
- `task/utils/config.py` - plik konfiguracyjny ścieżek i nazw plików.
- `tests/` - katalog zawierający testy jednostkowe.
