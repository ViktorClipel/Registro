import tkinter as tk
from tkinter import messagebox
from src.core.database import DatabaseManager
from src.views.login_view import LoginWindow
from src.core.normalizador_semantico import SemanticNormalizer

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Bestiário')
        app_width = 800
        app_height = 600
        chart_width = 600
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        pos_y = int((screen_height / 2) - (app_height / 2))
        
        total_width = app_width + chart_width + 10 
        pos_x = int((screen_width / 2) - (total_width / 2))

        self.geometry(f'{app_width}x{app_height}+{pos_x}+{pos_y}')
        
        self.db_manager = DatabaseManager()  
        self.current_user = None
        self.chart_window = None
        
        self.normalizer = SemanticNormalizer(self.db_manager)
        
        self.withdraw()
        self.show_login_window()

    def show_login_window(self):
        login = LoginWindow(self)
        login.mainloop()

    def logout(self):
        if self.chart_window and self.chart_window.winfo_exists():
            self.chart_window.destroy()
            self.chart_window = None
        self.current_user = None
        if hasattr(self, 'main_frame') and self.main_frame.winfo_exists():
            self.main_frame.destroy()
        self.withdraw()
        self.show_login_window()

    def process_login(self, username, password):
        user_data = self.db_manager.check_user(username, password)
        
        if user_data:
            self.current_user = user_data
            
            for widget in self.winfo_children():
                if isinstance(widget, LoginWindow):
                    widget.destroy()

            from src.views.main_view import MainWindow
            
            self.deiconify() # Mostra a janela principal
            self.main_frame = MainWindow(self, user=user_data)
            self.main_frame.pack(fill='both', expand=True)
            self.refresh_species_list()
        else:
            messagebox.showerror("Login Falhou", "Usuário ou senha inválidos.")
            
    def process_registration(self, username, password, register_window):
        sucesso = self.db_manager.add_user(username, password)
        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!", parent=register_window)
            register_window.destroy()
            self.process_login(username, password) 
        else:
            messagebox.showerror("Erro", "Este nome de usuário já existe.", parent=register_window)

    def add_nova_especie(self, dados_especie):
        if not self.current_user:
            messagebox.showerror("Erro", "Nenhum usuário logado para associar à espécie.")
            return
        sucesso = self.db_manager.add_especie(dados_especie, self.current_user['id'])
        if sucesso:
            messagebox.showinfo("Sucesso", "Espécie adicionada com sucesso!")
            self.normalizer.update_canonical_terms()
            self.refresh_species_list()
            self.refresh_chart_if_open()
            self.main_frame.clear_form_fields()
        else:
            messagebox.showerror("Erro", "Não foi possível adicionar a espécie.")

    def refresh_species_list(self):
        all_species_data = self.db_manager.fetch_all_species()
        self.main_frame.populate_treeview(all_species_data)

    def fetch_species_details_for_form(self, species_id):
        species_data = self.db_manager.fetch_specie_by_id(species_id)
        if species_data:
            self.main_frame.populate_form_fields(species_data)

    def update_especie_selecionada(self, species_id, dados_especie):
        if not self.current_user:
            messagebox.showerror("Erro", "Nenhum usuário logado.")
            return
        sucesso = self.db_manager.update_especie(species_id, dados_especie)
        if sucesso:
            messagebox.showinfo("Sucesso", "Espécie atualizada com sucesso!")
            self.normalizer.update_canonical_terms()
            self.refresh_species_list()
            self.refresh_chart_if_open()
            self.main_frame.clear_form_fields()
        else:
            messagebox.showerror("Erro no Banco de Dados", "Não foi possível atualizar a espécie.")

    def delete_especie_selecionada(self, species_id):
        sucesso = self.db_manager.delete_especie(species_id)
        if sucesso:
            messagebox.showinfo("Sucesso", "Espécie excluída com sucesso!")
            self.normalizer.update_canonical_terms()
            self.refresh_species_list()
            self.main_frame.clear_form_fields()
            self.refresh_chart_if_open()
        else:
            messagebox.showerror("Erro no Banco de Dados", "Não foi possível excluir a espécie.")

    def show_classification_chart(self):
        from src.views.chart_view import ClassificationChartWindow

        if not self.current_user:
            messagebox.showerror("Erro", "Nenhum usuário logado.")
            return

        chart_data = self.db_manager.fetch_classification_counts(self.current_user['id'])
        
        if self.chart_window and self.chart_window.winfo_exists():
            self.chart_window.lift()
            return
        
        if chart_data:
            main_x = self.winfo_x()
            main_y = self.winfo_y()
            main_width = self.winfo_width()
            pos_x = main_x + main_width + 10
            pos_y = main_y
            chart_geometry = f'600x600+{pos_x}+{pos_y}'
            self.chart_window = ClassificationChartWindow(self, chart_data, geometry=chart_geometry)
            self.chart_window.protocol("WM_DELETE_WINDOW", self.on_chart_close)
        else:
            messagebox.showinfo("Sem Dados", "Não há espécies classificadas para gerar um gráfico.", parent=self)      

    def on_chart_close(self):
        self.chart_window.destroy()
        self.chart_window = None

    def refresh_chart_if_open(self):
        if self.chart_window and self.chart_window.winfo_exists() and self.current_user:
            new_chart_data = self.db_manager.fetch_classification_counts(self.current_user['id'])
            self.chart_window.update_chart(new_chart_data)