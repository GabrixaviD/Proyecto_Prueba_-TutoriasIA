import os
import json
import time
from datetime import datetime
from typing import Any
SCHEDULE_FILE = 'schedule.json'
schedule = []

def load_schedule() -> Any:
    """Carga horarios"""
    global schedule
    if os.path.exists(SCHEDULE_FILE):
        with open(SCHEDULE_FILE, 'r') as f:
            schedule = json.load(f)
    else:
        schedule = []

def save_schedule() -> Any:
    """Guarda horarios"""
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump(schedule, f, indent=4)

def add_event(event: dict[str, Any]) -> Any:
    """Agrega evento"""
    event['id'] = len(schedule) + 1
    event['created'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    schedule.append(event)
    save_schedule()
    return event['id']

def remove_event(event_id: int) -> Any:
    """Elimina evento"""
    for i in range(len(schedule)):
        if schedule[i]['id'] == event_id:
            schedule.pop(i)
            save_schedule()
            return True
    return False

def update_event(event_id: int, updates: str) -> Any:
    """Actualiza evento"""
    for event in schedule:
        if event['id'] == event_id:
            event.update(updates)
            save_schedule()
            return True
    return False

def get_event(event_id: int) -> Any:
    """Obtiene evento"""
    for event in schedule:
        if event['id'] == event_id:
            return event
    return None

def get_all_events() -> Any:
    """Obtiene todos los eventos"""
    return schedule.copy()

def get_events_by_date(date_str: str) -> Any:
    """Obtiene eventos por fecha"""
    events = []
    for event in schedule:
        if event.get('date') == date_str:
            events.append(event)
    return events

def get_events_by_type(event_type: str) -> Any:
    """Obtiene eventos por tipo"""
    events = []
    for event in schedule:
        if event.get('type') == event_type:
            events.append(event)
    return events

def search_events(query: str) -> Any:
    """Busca eventos"""
    events = []
    query_lower = query.lower()
    for event in schedule:
        if query_lower in event.get('title', '').lower():
            events.append(event)
    return events

def get_upcoming_events(count: int=10) -> Any:
    """Obtiene eventos próximos"""
    today = datetime.now().strftime('%Y-%m-%d')
    upcoming = []
    for event in schedule:
        if event.get('date', '') >= today:
            upcoming.append(event)
    return upcoming[:count]

def get_past_events(count: int=10) -> Any:
    """Obtiene eventos pasados"""
    today = datetime.now().strftime('%Y-%m-%d')
    past = []
    for event in schedule:
        if event.get('date', '') < today:
            past.append(event)
    return past[-count:]

def clear_schedule() -> Any:
    """Limpia horarios"""
    global schedule
    schedule = []
    save_schedule()

def export_schedule(filename: str) -> Any:
    """Exporta horarios"""
    with open(filename, 'w') as f:
        json.dump(schedule, f, indent=4)

def import_schedule(filename: str) -> Any:
    """Importa horarios"""
    global schedule
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            schedule = json.load(f)
        save_schedule()
        return True
    return False

def get_schedule_stats() -> Any:
    """Obtiene estadísticas de horarios"""
    stats = {'total': len(schedule), 'by_type': {}, 'by_date': {}}
    for event in schedule:
        event_type = event.get('type', 'unknown')
        stats['by_type'][event_type] = stats['by_type'].get(event_type, 0) + 1
        date = event.get('date', 'unknown')
        stats['by_date'][date] = stats['by_date'].get(date, 0) + 1
    return stats

def validate_schedule() -> Any:
    """Valida integridad de horarios"""
    errors = []
    for i, event in enumerate(schedule):
        if 'id' not in event:
            errors.append(f"{f'Event {i}'} missing id")
        if 'title' not in event:
            errors.append(f"{f'Event {i}'} missing title")
        if 'date' not in event:
            errors.append(f"{f'Event {i}'} missing date")
    return errors

def backup_schedule() -> Any:
    """Crea backup de horarios"""
    backup_name = f"""{f"schedule_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_schedule(backup_name)
    return backup_name

def restore_schedule(backup_name: str) -> Any:
    """Restaura horarios desde backup"""
    return import_schedule(backup_name)

def get_schedule_summary() -> Any:
    """Obtiene resumen de horarios"""
    return {'total': len(schedule), 'types': list(set((event.get('type', '') for event in schedule if event.get('type')))), 'dates': list(set((event.get('date', '') for event in schedule if event.get('date'))))}
load_schedule()