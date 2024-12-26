
# Проект "msg_split"

## Запуск проекта

1. Установите зависимости с помощью Poetry:
   ```bash
   poetry install
   ```

2. Запустите основной скрипт:
   ```bash
   poetry run python ./msg_split.py --max-len=4096 ./html/test.html
   ```
   - Путь к файлу и максимальную длину можно изменить в командной строке.

## Запуск тестов

Чтобы запустить тесты, выполните команду:

```bash
poetry run python ./tests/test_msg_split.py
```

## Модули проекта

### Модуль HTML

Содержит тестовые файлы HTML для скрипта.

### Модуль Tests

Содержит файлы для юнит-тестов (в рамках тестового задания на данный момент содержится только 1 файл).

### Модуль Utils

Содержит утилитарные функции, которые могут быть использованы повторно в других частях проекта.

### Файл msg_split

Основной исполняемый файл, который содержит две ключевые функции:

- **split_message**: Функция для обработки валидности данных.
  
- **soap_loop**: Основная функция, работающая методом реверсивного вычленения данных из файла. Она рекурсивно проходит по дереву элементов, вставляя элементы, если они удовлетворяют условиям длины. В противном случае, если элемент является тегом и находится в белом списке, функция запускается снова внутри этого тега. Если элемент — это текст или тег-исключение, возвращается текущее положение. 

  Перед запуском функции добавляется стартовый тег, так как функция может рекурсивно запуститься, только если нет возможности вставить тег полностью. По завершении функции добавляется закрывающий тег по аналогичным соображениям.

## Автор

**SoulLution (Vitaliy Podkutin)**



## Running the Project

1. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

2. Run the main script:
   ```bash
   poetry run python ./msg_split.py --max-len=4096 ./html/test.html
   ```
   - The file path and maximum length can be modified via the command line.

## Running Tests

To run the tests, execute the following command:

```bash
poetry run python ./tests/test_msg_split.py
```

## Project Modules

### HTML Module

Contains test HTML files for the script.

### Tests Module

Contains unit test files (currently, the test folder contains only 1 file as part of the test task).

### Utils Module

Contains utility functions that can potentially be reused in other parts of the project.

### msg_split File

The main executable file, which contains two key functions:

- **split_message**: Function to validate the data.
  
- **soap_loop**: The main function that works by reverse extraction of data from the file. It recursively traverses the element tree, inserting elements if they meet the length conditions. If not, and if the element is a tag in the whitelist, it restarts inside the tag. If the element is text or an exclusion tag, it returns the current position. 

  Before the function starts, a starting tag is added because the function can only be executed recursively if it’s not possible to fully insert the tag. After the function finishes, a closing tag is added for the same reason.

## Author

**SoulLution (Vitaliy Podkutin)**
