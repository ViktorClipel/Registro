from src.main import App
from src.core.database import DatabaseManager 
from src.config import DATABASE_NAME

def initialize_database():
    db_manager = DatabaseManager(db_name=DATABASE_NAME)
    schema_path = 'base_de_dados/banco.sql' 
    db_manager.execute_script(schema_path)

if __name__ == "__main__":
    initialize_database()
    app = App()
    app.mainloop()