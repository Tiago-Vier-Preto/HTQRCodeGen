import customtkinter as ctk
from tkinter import filedialog
import os
import src.halftone as halftone

class Window(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HTQRCodeGen")
        self.geometry("700x500")
        self.configure(bg="#2E3440")  # Background color

        # Frame para centralizar os widgets
        self.main_frame = ctk.CTkFrame(self, fg_color="#3B4252")
        self.main_frame.pack(fill="both", expand=True)

        # Label de título
        self.title_label = ctk.CTkLabel(
            self.main_frame, text="HTQRCodeGen", font=("Arial", 24, "bold"), text_color="#88C0D0"
        )
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        # Botão para selecionar imagem
        self.image_button = ctk.CTkButton(
            self.main_frame, text="Select Image Input", command=self.select_image,
            fg_color="#88C0D0", text_color="#2E3440", width=200
        )
        self.image_button.grid(row=1, column=0, columnspan=2, pady=10)

        # Label para exibir o caminho da imagem selecionada
        self.image_label = ctk.CTkLabel(self.main_frame, text="", text_color="#D8DEE9", wraplength=400)
        self.image_label.grid(row=2, column=0, columnspan=2, pady=5)

        # Entrada de texto para data string
        self.data_string = ctk.CTkEntry(
            self.main_frame, placeholder_text="Data String", fg_color="#4C566A", text_color="#D8DEE9"
        )
        self.data_string.grid(row=3, column=0, columnspan=2, pady=10)

        # Dropdown para nível de erro
        self.error_label = ctk.CTkLabel(self.main_frame, text="Redundancy (error correction level):", text_color="#D8DEE9")
        self.error_label.grid(row=4, column=0, columnspan=2, pady=(10, 5))

        self.dropdown_var = ctk.StringVar(value="High (30%)")
        self.dropdown_menu = ctk.CTkOptionMenu(
            self.main_frame,
            variable=self.dropdown_var,
            values=["Low (7%)", "Medium (15%)", "Quartile (25%)", "High (30%)"],
            fg_color="#4C566A",
            text_color="#D8DEE9",
            width=200,
        )
        self.dropdown_menu.grid(row=5, column=0, columnspan=2, pady=10)

        # Switch para QRCode colorido
        self.switch_var = ctk.BooleanVar(value=False)
        self.switch = ctk.CTkSwitch(
            self.main_frame, text="Colorful QRCode", variable=self.switch_var, onvalue=True, offvalue=False,
            fg_color="#4C566A", text_color="#D8DEE9"
        )
        self.switch.grid(row=6, column=0, columnspan=2, pady=10)

        # Entrada de texto para nome do arquivo de saída
        self.output_name = ctk.CTkEntry(
            self.main_frame, placeholder_text="Output Name", fg_color="#4C566A", text_color="#D8DEE9"
        )
        self.output_name.grid(row=7, column=0, columnspan=2, pady=10)

        # Botão para gerar síntese
        self.generate_button = ctk.CTkButton(
            self.main_frame, text="Generate Synth", command=self.generate,
            fg_color="#88C0D0", text_color="#2E3440", width=200
        )
        self.generate_button.grid(row=8, column=0, columnspan=2, pady=20)

        # Ajusta o espaçamento das colunas
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)

    def run(self):
        self.mainloop()
            
    def select_image(self):
        file_path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Selecionar Imagem",
            filetypes=[("Image Files (*.jpg *.png *.jpeg)", "*.jpg *.png *.jpeg")]
        )
        if file_path:
            self.image_path = file_path
            self.image_label.configure(text=f"Imagem selecionada: {file_path}")

    def generate(self):
        if not self.image_path:
            self.show_error("Selecione uma imagem de entrada.")
            return

        if not self.data_string.get():
            self.show_error("Digite uma string de dados.")
            return

        if not self.output_name.get():
            self.show_error("Digite um nome de saída.")
            return

        selected_option = self.dropdown_var.get()[0].lower()
        halftone.run(self.image_path, self.data_string.get(), selected_option, self.output_name.get(), self.switch_var.get())
        
        
        


       
        