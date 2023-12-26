import re
from abc import abstractmethod, ABC

import customtkinter as CTk
from tkinter import messagebox
from windows.MainWindow import MainWindow

passwords = [
    "qtyAsO5E-",
    "ECvQSUH7K@",
    "mhZWi9C-",
    "mdPsx2Y-",
    "ZtGrWRc5X_",
    "2Vx11HX",
    "Axu7x",
    "aoRd",
    "Z_Gqob",
    "Lw"
]


class PasswordValidationStrategy(ABC):
    @abstractmethod
    def is_valid(self, password):
        pass

    @abstractmethod
    def error_message(self):
        pass


class LengthValidation(PasswordValidationStrategy):
    def is_valid(self, password):
        return len(password) >= 8

    def error_message(self):
        return "Must be at least 8 characters"


class CharacterValidation(PasswordValidationStrategy):
    def is_valid(self, password):
        return bool(re.search(r'[a-zA-Z]', password))

    def error_message(self):
        return "Must contain Latin letters"


class DigitValidation(PasswordValidationStrategy):
    def is_valid(self, password):
        return bool(re.search(r'\d', password))

    def error_message(self):
        return "Must contain numbers"


class SpecialCharacterValidation(PasswordValidationStrategy):
    def is_valid(self, password):
        return bool(re.search(r'[?!@*_\+\-%&]', password))

    def error_message(self):
        return "Must contain special characters"


class UppercaseValidation(PasswordValidationStrategy):
    def is_valid(self, password):
        return bool(re.search(r'[A-Z]', password))

    def error_message(self):
        return "Must contain capital letters"


class LowercaseValidation(PasswordValidationStrategy):
    def is_valid(self, password):
        return bool(re.search(r'[a-z]', password))

    def error_message(self):
        return "Must contain lowercase letters"


class PasswordValidator:
    def __init__(self, password, validation_strategies):
        self.password = password
        self.validation_strategies = validation_strategies
        self.errors = []

    def is_valid_password(self):
        self.errors = []
        for strategy in self.validation_strategies:
            if not strategy.is_valid(self.password):
                self.errors.append(strategy.error_message())

        return len(self.errors) == 0, self.errors


# Пример использования
validation_strategies = [
    LengthValidation(),
    CharacterValidation(),
    DigitValidation(),
    SpecialCharacterValidation(),
    UppercaseValidation(),
    LowercaseValidation(),
]


CTk.set_appearance_mode("Dark")
CTk.set_default_color_theme("dark-blue")


def on_validate(P):
    return len(P) <= 32 and " " not in P


def show_error_message(type, errors):
    if type == "empty_input":
        messagebox.showerror("Error", "You must enter your token!")
    elif type == "no_access":
        messagebox.showerror("Error", "You do not have access to this token!")
    elif type == "validate":
        message_error = ""
        for error in errors:
            message_error += "- " + error + "\n"

        messagebox.showerror("Error", f"The password is invalid. Errors:\n\n{message_error}")


class RegistrationWindow(CTk.CTk):
    width = 460
    height = 370

    def __init__(self):
        super().__init__()

        self.geometry(f"{self.width}x{self.height}")
        self.title("TitaniumSafe (Authentication)")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.validate_data = self.register(on_validate)

        # ==== Drawing the automation window ==== #
        self.login_frame = CTk.CTkFrame(self, corner_radius=10)
        self.login_frame.grid(row=0, column=0, sticky="ns", padx=90, pady=self.height / 4)
        self.login_label = CTk.CTkLabel(self.login_frame, text="TitaniumSafe",
                                        font=CTk.CTkFont(size=25, weight="bold"))
        self.login_label.grid(row=0, column=0, padx=30, pady=(15, 15))
        self.password_entry = CTk.CTkEntry(self.login_frame, width=220, show="*", placeholder_text="token",
                                           validate="key", validatecommand=(self.validate_data, "%P"), state="normal")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))

        self.login_button = CTk.CTkButton(self.login_frame, text="Login", command=self.login_button_event, width=220)
        self.login_button.grid(row=3, column=0, padx=30, pady=(0, 15))
        # ===================================== #

    def login_button_event(self):
        match self.password_entry.get():
            case "":
                show_error_message("empty_input", None)
            case _:
                try:
                    password_validator = PasswordValidator(self.password_entry.get(), validation_strategies)
                    is_valid, errors = password_validator.is_valid_password()
                    if is_valid:
                        if self.password_entry.get() in passwords:
                            main_window = MainWindow()
                            self.destroy()
                            main_window.run()
                        else:
                            show_error_message("no_access", None)
                    else:
                        show_error_message("validate", errors)

                except Exception as e:
                    print("[TitaniumSafe | ERROR]", e)
        return

    def on_closing(self):
        self.destroy()
