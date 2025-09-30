import tkinter as tk
from tkinter import ttk, messagebox

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = parent.controller

        self.title("Cadastro de Novo Usuário")
        self.geometry("350x220")
        self.resizable(False, False)
        self.grab_set()
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()
        ttk.Label(main_frame, text="Novo Usuário:").pack(fill="x", padx=5, pady=2)
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var)
        username_entry.pack(fill="x", padx=5, pady=2)
        username_entry.focus()
        ttk.Label(main_frame, text="Senha:").pack(fill="x", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=self.password_var, show="*").pack(fill="x", padx=5, pady=2)
        ttk.Label(main_frame, text="Confirmar Senha:").pack(fill="x", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=self.confirm_password_var, show="*").pack(fill="x", padx=5, pady=2)
        ttk.Button(main_frame, text="Cadastrar", command=self.attempt_register).pack(pady=15)
        self.bind('<Return>', lambda event=None: self.attempt_register())

    def attempt_register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()
        if not username or not password or not confirm_password:
            messagebox.showwarning("Campos Vazios", "Todos os campos são obrigatórios.", parent=self)
            return
        if password != confirm_password:
            messagebox.showerror("Erro", "As senhas não coincidem.", parent=self)
            return
        self.controller.process_registration(username, password, self)
        
    def on_closing(self):
        """Quando a janela de cadastro é fechada, reexibe a de login."""
        self.master.deiconify()
        self.destroy()