import tkinter as tk
from tkinter import ttk, messagebox
from .register_view import RegisterWindow

class LoginWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = parent

        self.title("Login de Usuário")
        self.geometry("300x180")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.grab_set()

        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        ttk.Label(main_frame, text="Usuário:").pack(fill="x", padx=5, pady=2)
        username_entry = ttk.Entry(main_frame, textvariable=self.username_var)
        username_entry.pack(fill="x", padx=5, pady=2)
        username_entry.focus()

        ttk.Label(main_frame, text="Senha:").pack(fill="x", padx=5, pady=2)
        ttk.Entry(main_frame, textvariable=self.password_var, show="*").pack(fill="x", padx=5, pady=2)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Entrar", command=self.attempt_login).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cadastrar", command=self.open_register_window).pack(side="left", padx=5)
        
        self.bind('<Return>', lambda event=None: self.attempt_login())

    def attempt_login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        if not username or not password:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha o usuário e a senha.")
            return
        self.controller.process_login(username, password)
        
    def open_register_window(self):
        """Abre a janela de cadastro e esconde a de login."""
        self.withdraw()
        register = RegisterWindow(self)
        register.mainloop()

    def on_closing(self):
        self.controller.quit()