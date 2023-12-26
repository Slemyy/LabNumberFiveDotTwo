from windows.RegistrationWindow import RegistrationWindow


def main():
    print("[TitaniumSafe] Application launched successfully")
    auth = RegistrationWindow()
    auth.mainloop()


if __name__ == "__main__":
    main()
