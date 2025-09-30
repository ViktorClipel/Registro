import mysql.connector
from mysql.connector import errors
from .logger import log_error 
from src.config import MYSQL_CONFIG

class DatabaseManager:
    def __init__(self):
        self.config = MYSQL_CONFIG
        self.connection = None
        self.cursor = None

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
        except errors.Error as e:
            log_error(e)
            print(f"Ocorreu um erro ao conectar ao MySQL: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
            
    def execute_script(self, file_path):
        try:
            self._connect()
            with open(file_path, 'r', encoding='utf-8') as sql_file:
                sql_commands = sql_file.read().split(';')
                for command in sql_commands:
                    if command.strip() != '':
                        self.cursor.execute(command)
            self.connection.commit()
            print(f"Script '{file_path}' executado com sucesso no MySQL.")
        except errors.Error as e:
            log_error(e)
            print(f"Erro ao executar o script no MySQL: {e}")
        finally:
            self.close()
            
    def add_especie(self, dados_especie, user_id):
        sql = "INSERT INTO especies (nome_popular, classificacao, descricao_fisica, comportamento, populacao_estimada, dados_adicionais, id_criador) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        try:
            self._connect()
            dados_completos = dados_especie + (user_id,)
            self.cursor.execute(sql, dados_completos)
            self.connection.commit()
            return True
        except errors.Error as e:
            log_error(e); return False
        finally: self.close()

    def fetch_all_species(self):
        sql = "SELECT id, nome_popular, classificacao, id_criador FROM especies"
        try:
            self._connect()
            self.cursor.execute(sql)
            records = self.cursor.fetchall()
            return [tuple(row.values()) for row in records]
        except errors.Error as e:
            log_error(e); return []
        finally: self.close()
        
    def fetch_specie_by_id(self, species_id):
        sql = "SELECT * FROM especies WHERE id = %s"
        try:
            self._connect()
            self.cursor.execute(sql, (species_id,))
            return self.cursor.fetchone()
        except errors.Error as e:
            log_error(e); return None
        finally: self.close()

    def update_especie(self, species_id, dados_especie):
        sql = "UPDATE especies SET nome_popular = %s, classificacao = %s, descricao_fisica = %s, comportamento = %s, populacao_estimada = %s, dados_adicionais = %s WHERE id = %s"
        try:
            self._connect()
            self.cursor.execute(sql, dados_especie + (species_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except errors.Error as e:
            log_error(e); return False
        finally: self.close()

    def delete_especie(self, species_id):
        sql = "DELETE FROM especies WHERE id = %s"
        try:
            self._connect()
            self.cursor.execute(sql, (species_id,))
            self.connection.commit()
            return True
        except errors.Error as e:
            log_error(e); return False
        finally: self.close()

    def add_user(self, username, password):
        sql = "INSERT INTO usuarios (nome_usuario, senha) VALUES (%s, %s)"
        try:
            self._connect()
            self.cursor.execute(sql, (username, password))
            self.connection.commit()
            return True
        except errors.IntegrityError:
            log_error(f"Usuário duplicado: {username}"); return False
        except errors.Error as e:
            log_error(f"Erro ao adicionar usuário: {e}"); return False
        finally: self.close()
            
    def check_user(self, username, password):
        sql = "SELECT * FROM usuarios WHERE nome_usuario = %s AND senha = %s"
        try:
            self._connect()
            self.cursor.execute(sql, (username, password))
            return self.cursor.fetchone()
        except errors.Error as e:
            log_error(f"Erro ao verificar usuário: {e}"); return None
        finally: self.close()

    def fetch_unique_classifications(self):
        sql = "SELECT DISTINCT classificacao FROM especies WHERE classificacao IS NOT NULL AND classificacao != ''"
        try:
            self._connect()
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            return [row['classificacao'] for row in rows]
        except errors.Error as e:
            log_error(e); return []
        finally: self.close()
    
    def fetch_classification_counts(self, user_id):
        sql = "SELECT classificacao, COUNT(*) as count FROM especies WHERE id_criador = %s AND classificacao IS NOT NULL AND classificacao != '' GROUP BY classificacao ORDER BY count DESC"
        try:
            self._connect()
            self.cursor.execute(sql, (user_id,))
            rows = self.cursor.fetchall()
            return [(row['classificacao'], row['count']) for row in rows]
        except errors.Error as e:
            print(f"Erro ao buscar contagem: {e}"); return []
        finally: self.close()