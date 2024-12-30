import customtkinter as ctk
from tkinter import filedialog
import os
import src.halftone as halftone

class Window (ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("HTQRCodeGen")
        self.geometry("700x500")

        # Widgets
        self.image_button = ctk.CTkButton(self, text="Select Image Input", command=self.select_image)
        self.image_button.pack(pady=(50, 5))
        self.image_path = None

        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(pady=10)

        self.data_string = ctk.CTkEntry(self, placeholder_text="Data String")
        self.data_string.pack(pady=10)

        self.output_name = ctk.CTkEntry(self, placeholder_text="Output Name")
        self.output_name.pack(pady=10)

        self.generate_button = ctk.CTkButton(self, text="Generate Synth", command=self.generate)
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
      
        halftone.run(self.image_path, self.data_string.get())
        
        
        


       
        