"""
Генерирует .c файлы из bugs.json.

Использование (из корня проекта):
    python3 dataset/generate_files.py

Скрипт читает dataset/bugs.json, и для каждого бага создаёт пару файлов:
  dataset/files/<cwe>_bad.c
  dataset/files/<cwe>_good.c

Эти файлы потом используются в src/rules/validator.py для проверки
сгенерированных правил cppcheck.
"""

import json
import os
import sys


def main() -> int:
    # Скрипт лежит внутри dataset/, корень проекта — на уровень выше.
    here = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(here)

    bugs_json = os.path.join(here, "bugs.json")
    files_dir = os.path.join(here, "files")

    if not os.path.exists(bugs_json):
        print(f"Не найден {bugs_json}", file=sys.stderr)
        return 1

    with open(bugs_json, encoding="utf-8") as f:
        bugs = json.load(f)

    os.makedirs(files_dir, exist_ok=True)

    created = 0
    for bug in bugs:
        # bug["bad_file"] хранится как "dataset/files/cwe123_bad.c", т.е.
        # путь относительно корня проекта. Превращаем в абсолютный.
        bad_path = os.path.join(project_root, bug["bad_file"])
        good_path = os.path.join(project_root, bug["good_file"])

        os.makedirs(os.path.dirname(bad_path), exist_ok=True)
        os.makedirs(os.path.dirname(good_path), exist_ok=True)

        with open(bad_path, "w", encoding="utf-8") as f:
            f.write(bug["bad_code"])
            if not bug["bad_code"].endswith("\n"):
                f.write("\n")

        with open(good_path, "w", encoding="utf-8") as f:
            f.write(bug["good_code"])
            if not bug["good_code"].endswith("\n"):
                f.write("\n")

        created += 2
        print(f"  [{bug['id']:10}] {bad_path}")
        print(f"  [{bug['id']:10}] {good_path}")

    print()
    print(f"Готово. Создано файлов: {created} (по 2 на каждый из {len(bugs)} багов)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
