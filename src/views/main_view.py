import tkinter as tk
from tkinter import ttk, messagebox

class MainWindow(ttk.Frame):
    def __init__(self, parent, user):
        super().__init__(parent)
        self.user = user
        self.controller = parent
        self.selected_species_id = None

        input_frame = ttk.LabelFrame(self, text="Gerenciar Espécie")
        input_frame.pack(fill="x", padx=10, pady=10)

        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.entry_vars = {
            "nome_popular": tk.StringVar(), "classificacao": tk.StringVar(),
            "descricao_fisica": tk.StringVar(), "comportamento": tk.StringVar(),
            "populacao_estimada": tk.StringVar(), "dados_adicionais": tk.StringVar()
        }
        labels_texts = ["Nome Popular:", "Classificação:", "Descrição Física:", "Comportamento:", "População Estimada:", "Dados Adicionais:"]

        for i, (key, text) in enumerate(zip(self.entry_vars.keys(), labels_texts)):
            label = ttk.Label(input_frame, text=text)
            label.grid(row=i+1, column=0, columnspan=2, padx=5, pady=2, sticky="w")
            entry = ttk.Entry(input_frame, textvariable=self.entry_vars[key], width=50)
            entry.grid(row=i+1, column=2, columnspan=2, padx=5, pady=2, sticky="ew")

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=len(labels_texts)+1, column=0, columnspan=5, pady=10)

        ttk.Button(button_frame, text="Adicionar Nova", command=self.on_add_button_clicked).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Atualizar Selecionada", command=self.on_update_button_clicked).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Excluir Selecionada", command=self.on_delete_button_clicked).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Ver Gráfico", command=self.controller.show_classification_chart).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Logout", command=self.on_logout_button_clicked).pack(side="left", padx=5)

        columns = ("id", "nome_popular", "classificacao")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nome_popular", text="Nome Popular")
        self.tree.heading("classificacao", text="Classificação")
        self.tree.column("id", width=50, stretch=tk.NO)
        
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_item_selected)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_item_selected(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            record_id = item['values'][0]
            self.selected_species_id = record_id
            self.controller.fetch_species_details_for_form(record_id)

    def populate_form_fields(self, species_data):
        if species_data:
            self.entry_vars["nome_popular"].set(species_data.get("nome_popular", ""))
            self.entry_vars["classificacao"].set(species_data.get("classificacao", ""))
            self.entry_vars["descricao_fisica"].set(species_data.get("descricao_fisica", ""))
            self.entry_vars["comportamento"].set(species_data.get("comportamento", ""))
            self.entry_vars["populacao_estimada"].set(species_data.get("populacao_estimada", ""))
            self.entry_vars["dados_adicionais"].set(species_data.get("dados_adicionais", ""))
    
    def on_add_button_clicked(self):
        nome = self.entry_vars["nome_popular"].get()
        if not nome:
            messagebox.showwarning("Campo Obrigatório", "O campo 'Nome Popular' é obrigatório.")
            return

        classificacao_raw = self.entry_vars["classificacao"].get()
        classificacao_normalizada = self.controller.normalizer.normalize(classificacao_raw) if classificacao_raw else ""

        dados_tupla = (
            nome,
            classificacao_normalizada,
            self.entry_vars["descricao_fisica"].get(),
            self.entry_vars["comportamento"].get(),
            self.entry_vars["populacao_estimada"].get(),
            self.entry_vars["dados_adicionais"].get()
        )
        
        self.controller.add_nova_especie(dados_tupla)
        self.clear_form_fields()

    def on_update_button_clicked(self):
        if self.selected_species_id is None:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma espécie na lista para atualizar.")
            return
        
        classificacao_raw = self.entry_vars["classificacao"].get()
        classificacao_normalizada = self.controller.normalizer.normalize(classificacao_raw)
        
        dados_tupla = (
            self.entry_vars["nome_popular"].get(),
            classificacao_normalizada,
            self.entry_vars["descricao_fisica"].get(),
            self.entry_vars["comportamento"].get(),
            self.entry_vars["populacao_estimada"].get(),
            self.entry_vars["dados_adicionais"].get()
        )
        
        self.controller.update_especie_selecionada(self.selected_species_id, dados_tupla)

    def on_delete_button_clicked(self):
        if self.selected_species_id is None:
            messagebox.showwarning("Nenhuma Seleção", "Por favor, selecione uma espécie na lista para excluir.")
            return
        
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir a espécie selecionada?"):
            self.controller.delete_especie_selecionada(self.selected_species_id)

    def on_logout_button_clicked(self):
        self.controller.logout()

    def populate_treeview(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for record in data:
            if record[3] == self.user.get('id'):
                self.tree.insert("", tk.END, values=record[:3])

    def clear_form_fields(self):
        for var in self.entry_vars.values():
            var.set("")
        self.selected_species_id = None
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection()[0])