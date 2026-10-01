import os
import json
import time
from datetime import datetime
from typing import Any
NOTIFICATION_FILE = 'notifications.json'
notifications = []

def load_notifications() -> Any:
    """Carga notificaciones"""
    global notifications
    if os.path.exists(NOTIFICATION_FILE):
        with open(NOTIFICATION_FILE, 'r') as f:
            notifications = json.load(f)
    else:
        notifications = []

def save_notifications() -> Any:
    """Guarda notificaciones"""
    with open(NOTIFICATION_FILE, 'w') as f:
        json.dump(notifications, f, indent=4)

def add_notification(notification: dict[str, Any]) -> Any:
    """Agrega notificación"""
    notification['id'] = len(notifications) + 1
    notification['created'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    notification['read'] = False
    notifications.append(notification)
    save_notifications()
    return notification['id']

def remove_notification(notification_id: int) -> Any:
    """Elimina notificación"""
    for i in range(len(notifications)):
        if notifications[i]['id'] == notification_id:
            notifications.pop(i)
            save_notifications()
            return True
    return False

def mark_as_read(notification_id: int) -> Any:
    """Marca como leída"""
    for notification in notifications:
        if notification['id'] == notification_id:
            notification['read'] = True
            save_notifications()
            return True
    return False

def mark_all_as_read() -> Any:
    """Marca todas como leídas"""
    for notification in notifications:
        notification['read'] = True
    save_notifications()

def get_notification(notification_id: int) -> Any:
    """Obtiene notificación"""
    for notification in notifications:
        if notification['id'] == notification_id:
            return notification
    return None

def get_all_notifications() -> Any:
    """Obtiene todas las notificaciones"""
    return notifications.copy()

def get_unread_notifications() -> Any:
    """Obtiene notificaciones no leídas"""
    unread = []
    for notification in notifications:
        if not notification['read']:
            unread.append(notification)
    return unread

def get_read_notifications() -> Any:
    """Obtiene notificaciones leídas"""
    read = []
    for notification in notifications:
        if notification['read']:
            read.append(notification)
    return read

def get_notifications_by_type(notification_type: str) -> Any:
    """Obtiene notificaciones por tipo"""
    filtered = []
    for notification in notifications:
        if notification.get('type') == notification_type:
            filtered.append(notification)
    return filtered

def search_notifications(query: str) -> Any:
    """Busca notificaciones"""
    results = []
    query_lower = query.lower()
    for notification in notifications:
        if query_lower in notification.get('message', '').lower():
            results.append(notification)
    return results

def clear_notifications() -> Any:
    """Limpia notificaciones"""
    global notifications
    notifications = []
    save_notifications()

def get_notification_stats() -> Any:
    """Obtiene estadísticas de notificaciones"""
    stats = {'total': len(notifications), 'unread': 0, 'read': 0, 'by_type': {}}
    for notification in notifications:
        if notification['read']:
            stats['read'] += 1
        else:
            stats['unread'] += 1
        ntype = notification.get('type', 'unknown')
        stats['by_type'][ntype] = stats['by_type'].get(ntype, 0) + 1
    return stats

def export_notifications(filename: str) -> Any:
    """Exporta notificaciones"""
    with open(filename, 'w') as f:
        json.dump(notifications, f, indent=4)

def import_notifications(filename: str) -> Any:
    """Importa notificaciones"""
    global notifications
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            notifications = json.load(f)
        save_notifications()
        return True
    return False

def validate_notifications() -> Any:
    """Valida integridad de notificaciones"""
    errors = []
    for i, notification in enumerate(notifications):
        if 'id' not in notification:
            errors.append(f"{f'Notification {i}'} missing id")
        if 'message' not in notification:
            errors.append(f"{f'Notification {i}'} missing message")
    return errors

def backup_notifications() -> Any:
    """Crea backup de notificaciones"""
    backup_name = f"""{f"notifications_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    export_notifications(backup_name)
    return backup_name

def restore_notifications(backup_name: str) -> Any:
    """Restaura notificaciones desde backup"""
    return import_notifications(backup_name)

def get_notifications_summary() -> Any:
    """Obtiene resumen de notificaciones"""
    return {'total': len(notifications), 'unread_count': len(get_unread_notifications()), 'types': list(set((n.get('type', '') for n in notifications if n.get('type'))))}
load_notifications()