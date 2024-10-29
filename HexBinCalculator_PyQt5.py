from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QPushButton, 
    QVBoxLayout, QRadioButton, QLineEdit, QHBoxLayout, QLabel
)
import sys
from math import sqrt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.number = 0
        self.calculation = None
        self.mode = "dec"  # Başlangıçta decimal mod
        self.buttons = {}  # Tüm butonları burada başlatıyoruz

        self.initUI()  # UI başlatma işlemi

    def initUI(self):
        # Ana layout (dikey)
        main_layout = QVBoxLayout()
        
        # Bilgi etiketi
        self.label = QLabel()
        self.label.setStyleSheet("color: white; font-size: 18px;")
        main_layout.addWidget(self.label)

        # Ekran alanı
        self.display = QLineEdit()
        self.display.setFixedHeight(50)
        self.display.setStyleSheet("font-size: 20px;color: white; background-color: gray;")
        main_layout.addWidget(self.display)

        # On/Off Radyo Butonları için ayrı layout
        power_layout = QHBoxLayout()
        self.radio_on = QRadioButton("On")
        self.radio_off = QRadioButton("Off")
        power_layout.addWidget(self.radio_on)
        power_layout.addWidget(self.radio_off)

        # Mod seçimi için ayrı layout
        mode_layout = QHBoxLayout()
        self.radio_hex = QRadioButton("Hex")
        self.radio_bin = QRadioButton("Bin")
        self.radio_dec = QRadioButton("Dec")
        mode_layout.addWidget(self.radio_hex)
        mode_layout.addWidget(self.radio_bin)
        mode_layout.addWidget(self.radio_dec)

        # RadioButton stilleri ve bağlantıları
        for btn in [self.radio_on, self.radio_off, self.radio_hex, self.radio_bin, self.radio_dec]:
            btn.setStyleSheet("color: white; font-size: 18px;")
        
        self.radio_on.setChecked(True)
        self.radio_on.toggled.connect(self.enable_buttons)
        self.radio_off.toggled.connect(self.disable_buttons)
        self.radio_hex.toggled.connect(self.hex_enable)
        self.radio_bin.toggled.connect(self.bin_enable)
        self.radio_dec.toggled.connect(self.dec_enable)

        main_layout.addLayout(power_layout)
        main_layout.addLayout(mode_layout)

        # Tuş takımı için grid layout
        button_grid = QGridLayout()
        buttons = [
            'sqrt', 'x²', '1/x', '-', 'Or',
            '7', '8', '9', '*', 'And',
            '4', '5', '6', '/', 'Xor',
            '1', '2', '3', '-', 'Not',
            'A', 'B', 'C', '<<', '>>',
            'D', 'E', 'F', 'Clear', '=',
            '0', '.', 'DEL'
        ]

        # Tuşların grid içine yerleştirilmesi ve sözlüğe eklenmesi
        positions = [(i, j) for i in range(7) for j in range(5)]

        for position, text in zip(positions, buttons):
            button = QPushButton(text)
            button.setFixedSize(60, 60)
            button.clicked.connect(self.onButtonClick)
            button.setStyleSheet("font-size: 18px; margin: 5px; background-color: lightgray;")
            button_grid.addWidget(button, *position)
            self.buttons[text] = button  # Butonu sözlüğe ekle

        main_layout.addLayout(button_grid)
        self.setLayout(main_layout)

        # Pencereyi ayarla
        self.setWindowTitle('Calculator')
        self.setGeometry(300, 400, 400, 600)
        self.setStyleSheet("background-color: black;")
        self.show()

    def enable_buttons(self):
        """Enable all buttons when 'On' is selected."""
        self.display.setEnabled(True)
        for button in self.buttons.values():
            button.setEnabled(True)

    def disable_buttons(self):
        """Disable all buttons when 'Off' is selected."""
        for button in self.buttons.values():
            button.setEnabled(False)
        self.display.setEnabled(False)

    def hex_enable(self):
        """Enable Hex mode with A-F buttons."""
        self.enable_buttons()
        self.mode = "hex"
        for button in self.buttons.values():
            if button.text() in 'sqrt1/x':
                button.setEnabled(False)
                if button.text() in '/1':
                    button.setEnabled(True)                

    def bin_enable(self):
        """Enable Binary mode with 0 and 1, operators enabled."""
        self.enable_buttons()
        self.mode = "bin"
        for button in self.buttons.values():
            if button.text() not in '01."DEL","Clear"=<<>>NotXorAndOr-*/+':
                button.setEnabled(False)
            if button.text() in 'ABCDEF':
                button.setEnabled(False)

    def dec_enable(self):
        """Enable Decimal mode."""
        self.enable_buttons()
        self.mode = "dec"
        for letter in "ABCDEF":
            self.buttons[letter].setEnabled(False)

    def onButtonClick(self):
        sender = self.sender().text()
        if sender in '0123456789ABCDEF':
            self.display.setText(self.display.text() + sender)
        elif sender == '.':
            if '.' not in self.display.text():
                self.display.setText(self.display.text() + '.')
        elif sender == 'Clear':
            self.display.clear()
            self.label.clear()
        elif sender == 'DEL':
            self.display.backspace()
        elif sender in ['+', '-', '*', '/', 'And', 'Or', 'Xor','<<', '>>']:
            self.number = self.get_number()
            self.label.setText(self.display.text() + sender)
            self.display.clear()
            self.calculation = sender
        elif sender == 'Not':
            self.number = self.get_number()
            self.label.setText("Not " + self.display.text())
            self.display.clear()
            result = not(self.number) 
            self.display.setText(str(result))
            #self.calculation = sender
        elif sender == '1/x':
            self.number = self.get_number()
            self.label.setText("1/" + self.display.text())
            self.display.clear()
            if self.number != 0:
                result = 1 / self.number
                self.display.setText(str(result))
            else:
                self.display.setText("Error")  # Bölme hatası            
            #self.calculation = sender   
        elif sender == 'sqrt':
            self.number = self.get_number()
            self.label.setText("sqrt( " + self.display.text() + ")")
            self.display.clear()
            #self.number = self.get_number()
            if self.number >= 0:
                result = sqrt(self.number)
                self.display.setText(str(result))
            else:
                self.display.setText("Error")  # Negatif sayının karekökü yok
            
            #self.calculation = sender
        elif sender == 'x²':
            self.number = self.get_number()
            self.label.setText(self.display.text() +"*" + self.display.text())
            self.display.clear()
            result = self.number ** 2
            if self.mode == "hex":
                self.display.setText(hex(int(result))[2:].upper())            
            else:
                self.display.setText(str(result))            
            #self.calculation = sender           
        
        elif sender == '=':
            self.calculate()

    def get_number(self):
        text = self.display.text()
        if self.mode == "hex":
            return int(text, 16)
        elif self.mode == "bin":
            return int(text, 2)
        else:
            return float(text)

    def calculate(self):
        try:
            second_number = self.get_number()
            if self.calculation == '+':
                result = self.number + second_number
            elif self.calculation == '-':
                result = self.number - second_number
            elif self.calculation == '*':
                result = self.number * second_number
            elif self.calculation == '/':
                result = self.number / second_number
            elif self.calculation == 'And':
                result = self.number & second_number
            elif self.calculation == 'Or':
                result = self.number | second_number
            elif self.calculation == 'Xor':
                result = self.number ^ second_number
            elif self.calculation == '<<':
                result = self.number << second_number
            elif self.calculation == '>>':
                result = self.number >> second_number 
            elif self.calculation == '1/x':
                result = 1/(self.number)  
            elif self.calculation == 'sqrt':
                result = sqrt(self.number ) 
            elif self.calculation == 'x²':
                result = self.number ** 2            
                
            if self.mode == "hex":
                self.display.setText(hex(int(result))[2:].upper())
            elif self.mode == "bin":
                self.display.setText(bin(int(result))[2:])
            else:
                self.display.setText(str(result))
            self.label.clear()
        except Exception as e:
            self.display.setText("Error")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    sys.exit(app.exec_())
