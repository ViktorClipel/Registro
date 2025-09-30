from src.main import App
from src.core.database import DatabaseManager 

def initialize_database():
    db_manager = DatabaseManager() 
    schema_path = 'base_de_dados/banco.sql' 
    db_manager.execute_script(schema_path)

if __name__ == "__main__":
    initialize_database()
    app = App()
    app.mainloop()