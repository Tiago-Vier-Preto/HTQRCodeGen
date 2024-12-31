import customtkinter as ctk
from tkinter import filedialog
import os
import src.halftone as halftone

class Window (ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HTQRCodeGen")
        self.geometry("700x500")
        self.configure(bg="#2E3440")  # Background color

        # Widgets
        self.image_button = ctk.CTkButton(self, text="Select Image Input", command=self.select_image, fg_color="#88C0D0", text_color="#2E3440")
        self.image_button.pack(pady=(40, 0))
        self.image_path = None

        self.image_label = ctk.CTkLabel(self, text="", text_color="#D8DEE9")
        self.image_label.pack(pady=10)

        self.data_string = ctk.CTkEntry(self, placeholder_text="Data String", fg_color="#4C566A", text_color="#D8DEE9")
        self.data_string.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="Redundancy (error correction level):", text_color="#D8DEE9")
        self.error_label.pack(pady=5)
        self.dropdown_var = ctk.StringVar(value="High (30%)")
        self.dropdown_menu = ctk.CTkOptionMenu(self, variable=self.dropdown_var, values=["Low (7%)", "Medium (15%)", "Quartile (25%)", "High (30%)"], fg_color="#4C566A", text_color="#D8DEE9")
        self.dropdown_menu.pack(pady=10)

        self.switch_var = ctk.BooleanVar(value=False)
        self.switch = ctk.CTkSwitch(self, text="Colorful QRCode", variable=self.switch_var, onvalue=True, offvalue=False, fg_color="#4C566A", text_color="#D8DEE9")
        self.switch.pack(pady=10)

        self.output_name = ctk.CTkEntry(self, placeholder_text="Output Name", fg_color="#4C566A", text_color="#D8DEE9")
        self.output_name.pack(pady=10)

        self.generate_button = ctk.CTkButton(self, text="Generate Synth", command=self.generate, fg_color="#88C0D0", text_color="#2E3440")
        self.generate_button.pack(pady=10)

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
        
        
        


       
        