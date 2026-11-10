"""Deterministic assessment and planning of a developer's IDE migration."""
from dataclasses import dataclass, asdict
import json

CHECKS = (
    ('backup', 'Сохранить настройки старой среды', 3),
    ('extensions', 'Перенести необходимые расширения', 2),
    ('shortcuts', 'Сопоставить горячие клавиши', 2),
    ('project', 'Открыть проект и проверить пути', 3),
    ('runtime', 'Настроить интерпретатор и зависимости', 3),
    ('formatter', 'Настроить единый стиль форматирования', 2),
    ('debugger', 'Настроить точки останова и запуск', 3),
    ('tests', 'Запустить проектные тесты', 3),
    ('vcs', 'Проверить операции Git', 2),
    ('docs', 'Обновить инструкцию разработки', 1),
)

@dataclass(frozen=True)
class Progress:
    code: str
    done: bool


def normalize(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError('Expected text')
    return ' '.join(value.strip().lower().split())


def analyze(progress: list[Progress]) -> dict:
    if not isinstance(progress, list):
        raise TypeError('Expected list')
    status = {}
    allowed = {code for code, _, _ in CHECKS}
    for item in progress:
        if not isinstance(item, Progress) or item.code not in allowed:
            raise ValueError('Unknown check')
        if not isinstance(item.done, bool):
            raise TypeError('done must be bool')
        if item.code in status:
            raise ValueError('Duplicate check')
        status[item.code] = item.done
    total = sum(weight for _, _, weight in CHECKS)
    complete = sum(weight for code, _, weight in CHECKS if status.get(code, False))
    return {'complete_weight': complete, 'total_weight': total,
            'percent': round(100 * complete / total, 1),
            'completed': sum(status.get(code, False) for code, _, _ in CHECKS),
            'total': len(CHECKS)}


def make_plan(progress: list[Progress]) -> list[dict]:
    analyze(progress)
    status = {p.code: p.done for p in progress}
    return [{'code': code, 'step': name, 'priority': weight}
            for code, name, weight in CHECKS if not status.get(code, False)]


def export_json(progress: list[Progress]) -> str:
    return json.dumps({'assessment': analyze(progress), 'remaining': make_plan(progress)},
                      ensure_ascii=False, indent=2)
