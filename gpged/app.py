from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QComboBox,
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

        self.input_entry = QTextEdit()
        self.output_entry = QTextEdit()
        self.encrypt_button = QPushButton("Encrypt", self)
        self.decrypt_button = QPushButton("Decrypt", self)
        self.refresh_button = QPushButton("Refresh", self)
        self.public_key_input_label = QLabel("Public Key:")
        self.public_key_input = QTextEdit()

        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.refresh_button.clicked.connect(self.refresh)
        self.key_select.currentTextChanged.connect(self.handle_dropdown)

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Select Key:"))
        hbox.addWidget(self.key_select)
        hbox.addWidget(self.refresh_button)
        vbox.addLayout(hbox)
        vbox.addWidget(self.public_key_input_label)
        vbox.addWidget(self.public_key_input)
        vbox.addWidget(QLabel("Message/Ciphertext:"))
        vbox.addWidget(self.input_entry)
        vbox.addWidget(self.encrypt_button)
        vbox.addWidget(self.decrypt_button)
        vbox.addWidget(QLabel("Output:"))
        vbox.addWidget(self.output_entry)

        self.setLayout(vbox)
        self.setWindowTitle("PGP Encrypt/Decrypt")
        self.setGeometry(300, 300, 300, 200)
        # self.public_key_input.hide()  # Hide initially
        self.show()

    def handle_dropdown(self, text):
        if text == "Public Key Input":
            self.public_key_input_label.show()
            self.public_key_input.show()
        else:
            self.public_key_input_label.hide()
            self.public_key_input.hide()

    def populate_keys(self):
        self.key_select.clear()
        self.key_select.addItem("Public Key Input")  # Add public key input option
        public_keys = self.gpg.list_keys()
        for key in public_keys:
            if len(key["uids"]) > 0:
                self.key_select.addItem(key["uids"][0])
            else:
                self.key_select.addItem(key["fingerprint"][-6:])

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
