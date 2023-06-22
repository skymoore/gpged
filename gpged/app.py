from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QApplication,
    QListWidget,
    QLineEdit,
)
from fuzzywuzzy import fuzz
import gnupg


class GPGED(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.gpg = gnupg.GPG()
        self.clipboard = QApplication.clipboard()

        self.key_list_widget = QListWidget()
        self.key_list_widget.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.keys = {}
        self.populate_keys_list()
        self.key_search = QLineEdit()

        self.input_entry = QTextEdit()
        self.output_entry = QTextEdit()
        self.encrypt_button = QPushButton("Encrypt", self)
        self.decrypt_button = QPushButton("Decrypt", self)
        self.refresh_button = QPushButton("Load Keys", self)
        self.paste_input_button = QPushButton("Paste", self)
        self.copy_output_button = QPushButton("Copy", self)
        self.clear_input_button = QPushButton("Clear", self)
        self.clear_output_button = QPushButton("Clear", self)
        self.clear_key_list_selection_button = QPushButton("Clear Selection", self)

        self.key_search.textChanged.connect(self.filter_items)
        self.clear_key_list_selection_button.clicked.connect(self.clear_selection)
        self.encrypt_button.clicked.connect(self.encrypt)
        self.decrypt_button.clicked.connect(self.decrypt)
        self.refresh_button.clicked.connect(self.refresh)
        self.paste_input_button.clicked.connect(self.paste_input)
        self.copy_output_button.clicked.connect(self.copy_output)
        self.clear_input_button.clicked.connect(self.clear_input)
        self.clear_output_button.clicked.connect(self.clear_output)

        vbox = QVBoxLayout()
        hbox_key_select = QHBoxLayout()
        hbox_key_select.addWidget(QLabel("Filter Keys:"))
        hbox_key_select.addWidget(self.key_search)
        hbox_key_select.addWidget(self.refresh_button)
        vbox_key_search = QVBoxLayout()
        vbox_key_search.addWidget(QLabel("Select Keys:"))
        vbox_key_search.addWidget(self.key_list_widget)
        vbox_key_search.addWidget(self.clear_key_list_selection_button)
        vbox.addLayout(hbox_key_select)
        vbox.addLayout(vbox_key_search)
        hbox_public_key = QHBoxLayout()
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
        self.setGeometry(300, 300, 700, 800)
        self.show()

    def populate_keys_list(self):
        public_keys = self.gpg.list_keys()

        keys_list = []
        self.keys.clear()

        for key in public_keys:
            if len(key["uids"]) > 0:
                keys_list.append(f"{key['uids'][0]} - {key['fingerprint'][-6:]}")
                self.keys[f"{key['uids'][0]} - {key['fingerprint'][-6:]}"] = key[
                    "fingerprint"
                ]
            else:
                keys_list.append(key["fingerprint"][-6:])
                self.keys[key["fingerprint"][-6:]] = key["fingerprint"]

        self.key_list_widget.clear()
        self.key_list_widget.addItems(sorted(keys_list, key=lambda x: x.lower()))

    def filter_items(self, text):
        count = self.key_list_widget.count()

        for i in range(count):
            item = self.key_list_widget.item(i)

            text_lower = text.lower()
            item_text_lower = item.text().lower()

            if (
                text_lower in item_text_lower
                or fuzz.ratio(text_lower, item_text_lower) > 50
            ):
                item.setHidden(False)
            else:
                item.setHidden(True)

    def encrypt(self):
        selected_keys = [
            self.keys[key]
            for key in [item.text() for item in self.key_list_widget.selectedItems()]
        ]
        plaintext = self.input_entry.toPlainText().strip()

        encrypted_data = self.gpg.encrypt(plaintext, selected_keys, always_trust=True)
        if not encrypted_data.ok:
            self.output_entry.setText(
                f"Failed to encrypt message:\n{encrypted_data.stderr}"
            )
            return

        self.output_entry.setText(str(encrypted_data))

    def decrypt(self):
        ciphertext = self.input_entry.toPlainText().strip()

        decrypted_data = self.gpg.decrypt(ciphertext)
        if not decrypted_data.ok:
            self.output_entry.setText(
                f"Failed to decrypt message:\n{decrypted_data.stderr}"
            )
            return

        self.output_entry.setText(str(decrypted_data))

    def refresh(self):
        self.populate_keys_list()

    def clear_selection(self):
        self.key_list_widget.clearSelection()

    def paste_input(self):
        self.input_entry.setText(self.clipboard.text())

    def copy_output(self):
        self.clipboard.setText(self.output_entry.toPlainText())

    def clear_input(self):
        self.input_entry.clear()

    def clear_output(self):
        self.output_entry.clear()
