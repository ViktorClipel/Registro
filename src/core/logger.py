from datetime import datetime

def log_error(error_message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] - ERRO: {error_message}\n"
    
    try:
        with open('error.log', 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry)
    except IOError as e:
        print(f"Falha ao escrever no arquivo de log: {e}")