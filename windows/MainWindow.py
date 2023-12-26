import io
import re
from tkinter import filedialog, messagebox

import customtkinter as CTk

from ciphers.caesar import Caesar
from ciphers.rsa import RSA
from ciphers.vigenere import Vigenere


def change_appearance_mode_event(new_appearance_mode):
    CTk.set_appearance_mode(new_appearance_mode)


def on_validate(P):
    return P.isdigit() and 10024 >= int(P) > 0 or P == ""


def on_validate_vis(P):
    return " " not in P


def save_to_file(text):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

    if file_path:
        with io.open(file_path, 'w', encoding='utf8', errors="replace") as file:
            file.write(text)


def open_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with io.open(file_path, 'r', encoding='utf8', errors="replace") as file:
            content = file.read()
            return content


class MainWindow(CTk.CTk):
    width = 960
    height = 500

    def __init__(self):
        super().__init__()

        self.rsa_frame = None
        self.vigenere_frame = None
        self.caesar_frame = None
        self.frame_left = None

        self.geometry(f"{self.width}x{self.height}")
        self.title("TitaniumSafe")
        self.iconbitmap("D:\\" + "NSTU\\" + "3 семестр\\" + "Программирование\\" +
                        "Курсовая\\" + "TitaniumSafe\\" + "images\\" + "icon.ico")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.validate_data = self.register(on_validate)
        self.vis_validate_data = self.register(on_validate_vis)

        # ==== Create Frames ==== #
        self.create_frames()
        # ======================= #

        # ==== Navigation Frame ==== #
        self.navigation_frame_label = CTk.CTkLabel(self.frame_left, text="TitaniumSafe\n———", compound="left",
                                                   font=CTk.CTkFont(size=20, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.caesar_button = CTk.CTkButton(self.frame_left, corner_radius=0, height=40,
                                           border_spacing=10, text="Caesar", fg_color="transparent",
                                           text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                           anchor="w", command=self.caesar_button_event)
        self.caesar_button.grid(row=1, column=0, padx=2, sticky="ew")

        self.vigenere_button = CTk.CTkButton(self.frame_left, corner_radius=0,
                                             height=40, border_spacing=10, text="Vigenere",
                                             fg_color="transparent", text_color=("gray10", "gray90"),
                                             hover_color=("gray70", "gray30"),
                                             anchor="w", command=self.vigenere_button_event)
        self.vigenere_button.grid(row=2, column=0, padx=2, sticky="ew")

        self.rsa_button = CTk.CTkButton(self.frame_left, corner_radius=0, height=40,
                                        border_spacing=10, text="RSA", fg_color="transparent",
                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                        anchor="w", command=self.rsa_button_event)
        self.rsa_button.grid(row=3, column=0, padx=2, sticky="ew")

        # Сюда дописывать новые шифры

        self.appearance_mode_menu = CTk.CTkOptionMenu(self.frame_left,
                                                      values=["Dark", "Light"],
                                                      command=change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # ==================================== #

        # ==== Caesar frame ==== #
        self.title_caesar_label = CTk.CTkLabel(self.caesar_frame, text="Caesar\n———",
                                               font=CTk.CTkFont(size=20, weight="bold"))
        self.title_caesar_label.place(relx=0.5, rely=0.05, anchor=CTk.N)

        self.caesar_entry_field = CTk.CTkLabel(self.caesar_frame, text="Entry field",
                                               font=CTk.CTkFont(size=15, weight="bold"))
        self.caesar_entry_field.place(relx=0.17, rely=0.17)

        self.caesar_textbox_one = CTk.CTkTextbox(master=self.caesar_frame, width=265, height=150,
                                                 state="normal", corner_radius=10,
                                                 font=CTk.CTkFont(size=13))
        self.caesar_textbox_one.place(relx=0.05, rely=0.24)

        self.arrow_label = CTk.CTkLabel(self.caesar_frame, text="->", font=CTk.CTkFont(size=20, weight="bold"))
        self.arrow_label.place(relx=0.5, rely=0.36, anchor=CTk.N)

        self.caesar_result_text = CTk.CTkLabel(self.caesar_frame, text="Result",
                                               font=CTk.CTkFont(size=15, weight="bold"))
        self.caesar_result_text.place(relx=0.73, rely=0.17)

        self.caesar_textbox_two = CTk.CTkTextbox(master=self.caesar_frame, width=265, height=150,
                                                 corner_radius=10, state="disable",
                                                 font=CTk.CTkFont(size=13))
        self.caesar_textbox_two.place(relx=0.58, rely=0.24)

        self.caesar_var = CTk.StringVar(self)
        self.caesar_var.set("Encrypt")
        self.mode_selection_menu = CTk.CTkOptionMenu(self.caesar_frame, variable=self.caesar_var,
                                                     dynamic_resizing=False,
                                                     values=["Encrypt", "Decrypt"])
        self.mode_selection_menu.place(relx=0.5, rely=0.82, anchor=CTk.CENTER)

        self.caesar_answer_button = CTk.CTkButton(self.caesar_frame, text="Answer", command=self.caesar_command)
        self.caesar_answer_button.place(relx=0.5, rely=0.9, anchor=CTk.CENTER)

        self.caesar_result_text = CTk.CTkLabel(self.caesar_frame, text="Enter shift value",
                                               font=CTk.CTkFont(size=13, weight="bold"))
        self.caesar_result_text.place(relx=0.5, rely=0.69, anchor=CTk.CENTER)

        self.caesar_shift_entry = CTk.CTkEntry(self.caesar_frame, state="normal",
                                               validate="key", validatecommand=(self.validate_data, "%P"))
        self.caesar_shift_entry.place(relx=0.5, rely=0.74, anchor=CTk.CENTER)

        self.caesar_open_file = CTk.CTkButton(self.caesar_frame, text="Load From File", command=self.caesar_open)
        self.caesar_open_file.place(relx=0.23, rely=0.62, anchor=CTk.CENTER)

        self.caesar_save_file = CTk.CTkButton(self.caesar_frame, text="Save To File", command=self.caesar_save)
        self.caesar_save_file.place(relx=0.73, rely=0.62, anchor=CTk.CENTER)

        self.caesar_copy_text = CTk.CTkButton(self.caesar_frame, text="Copy", command=self.caesar_copy, width=50)
        self.caesar_copy_text.place(relx=0.87, rely=0.62, anchor=CTk.CENTER)

        # ====================== #

        # ==== Vigenere frame ==== #
        self.title_frame_label = CTk.CTkLabel(self.vigenere_frame, text="Vigenere\n———",
                                              font=CTk.CTkFont(size=20, weight="bold"))
        self.title_frame_label.place(relx=0.5, rely=0.05, anchor=CTk.N)

        self.vigenere_entry_field = CTk.CTkLabel(self.vigenere_frame, text="Entry field",
                                                 font=CTk.CTkFont(size=15, weight="bold"))
        self.vigenere_entry_field.place(relx=0.17, rely=0.17)

        self.vigenere_textbox_one = CTk.CTkTextbox(self.vigenere_frame, width=265, height=150,
                                                   state="normal", corner_radius=10,
                                                   font=CTk.CTkFont(size=13))
        self.vigenere_textbox_one.place(relx=0.05, rely=0.24)

        self.vigenere_arrow_label = CTk.CTkLabel(self.vigenere_frame, text="->",
                                                 font=CTk.CTkFont(size=20, weight="bold"))
        self.vigenere_arrow_label.place(relx=0.5, rely=0.36, anchor=CTk.N)

        self.vigenere_result_text = CTk.CTkLabel(self.vigenere_frame, text="Result",
                                                 font=CTk.CTkFont(size=15, weight="bold"))
        self.vigenere_result_text.place(relx=0.73, rely=0.17)

        self.vigenere_textbox_two = CTk.CTkTextbox(master=self.vigenere_frame, width=265, height=150,
                                                   corner_radius=10, state="disable",
                                                   font=CTk.CTkFont(size=13))
        self.vigenere_textbox_two.place(relx=0.58, rely=0.24)

        self.vigenere_var = CTk.StringVar(self)
        self.vigenere_var.set("Encrypt")
        self.vigenere_selection_menu = CTk.CTkOptionMenu(self.vigenere_frame, variable=self.vigenere_var,
                                                         dynamic_resizing=False,
                                                         values=["Encrypt", "Decrypt"])
        self.vigenere_selection_menu.place(relx=0.5, rely=0.82, anchor=CTk.CENTER)

        self.vigenere_answer_button = CTk.CTkButton(self.vigenere_frame, text="Answer", command=self.vigenere_command)
        self.vigenere_answer_button.place(relx=0.5, rely=0.9, anchor=CTk.CENTER)

        self.vigenere_result_text = CTk.CTkLabel(self.vigenere_frame, text="Enter the encryption key",
                                                 font=CTk.CTkFont(size=13, weight="bold"))
        self.vigenere_result_text.place(relx=0.5, rely=0.69, anchor=CTk.CENTER)

        self.vigenere_key_entry = CTk.CTkEntry(self.vigenere_frame, state="normal",
                                               validate="key", validatecommand=(self.vis_validate_data, "%P"))
        self.vigenere_key_entry.place(relx=0.5, rely=0.74, anchor=CTk.CENTER)

        self.vigenere_open_file = CTk.CTkButton(self.vigenere_frame, text="Load From File",
                                                command=self.vigenere_open)
        self.vigenere_open_file.place(relx=0.23, rely=0.62, anchor=CTk.CENTER)

        self.vigenere_save_file = CTk.CTkButton(self.vigenere_frame, text="Save To File",
                                                command=self.vigenere_save)
        self.vigenere_save_file.place(relx=0.73, rely=0.62, anchor=CTk.CENTER)

        self.vigenere_copy_text = CTk.CTkButton(self.vigenere_frame, text="Copy", command=self.vigenere_copy, width=50)
        self.vigenere_copy_text.place(relx=0.87, rely=0.62, anchor=CTk.CENTER)

        # ======================== #

        # ==== RSA frame ==== #
        self.rsa_frame_label = CTk.CTkLabel(self.rsa_frame, text="RSA\n———",
                                            compound="center",
                                            font=CTk.CTkFont(size=20, weight="bold"))
        self.rsa_frame_label.place(relx=0.5, rely=0.05, anchor=CTk.N)

        self.rsa_entry_field = CTk.CTkLabel(self.rsa_frame, text="Entry field",
                                            font=CTk.CTkFont(size=15, weight="bold"))
        self.rsa_entry_field.place(relx=0.17, rely=0.17)

        self.rsa_textbox_one = CTk.CTkTextbox(self.rsa_frame, width=265, height=150,
                                              state="normal", corner_radius=10,
                                              font=CTk.CTkFont(size=13))
        self.rsa_textbox_one.place(relx=0.05, rely=0.24)

        self.rsa_arrow_label = CTk.CTkLabel(self.rsa_frame, text="->",
                                            font=CTk.CTkFont(size=20, weight="bold"))
        self.rsa_arrow_label.place(relx=0.5, rely=0.36, anchor=CTk.N)

        self.rsa_result_text = CTk.CTkLabel(self.rsa_frame, text="Result",
                                            font=CTk.CTkFont(size=15, weight="bold"))
        self.rsa_result_text.place(relx=0.73, rely=0.17)

        self.rsa_textbox_two = CTk.CTkTextbox(master=self.rsa_frame, width=265, height=150,
                                              corner_radius=10, state="disable",
                                              font=CTk.CTkFont(size=13))
        self.rsa_textbox_two.place(relx=0.58, rely=0.24)

        self.rsa_var = CTk.StringVar(self)
        self.rsa_var.set("Encrypt")
        self.rsa_selection_menu = CTk.CTkOptionMenu(self.rsa_frame, variable=self.rsa_var,
                                                    dynamic_resizing=False,
                                                    values=["Encrypt", "Decrypt"])
        self.rsa_selection_menu.place(relx=0.5, rely=0.82, anchor=CTk.CENTER)

        self.rsa_answer_button = CTk.CTkButton(self.rsa_frame, text="Answer", command=self.rsa_command)
        self.rsa_answer_button.place(relx=0.5, rely=0.9, anchor=CTk.CENTER)

        self.rsa_result_text = CTk.CTkLabel(self.rsa_frame, text="Enter the private key",
                                            font=CTk.CTkFont(size=13, weight="bold"))
        self.rsa_result_text.place(relx=0.5, rely=0.69, anchor=CTk.CENTER)

        self.rsa_key_entry = CTk.CTkEntry(self.rsa_frame, state="normal")
        self.rsa_key_entry.place(relx=0.5, rely=0.74, anchor=CTk.CENTER)

        self.rsa_open_file = CTk.CTkButton(self.rsa_frame, text="Load From File",
                                           command=self.rsa_open)
        self.rsa_open_file.place(relx=0.23, rely=0.62, anchor=CTk.CENTER)

        self.rsa_save_file = CTk.CTkButton(self.rsa_frame, text="Save To File",
                                           command=self.rsa_save)
        self.rsa_save_file.place(relx=0.73, rely=0.62, anchor=CTk.CENTER)

        self.rsa_copy_button = CTk.CTkButton(self.rsa_frame, text="Copy", command=self.rsa_copy, width=50)
        self.rsa_copy_button.place(relx=0.87, rely=0.62, anchor=CTk.CENTER)

        self.rsa_public_key_text = CTk.CTkLabel(self.rsa_frame, text="Public Key",
                                                font=CTk.CTkFont(size=13, weight="bold"))
        self.rsa_public_key_text.place(relx=0.24, rely=0.77, anchor=CTk.CENTER)
        self.rsa_public_key_entry = CTk.CTkEntry(self.rsa_frame, placeholder_text="A key will appear here",
                                                 state="disable", width=160)
        self.rsa_public_key_entry.place(relx=0.24, rely=0.82, anchor=CTk.CENTER)
        self.rsa_public_info_text = CTk.CTkLabel(self.rsa_frame, text="(*) No need to enter here",
                                                 font=CTk.CTkFont(size=13, weight="bold"))
        self.rsa_public_info_text.place(relx=0.24, rely=0.88, anchor=CTk.CENTER)

        self.rsa_private_key_text = CTk.CTkLabel(self.rsa_frame, text="Private Key",
                                                 font=CTk.CTkFont(size=13, weight="bold"))
        self.rsa_private_key_text.place(relx=0.76, rely=0.77, anchor=CTk.CENTER)
        self.rsa_private_key_entry = CTk.CTkEntry(self.rsa_frame, placeholder_text="A key will appear here",
                                                  state="disable", width=160)
        self.rsa_private_key_entry.place(relx=0.76, rely=0.82, anchor=CTk.CENTER)
        self.rsa_private_info_text = CTk.CTkLabel(self.rsa_frame, text="(*) No need to enter here",
                                                  font=CTk.CTkFont(size=13, weight="bold"))
        self.rsa_private_info_text.place(relx=0.76, rely=0.88, anchor=CTk.CENTER)
        self.rsa_copy_key_button = CTk.CTkButton(self.rsa_frame, text="Copy", command=self.rsa_copy_key, width=50)
        self.rsa_copy_key_button.place(relx=0.912, rely=0.82, anchor=CTk.CENTER)

        self.rsa_private_key_entry.configure(state="normal")
        self.rsa_private_key_entry.insert(0, "123, 123")
        self.rsa_private_key_entry.configure(state="disable")
        self.rsa_public_key_entry.configure(state="normal")
        self.rsa_public_key_entry.insert(0, "123, 123")
        self.rsa_public_key_entry.configure(state="disable")

        # =================== #

        self.select_frame("caesar")  # select default frame

    def create_frames(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.frame_left = CTk.CTkFrame(master=self, corner_radius=10, border_width=2)
        self.frame_left.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)
        self.frame_left.grid_rowconfigure(5, weight=1)

        self.caesar_frame = CTk.CTkFrame(master=self, corner_radius=10, border_width=2)
        self.caesar_frame.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        self.caesar_frame.grid_rowconfigure(3, weight=1)
        self.caesar_frame.grid_columnconfigure(2, weight=1)

        self.vigenere_frame = CTk.CTkFrame(master=self, corner_radius=10, border_width=2)
        self.vigenere_frame.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)

        self.rsa_frame = CTk.CTkFrame(master=self, corner_radius=10, border_width=2)
        self.rsa_frame.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)

    def select_frame(self, name):
        self.caesar_button.configure(fg_color=("gray75", "gray25") if name == "caesar" else "transparent")
        self.vigenere_button.configure(fg_color=("gray75", "gray25") if name == "vigenere" else "transparent")
        self.rsa_button.configure(fg_color=("gray75", "gray25") if name == "rsa" else "transparent")

        # show selected frame
        if name == "caesar":
            self.caesar_frame.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        else:
            self.caesar_frame.grid_forget()
        if name == "vigenere":
            self.vigenere_frame.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        else:
            self.vigenere_frame.grid_forget()
        if name == "rsa":
            self.rsa_frame.grid(row=0, column=1, sticky="nswe", padx=15, pady=15)
        else:
            self.rsa_frame.grid_forget()

    def caesar_button_event(self):
        self.select_frame("caesar")

    def vigenere_button_event(self):
        self.select_frame("vigenere")

    def rsa_button_event(self):
        self.select_frame("rsa")

    # CAESAR
    def caesar_command(self):
        self.caesar_textbox_two.configure(state="normal")
        self.caesar_textbox_two.delete("0.0", "end")
        shift = self.caesar_shift_entry.get()

        if shift == '':
            shift = "1"

        if self.caesar_var.get() == "Encrypt":
            text = self.caesar_textbox_one.get("1.0", "end-1c")
            result = Caesar.encrypt(text, int(shift))

            self.caesar_textbox_two.insert("0.0", result)
            self.caesar_textbox_two.configure(state="disable")
        else:
            text = self.caesar_textbox_one.get("1.0", "end-1c")
            result = Caesar.decrypt(text, int(shift))

            self.caesar_textbox_two.insert("0.0", result)
            self.caesar_textbox_two.configure(state="disable")

    def caesar_copy(self):
        content = self.caesar_textbox_two.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()

    def caesar_save(self):
        text = self.caesar_textbox_two.get('1.0', 'end-1c')
        save_to_file(text)

    def caesar_open(self):
        self.caesar_textbox_one.delete("0.0", "end")
        self.caesar_textbox_one.insert("0.0", self.check_content())

    # VIGENERE
    def vigenere_command(self):
        self.vigenere_textbox_two.configure(state="normal")
        self.vigenere_textbox_two.delete("0.0", "end")
        key = self.vigenere_key_entry.get()

        if key == '':
            key = "standard"

        if self.vigenere_var.get() == "Encrypt":
            text = self.vigenere_textbox_one.get("1.0", "end-1c")
            result = Vigenere.encrypt(text, key)

            self.vigenere_textbox_two.insert("0.0", result)
            self.vigenere_textbox_two.configure(state="disable")
        else:
            text = self.vigenere_textbox_one.get("1.0", "end-1c")
            result = Vigenere.decrypt(text, key)

            self.vigenere_textbox_two.insert("0.0", result)
            self.vigenere_textbox_two.configure(state="disable")

    def vigenere_copy(self):
        content = self.vigenere_textbox_two.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()

    def vigenere_save(self):
        text = self.vigenere_textbox_two.get('1.0', 'end-1c')
        save_to_file(text)

    def vigenere_open(self):
        self.vigenere_textbox_one.delete("0.0", "end")
        self.vigenere_textbox_one.insert("0.0", self.check_content())

    def check_content(self):
        content = open_from_file()

        if not (content is None) and len(content) >= 5000:
            result = messagebox.askquestion("Warning", "This file is too large, it may cause lags, "
                                                       "do you want to continue?",
                                            parent=self)

            if not (result == 'yes'):
                return ''
        else:
            return content

        return content

    # RSA
    def rsa_command(self):
        self.rsa_textbox_two.configure(state="normal")
        self.rsa_textbox_two.delete("0.0", "end")

        key = tuple(map(int, re.findall(r'\d+', self.rsa_key_entry.get())))
        text = self.rsa_textbox_one.get("1.0", "end-1c")

        if self.rsa_var.get() == "Encrypt":
            public, private = RSA().key_gen()
            message = RSA.encrypt(text, public)

            encrypted_message = ""
            for i in message:
                encrypted_message += " " + str(i)

            self.rsa_textbox_two.insert("0.0", encrypted_message[1:])
            self.rsa_textbox_two.configure(state="disable")
            self.rsa_private_key_entry.configure(state="normal")
            self.rsa_private_key_entry.delete(0, CTk.END)
            self.rsa_private_key_entry.insert(0, private)
            self.rsa_private_key_entry.configure(state="disable")
            self.rsa_public_key_entry.configure(state="normal")
            self.rsa_public_key_entry.delete(0, CTk.END)
            self.rsa_public_key_entry.insert(0, public)
            self.rsa_public_key_entry.configure(state="disable")
        else:
            try:
                text = [int(num) for num in text.split(' ')]
                result = RSA.decrypt(text, key)
                self.rsa_textbox_two.insert("0.0", result)
                self.rsa_textbox_two.configure(state="disable")
            except Exception as e:
                print("[TitaniumSafe | ERROR]", e)
                messagebox.showerror("Error", "You entered incorrect text or key. Please check and try again.")

    def rsa_copy(self):
        content = self.rsa_textbox_two.get("1.0", "end-1c")
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()

    def rsa_copy_key(self):
        content = self.rsa_private_key_entry.get()
        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()

    def rsa_save(self):
        text = self.rsa_textbox_two.get('1.0', 'end-1c')
        save_to_file(text)

    def rsa_open(self):
        self.rsa_textbox_one.delete("0.0", "end")
        self.rsa_textbox_one.insert("0.0", self.check_content())

    def on_closing(self):
        self.destroy()

    def run(self):
        self.mainloop()