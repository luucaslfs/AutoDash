import uuid
import threading
import time

# Dicionário para armazenar o estado: {uuid: {'code': ..., 'timestamp': ...}}
state_store = {}
lock = threading.Lock()

# Tempo de expiração em segundos (e.g., 1 hora)
EXPIRATION_TIME = 3600

def generate_unique_id():
    return uuid.uuid4().hex

def store_dashboard_code(code, preview_data):
    unique_id = generate_unique_id()
    with lock:
        state_store[unique_id] = {'code': code, 'table_data': preview_data, 'timestamp': time.time()}
    return unique_id

def get_dashboard_code(unique_id):
    with lock:
        data = state_store.get(unique_id)
        if data:
            return data['code']
        return None

def get_table_data(unique_id):
    with lock:
        data = state_store.get(unique_id)
        if data:
            return data.get('table_data')
        return None

def cleanup_expired_entries():
    while True:
        time.sleep(600)  # Verifica a cada 10 minutos
        current_time = time.time()
        with lock:
            expired_keys = [key for key, value in state_store.items() if current_time - value['timestamp'] > EXPIRATION_TIME]
            for key in expired_keys:
                del state_store[key]
