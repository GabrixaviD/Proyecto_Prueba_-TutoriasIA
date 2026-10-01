import os
import json
import csv
from datetime import datetime
from typing import Any
EXPORT_DIR = 'exports'
IMPORT_DIR = 'imports'

def init_dirs() -> Any:
    """Inicializa directorios"""
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
    if not os.path.exists(IMPORT_DIR):
        os.makedirs(IMPORT_DIR)

def export_to_json(data: dict[str, Any], filename: str) -> Any:
    """Exporta datos a JSON"""
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    return filepath

def import_from_json(filename: str) -> Any:
    """Importa datos desde JSON"""
    filepath = os.path.join(EXPORT_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def export_to_csv(data: dict[str, Any], filename: str) -> Any:
    """Exporta datos a CSV"""
    filepath = os.path.join(EXPORT_DIR, filename)
    if isinstance(data, list) and len(data) > 0:
        if isinstance(data[0], dict):
            with open(filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return filepath
    return None

def import_from_csv(filename: str) -> Any:
    """Importa datos desde CSV"""
    filepath = os.path.join(EXPORT_DIR, filename)
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    return data

def export_to_txt(data: dict[str, Any], filename: str) -> Any:
    """Exporta datos a TXT"""
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w') as f:
        if isinstance(data, list):
            for item in data:
                f.write(f'{item}\n')
        else:
            f.write(str(data))
    return filepath

def import_from_txt(filename: str) -> Any:
    """Importa datos desde TXT"""
    filepath = os.path.join(EXPORT_DIR, filename)
    data = []
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                data.append(line.strip())
    return data

def list_exports() -> Any:
    """Lista archivos de exportación"""
    files = []
    if os.path.exists(EXPORT_DIR):
        for filename in os.listdir(EXPORT_DIR):
            filepath = os.path.join(EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({'name': filename, 'size': stat.st_size, 'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')})
    return files

def delete_export(filename: str) -> Any:
    """Elimina archivo de exportación"""
    filepath = os.path.join(EXPORT_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False

def get_export_info(filename: str) -> Any:
    """Obtiene información de exportación"""
    filepath = os.path.join(EXPORT_DIR, filename)
    if os.path.exists(filepath):
        stat = os.stat(filepath)
        return {'name': filename, 'size': stat.st_size, 'created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'), 'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}
    return None

def copy_export(filename: str, destination: str) -> Any:
    """Copia exportación a otra ubicación"""
    source_path = os.path.join(EXPORT_DIR, filename)
    dest_path = os.path.join(destination, filename)
    if os.path.exists(source_path):
        import shutil
        shutil.copy2(source_path, dest_path)
        return True
    return False

def move_export(filename: str, destination: str) -> Any:
    """Mueve exportación a otra ubicación"""
    source_path = os.path.join(EXPORT_DIR, filename)
    dest_path = os.path.join(destination, filename)
    if os.path.exists(source_path):
        import shutil
        shutil.move(source_path, dest_path)
        return True
    return False

def create_backup(backup_name: str | None=None) -> Any:
    """Crea backup de todas las exportaciones"""
    if backup_name is None:
        backup_name = f"""{f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"}.json"""
    backup_path = os.path.join(EXPORT_DIR, backup_name)
    all_exports = {}
    if os.path.exists(EXPORT_DIR):
        for filename in os.listdir(EXPORT_DIR):
            filepath = os.path.join(EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as f:
                    all_exports[filename] = f.read()
    with open(backup_path, 'w') as f:
        json.dump(all_exports, f, indent=4)
    return backup_path

def restore_backup(backup_name: str) -> Any:
    """Restaura backup de exportaciones"""
    backup_path = os.path.join(EXPORT_DIR, backup_name)
    if os.path.exists(backup_path):
        with open(backup_path, 'r') as f:
            all_exports = json.load(f)
        for filename, content in all_exports.items():
            filepath = os.path.join(EXPORT_DIR, filename)
            with open(filepath, 'w') as f:
                f.write(content)
        return True
    return False

def get_total_export_size() -> Any:
    """Obtiene tamaño total de exportaciones"""
    total_size = 0
    if os.path.exists(EXPORT_DIR):
        for filename in os.listdir(EXPORT_DIR):
            filepath = os.path.join(EXPORT_DIR, filename)
            if os.path.isfile(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def export_data_report(data: dict[str, Any], filename: str) -> Any:
    """Exporta reporte de datos"""
    filepath = os.path.join(EXPORT_DIR, filename)
    with open(filepath, 'w') as f:
        f.write('REPORTE DE DATOS\n')
        f.write(f"{'=' * 50}\n")
        f.write(f"""{f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}\n""")
        f.write(f"{'=' * 50}\n\n")
        if isinstance(data, dict):
            for key, value in data.items():
                f.write(f'{key.upper()}:\n')
                f.write(f"{'-' * 30}\n")
                if isinstance(value, list):
                    for item in value:
                        f.write(f"{f'  - {item}'}\n")
                else:
                    f.write(f"{f'  {value}'}\n")
                f.write('\n')
        else:
            f.write(f'{data}\n')
    return filepath
init_dirs()