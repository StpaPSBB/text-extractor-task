# text-extractor-task

## Установка зависимостей
```bash
  python -m venv venv
  source /venv/bin/activate #или для Windows: source \venv\scripts\activate 
  pip install -r requirements.txt
```

## Запуск скрипта в режиме с интерфейсом
```bash
  python text_extractor_script.py -ui
```

## Запуск скрипта в консольном режиме
```bash
  python text_extractor_script.py -path /path/to/dir /path/to/file
```

## Структура 
```
text-extractor-task/
├── text_extractor_script.py           # основной скрипт для извлечения кадров
├── frames/                    # кадры фильма для обработки
├── result.txt                 # результат обработки
├── .gitignore
├── requirements.txt           # зависимости проекта
└── README.md
```