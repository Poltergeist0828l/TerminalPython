from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QLineEdit
from PyQt5.QtCore import Qt


class TecladoScreen(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.target_input = None

        try:
            with open("css/teclado.css", "r", encoding="utf-8") as file:
                self.setStyleSheet(file.read())
        except:
            self.setStyleSheet("background-color: #03111f;")

        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(50, 40, 50, 40)

        container = QFrame()
        container.setObjectName("inputContainer")
        layout_inputs = QVBoxLayout(container)

        self.title = QLabel("AUTENTICAÇÃO🔏")
        self.title.setObjectName("title")
        self.title.setAlignment(Qt.AlignCenter)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("NOME COMPLETO")
        self.input_nome.mousePressEvent = lambda e: self.set_target(self.input_nome)

        self.input_cpf = QLineEdit()
        self.input_cpf.setPlaceholderText("CPF")
        self.input_cpf.setAlignment(Qt.AlignCenter)
        self.input_cpf.mousePressEvent = lambda e: self.set_target(self.input_cpf)

        layout_inputs.addWidget(self.title)
        layout_inputs.addWidget(self.input_nome)
        layout_inputs.addWidget(self.input_cpf)

        container_keys = QFrame()
        layout_keys = QVBoxLayout(container_keys)

        linhas = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', '⌫'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', 'ESPAÇO', 'LIMPAR']
        ]

        for linha in linhas:
            h_layout = QHBoxLayout()
            for tecla in linha:
                btn = QPushButton(tecla)
                btn.setProperty("class", "keyBtn")

                if tecla in ['ESPAÇO', 'LIMPAR', '⌫']:
                    btn.setObjectName("specialKey")

                btn.clicked.connect(lambda ch, t=tecla: self.processar_tecla(t))
                h_layout.addWidget(btn)
            layout_keys.addLayout(h_layout)

        layout_acoes = QHBoxLayout()

        btn_cancel = QPushButton("CANCELAR")
        btn_cancel.setObjectName("cancelBtn")
        btn_cancel.clicked.connect(lambda: self.parent.setCurrentWidget(self.parent.login))

        btn_confirm = QPushButton("CONFIRMAR")
        btn_confirm.setObjectName("confirmBtn")
        btn_confirm.clicked.connect(self.finalizar)

        layout_acoes.addWidget(btn_cancel, 1)
        layout_acoes.addWidget(btn_confirm, 2)

        layout_principal.addWidget(container)
        layout_principal.addSpacing(30)
        layout_principal.addWidget(container_keys)
        layout_principal.addStretch()
        layout_principal.addLayout(layout_acoes)

        self.set_target(self.input_nome)

    def set_target(self, input_field):
        self.target_input = input_field
        input_field.setFocus()

    def processar_tecla(self, tecla):
        if not self.target_input: return
        if tecla == '⌫':
            self.target_input.backspace()
        elif tecla == 'LIMPAR':
            self.target_input.clear()
        elif tecla == 'ESPAÇO':
            self.target_input.insert(" ")
        else:
            self.target_input.insert(tecla)
        if self.target_input == self.input_cpf: self.formatar_cpf()

    def formatar_cpf(self):
        nums = ''.join(filter(str.isdigit, self.input_cpf.text()))[:11]
        fmt = ""
        for i, c in enumerate(nums):
            if i == 3 or i == 6:
                fmt += "."
            elif i == 9:
                fmt += "-"
            fmt += c
        self.input_cpf.blockSignals(True)
        self.input_cpf.setText(fmt)
        self.input_cpf.blockSignals(False)

    def finalizar(self):
        nome = self.input_nome.text().strip()
        cpf = self.input_cpf.text().strip()

        if len(nome) < 3 or len(cpf) < 14:
            self.title.setText("⚠️ PREENCHA TODOS OS CAMPOS!")
            self.title.setStyleSheet("color: #ff4d4d; font-weight: bold;")
            return  # Bloqueia o avanço

        self.parent.setCurrentWidget(self.parent.terminal)
