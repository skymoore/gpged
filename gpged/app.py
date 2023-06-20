from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QComboBox,
    QApplication
)
import gnupg

class GPGED(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.gpg = gnupg.GPG()
        self.key_select = QComboBox()
        self.populate_keys()

        self.clipboard = QApplication.clipboard()
        self.input_entry = QTextEdit()
        self.output_entry = QTextEdit()
        self.encrypt_button = QPushButton("Encrypt", self)
        self.decrypt_button = QPushButton("Decrypt", self)
        self.refresh_button = QPushButton("Load Keys", self)
        self.paste_input_button = QPushButton("Paste", self)
        self.paste_public_key_button = QPushButton("Paste", self)
        self.copy_output_button = QPushButton("Copy", self)
        self.clear_input_button = QPushButton("Clear", self)
        self.clear_public_key_button = QPushButton("Clear", self)
        self.clear_output_button = QPushButton("Clear", self)
        self.public_key_input_label = QLabel("Public Key:")
        self.public_key_input = QTextEdit()

        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.refresh_button.clicked.connect(self.refresh)
        self.paste_input_button.clicked.connect(self.paste_input)
        self.paste_public_key_button.clicked.connect(self.paste_public_key)
        self.copy_output_button.clicked.connect(self.copy_output)
        self.clear_input_button.clicked.connect(self.clear_input)
        self.clear_public_key_button.clicked.connect(self.clear_public_key)
        self.clear_output_button.clicked.connect(self.clear_output)
        self.key_select.currentTextChanged.connect(self.handle_dropdown)

        vbox = QVBoxLayout()
        hbox_key_select = QHBoxLayout()
        hbox_key_select.addWidget(QLabel("Select Key:"))
        hbox_key_select.addWidget(self.key_select)
        hbox_key_select.addWidget(self.refresh_button)
        vbox.addLayout(hbox_key_select)
        vbox.addWidget(self.public_key_input_label)
        vbox.addWidget(self.public_key_input)
        hbox_public_key = QHBoxLayout()
        hbox_public_key.addWidget(self.paste_public_key_button)
        hbox_public_key.addWidget(self.clear_public_key_button)
        vbox.addLayout(hbox_public_key)
        vbox.addWidget(QLabel("Message/Ciphertext:"))
        vbox.addWidget(self.input_entry)
        hbox_input = QHBoxLayout()
        hbox_input.addWidget(self.paste_input_button)
        hbox_input.addWidget(self.clear_input_button)
        vbox.addLayout(hbox_input)
        hbox_enc_dec = QHBoxLayout()
        hbox_enc_dec.addWidget(self.encrypt_button)
        hbox_enc_dec.addWidget(self.decrypt_button)
        vbox.addLayout(hbox_enc_dec)
        vbox.addWidget(QLabel("Output:"))
        vbox.addWidget(self.output_entry)
        hbox_output = QHBoxLayout()
        hbox_output.addWidget(self.copy_output_button)
        hbox_output.addWidget(self.clear_output_button)
        vbox.addLayout(hbox_output)

        self.setLayout(vbox)
        self.setWindowTitle("PGP Encrypt/Decrypt")
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def handle_dropdown(self, text):
        if text == "Public Key Input":
            self.public_key_input_label.show()
            self.public_key_input.show()
            self.paste_public_key_button.show()
            self.clear_public_key_button.show()
        else:
            self.public_key_input_label.hide()
            self.public_key_input.hide()
            self.paste_public_key_button.hide()
            self.clear_public_key_button.hide()

    def populate_keys(self):
        current_selection = self.key_select.currentText()
        self.key_select.clear()
        self.key_select.addItem("Public Key Input")
        public_keys = self.gpg.list_keys()

        for key in public_keys:
            if len(key["uids"]) > 0:
                self.key_select.addItem(key["uids"][0])
            else:
                self.key_select.addItem(key["fingerprint"][-6:])
        try:
            self.key_select.setCurrentText(current_selection)
        except Exception:
            self.key_select.setCurrentIndex(0)

    def encrypt(self):
        selected_key = self.key_select.currentText()
        plaintext = self.input_entry.toPlainText().strip()
        if selected_key == "Public Key Input":
            public_key = self.public_key_input.toPlainText().strip()
            import_result = self.gpg.import_keys(public_key)
            if import_result.count != 1:
                self.output_entry.setText("Failed to import public key")
                return
            selected_key = import_result.fingerprints[0]

        encrypted_data = self.gpg.encrypt(plaintext, selected_key)
        if not encrypted_data.ok:
            self.output_entry.setText("Failed to encrypt message")
            return

        self.output_entry.setText(str(encrypted_data))

    def decrypt(self):
        ciphertext = self.input_entry.toPlainText().strip()

        decrypted_data = self.gpg.decrypt(ciphertext)
        if not decrypted_data.ok:
            self.output_entry.setText("Failed to decrypt message")
            return

        self.output_entry.setText(str(decrypted_data))

    def refresh(self):
        self.populate_keys()

    def paste_input(self):
        self.input_entry.setText(self.clipboard.text())

    def paste_public_key(self):
        self.public_key_input.setText(self.clipboard.text())

    def copy_output(self):
        self.clipboard.setText(self.output_entry.toPlainText())

    def clear_input(self):
        self.input_entry.clear()

    def clear_public_key(self):
        self.public_key_input.clear()

    def clear_output(self):
        self.output_entry.clear()
