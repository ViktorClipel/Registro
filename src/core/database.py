import sqlite3
from .logger import log_error
from src.config import DATABASE_NAME

class DatabaseManager:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            log_error(e)
            print(f"Ocorreu um erro ao conectar ao SQLite: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            
    def execute_script(self, file_path):
        try:
            self._connect()
            with open(file_path, 'r', encoding='utf-8') as sql_file:
                sql_script = sql_file.read()
            self.cursor.executescript(sql_script)
            self.connection.commit()
            print(f"Script '{file_path}' executado com sucesso.")
        except sqlite3.Error as e:
            log_error(e)
            print(f"Erro ao executar o script: {e}")
        finally:
            self.close()

    def add_especie(self, dados_especie, user_id):
        sql = "INSERT INTO especies (nome_popular, classificacao, descricao_fisica, comportamento, populacao_estimada, dados_adicionais, id_criador) VALUES (?, ?, ?, ?, ?, ?, ?)"
        try:
            self._connect()
            dados_completos = dados_especie + (user_id,)
            self.cursor.execute(sql, dados_completos)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(e)
            return False
        finally:
            self.close()

    def fetch_all_species(self):
        sql = "SELECT id, nome_popular, classificacao, id_criador FROM especies"
        records = []
        try:
            self._connect()
            self.connection.row_factory = None
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
        except sqlite3.Error as e:
            log_error(e)
        finally:
            self.close()
        return records
        
    def fetch_specie_by_id(self, species_id):
        sql = "SELECT * FROM especies WHERE id = ?"
        record = None
        try:
            self._connect()
            self.cursor.execute(sql, (species_id,))
            record = self.cursor.fetchone()
        except sqlite3.Error as e:
            log_error(e)
        finally:
            self.close()
        return dict(record) if record else None

    def update_especie(self, species_id, dados_especie):
        sql = "UPDATE especies SET nome_popular = ?, classificacao = ?, descricao_fisica = ?, comportamento = ?, populacao_estimada = ?, dados_adicionais = ? WHERE id = ?"
        try:
            self._connect()
            dados_completos = dados_especie + (species_id,)
            self.cursor.execute(sql, dados_completos)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            log_error(e)
            return False
        finally:
            self.close()

    def delete_especie(self, species_id):
        sql = "DELETE FROM especies WHERE id = ?"
        try:
            self._connect()
            self.cursor.execute(sql, (species_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            log_error(e)
            return False
        finally:
            self.close()

    def add_user(self, username, password):
        sql = "INSERT INTO usuarios (nome_usuario, senha) VALUES (?, ?)"
        try:
            self._connect()
            self.cursor.execute(sql, (username, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            log_error(f"Tentativa de criar usuário duplicado: {username}")
            return False
        except sqlite3.Error as e:
            log_error(f"Erro ao adicionar usuário '{username}': {e}")
            return False
        finally:
            self.close()
            
    def check_user(self, username, password):
        sql = "SELECT * FROM usuarios WHERE nome_usuario = ? AND senha = ?"
        user = None
        try:
            self._connect()
            self.cursor.execute(sql, (username, password))
            user = self.cursor.fetchone()
        except sqlite3.Error as e:
            log_error(f"Erro ao verificar usuário: {e}")
        finally:
            self.close()
        return dict(user) if user else None

    def fetch_unique_classifications(self):
        sql = "SELECT DISTINCT classificacao FROM especies WHERE classificacao IS NOT NULL AND classificacao != ''"
        records = []
        try:
            self._connect()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            records = [row['classificacao'] for row in rows]
        except sqlite3.Error as e:
            log_error(e)
        finally:
            self.close()
        return records
    
    def fetch_classification_counts(self, user_id):
        sql = "SELECT classificacao, COUNT(*) FROM especies WHERE id_criador = ? AND classificacao IS NOT NULL AND classificacao != '' GROUP BY classificacao ORDER BY COUNT(*) DESC"
        records = []
        try:
            self._connect()
            self.connection.row_factory = None
            self.cursor = self.connection.cursor()
            self.cursor.execute(sql, (user_id,))
            records = self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar contagem de classificações: {e}")
        finally:
            self.close()
        return records