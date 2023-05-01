# Sean Driscoll
# CS 535
# RISC-J ISA Simulator

import sys
import time

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QListWidget, QVBoxLayout, QListWidgetItem, QAbstractItemView, QFileDialog)


class Dialog(QDialog):
    num_grid_rows = 3
    num_buttons = 4
    clock = 0
    mem_clock_count = 100
    l1_clock_count = 3
    file_open = False
    file_name = ''
    breakLine = -1
    pc = 0
    memory = {
        "0x0000": "0x0000",
        "0x0001": "0x0000",
        "0x0002": "0x0000",
        "0x0003": "0x0000",
        "0x0004": "0x0000",
        "0x0005": "0x0000",
        "0x0006": "0x0000",
        "0x0007": "0x0000",
        "0x0008": "0x0000",
        "0x0009": "0x0000",
        "0x000a": "0x0000",
        "0x000b": "0x0000",
        "0x000c": "0x0000",
        "0x000d": "0x0000",
        "0x000e": "0x0000",
        "0x000f": "0x0000"
    }

    cache_l1 = {  # index, valid bit, [tag, data]x4 (rightmost 5 address bits = [4:2]  3 bits for index, [1:0]  2 bits for offset within row)
        "000": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "001": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "010": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "011": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "100": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "101": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "110": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "111": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]]
        # set 111's valid bit to 1 for demo purposed, change back to 0 for testing
    }

    registers = {
        "0x0000": "0x0000",
        "0x0001": "0x0000",
        "0x0002": "0x0000",
        "0x0003": "0x0000",
        "0x0004": "0x0000",
        "0x0005": "0x0000",
        "0x0006": "0x0000",
        "0x0007": "0x0000",
        "0x0008": "0x0000",
        "0x0009": "0x0000",
        "0x000a": "0x0000",
        "0x000b": "0x0000",
        "0x000c": "0x0000",
        "0x000d": "0x0000",
        "0x000e": "0x0000",
        "0x000f": "0x0000",
        "0x0010": "0x0000",
        "0x0011": "0x0000",
        "0x0012": "0x0000",
        "0x0013": "0x0000",
        "0x0014": "0x0000",
        "0x0015": "0x0000",
        "0x0016": "0x0000",
        "0x0017": "0x0000",
        "0x0018": "0x0000",
        "0x0019": "0x0000",
        "0x001a": "0x0000",
        "0x001b": "0x0000",
        "0x001c": "0x0000",
        "0x001d": "0x0000",
        "0x001e": "0x0000",
        "0x001f": "0x0000"
    }

    def __init__(self):
        super().__init__()

        self.create_menu()
        self.create_horizontal_group_box()
        # self.create_grid_group_box()
        self.create_form_group_box()

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.main_layout = QVBoxLayout()
        self.main_layout.setMenuBar(self._menu_bar)
        self.main_layout.addWidget(self._form_group_box)
        self.main_layout.addWidget(self._horizontal_group_box)
        # self.main_layout.addWidget(self._grid_group_box)
        self.main_layout.addWidget(button_box)
        self.setLayout(self.main_layout)
        self.resize(1200, 500)
        self.setWindowTitle("RISC-J Simulation Driver")

    def create_cache(self):
        self._cache = QListWidget(self)
        self._cache.setGeometry(50, 70, 150, 80)
        # list widget items

        self._cache.addItem(
            "index      v      tag         word         tag         word        tag         word        tag         word")
        for addr in self.cache_l1:
            item1 = QListWidgetItem("{:>4}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}".format(
                addr, str(self.cache_l1[addr][0][0]), toHexString(str(self.cache_l1[addr][1][0])), str(
                    self.cache_l1[addr][1][1]),
                toHexString(str(self.cache_l1[addr][2][0])), str(
                    self.cache_l1[addr][2][1]),
                toHexString(str(self.cache_l1[addr][3][0])), str(
                    self.cache_l1[addr][3][1]),
                toHexString(str(self.cache_l1[addr][4][0])), str(self.cache_l1[addr][4][1])))
            # adding items to the list widget
            self._cache.addItem(item1)

        # setting vertical scroll mode
        self._cache.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # resetting horizontal scroll mode
        self._cache.resetHorizontalScrollMode()

    def create_mem(self):
        self._mem = QListWidget(self)
        self._mem.setMaximumWidth(130)
        # list widget items

        self._mem.addItem("address     value")
        for addr in self.memory:
            item1 = QListWidgetItem("{:>6}{:>12}".format(
                addr, self.memory[addr]))
            # adding items to the list widget
            self._mem.addItem(item1)

        # setting vertical scroll mode
        self._mem.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # resetting horizontal scroll mode
        self._mem.resetHorizontalScrollMode()

        # # creating a label
        # label = QLabel("Memory", self)

        # # setting geometry to the label
        # label.setGeometry(15, 5, 280, 80)

        # # making label multi line
        # label.setWordWrap(True)

    def create_menu(self):
        self._menu_bar = QMenuBar()

        self._file_menu = QMenu("&File", self)
        self._open_dialog = QFileDialog()
        self._open_action = self._file_menu.addAction("Open")
        self._open_action.triggered.connect(self.read_file)
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)
        self._exit_action.triggered.connect(self.accept)

    def read_file(self):
        self.read_file_from(self.pc)

    def read_file_from(self, lineNum):
        if self.file_name == '':
            self.file_name = QFileDialog.getOpenFileName(
                self, "Open", "D:\Classes\CS 535\Binary files")[0]
        self.file = open(self.file_name, 'r')
        self.setWindowTitle(
            "RISC-J Simulation Driver - reading " + self.file_name)
        self.breakLine = self.breakline_input.text()
        for line in self.file.readlines():
            if (lineNum > 0):
                lineNum -= 1
            else:
                print("pc: ", self.pc, " break: ", self.breakLine)
                if str(self.pc) == str(self.breakLine):
                    print("breaking")
                    self.file.close()
                    break
                if (len(line) >= 32):
                    self.decode(line.strip())
                    self.pc += 1
        self.file.close()

    def create_reg(self):
        self._reg = QListWidget(self)
        self._reg.addItem("register     value")
        self._reg.setMaximumWidth(130)

        for addr in self.registers:
            item1 = QListWidgetItem("{:>6}{:>12}".format(
                addr, self.registers[addr]))
            # adding items to the list widget
            self._reg.addItem(item1)

        # setting vertical scroll mode
        self._reg.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # resetting horizontal scroll mode
        self._reg.resetHorizontalScrollMode()

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QGroupBox(
            "Registers                               Memory                              Cache")
        layout = QHBoxLayout()
        self.create_mem()
        self.create_cache()
        self.create_reg()
        layout.addWidget(self._reg)
        layout.addWidget(self._mem)
        layout.addWidget(self._cache)

        self._horizontal_group_box.setLayout(layout)

    # def create_grid_group_box(self):
    #     self._grid_group_box = QGroupBox("Grid layout")
    #     layout = QGridLayout()

    #     for i in range(Dialog.num_grid_rows):
    #         label = QLabel(f"Line {i + 1}:")
    #         line_edit = QLineEdit()
    #         layout.addWidget(label, i + 1, 0)
    #         layout.addWidget(line_edit, i + 1, 1)

    #     self._small_editor = QTextEdit()
    #     self._small_editor.setPlainText("This widget takes up about two thirds "
    #                                     "of the grid layout.")

    #     layout.addWidget(self._small_editor, 0, 2, 4, 1)

    #     layout.setColumnStretch(1, 10)
    #     layout.setColumnStretch(2, 20)
    #     self._grid_group_box.setLayout(layout)

    def create_form_group_box(self):
        self._form_group_box = QGroupBox("Controls")
        layout = QFormLayout()
        self.cl = QLabel(str(self.clock))
        layout.addRow(QLabel("Clock:"), self.cl)
        self.addr_input = QLineEdit()
        self.val_input = QLineEdit()
        self.val2_input = QLineEdit()
        self.breakline_input = QLineEdit()
        layout.addRow(QLabel("Address:"), self.addr_input)
        layout.addRow(QLabel("Value 1:"), self.val_input)
        layout.addRow(QLabel("Value 2:"), self.val2_input)
        layout.addRow(QLabel("Break Line:"), self.breakline_input)
        self.addr_input.setMaximumWidth(100)
        self.val_input.setMaximumWidth(100)
        self.val2_input.setMaximumWidth(100)
        self.breakline_input.setMaximumWidth(100)

        self.cb = QComboBox()
        self.cb.addItem("add")
        self.cb.addItem("sub")
        self.cb.addItem("mul")
        self.cb.addItem("div")
        self.cb.addItem("mod")
        self.cb.addItem("xor")
        self.cb.addItem("or")
        self.cb.addItem("and")
        self.cb.addItem("sll")
        self.cb.addItem("srl")
        self.cb.addItem("addi")
        self.cb.addItem("xori")
        self.cb.addItem("ori")
        self.cb.addItem("andi")
        self.cb.addItem("slli")
        self.cb.addItem("srli")
        self.cb.addItem("sb")
        self.cb.addItem("sh")
        self.cb.addItem("sw")
        self.cb.addItem("lb")
        self.cb.addItem("lh")
        self.cb.addItem("lw")
        self.cb.addItem("beq")
        self.cb.addItem("bne")
        self.cb.addItem("blt")
        self.cb.addItem("bgt")
        self.cb.addItem("jal")
        self.cb.addItem("jalr")
        self.cb.setMaximumWidth(100)
        layout.addRow(QLabel("Function:"), self.cb)
        self.fun_button = QPushButton("Go")
        self.fun_button.setCheckable(False)
        self.fun_button.setMaximumWidth(50)
        self.fun_button.setStyleSheet("background: lightgreen")
        self.fun_button.clicked.connect(self.execute)
        layout.addWidget(self.fun_button)
        self._form_group_box.setLayout(layout)

    def decode(self, line):
        self.opcode = line[-4::]
        if self.opcode == "0000":  # R-format
            self.rd = line[-9:-4]
            self.function = line[-13:-9]
            self.rs1 = line[-18:-13]
            self.rs2 = line[-23:-18]
            self.addr_input.setText(hex(int(self.rd, 2)))
            self.val_input.setText(hex(int(self.rs1, 2)))
            self.val2_input.setText(hex(int(self.rs2, 2)))
            if self.function == "0000":  # add
                self.cb.setCurrentText("add")
        elif self.opcode == "0001":  # I-format
            self.rd = line[-9:-4]
            self.function = line[-13:-9]
            self.rs1 = line[-18:-13]
        elif self.opcode == "0011":  # S-format
            self.function = line[-8:-4]
            self.rs1 = line[-13:-8]
            self.rs2 = line[-18:-13]
            self.immediate = line[-32:-18]
            self.addr_input.setText(
                hex(int(self.rs1, 2) + int(self.immediate, 2)))
            if self.function == "0001":  # store half
                self.cb.setCurrentText("sh")
                self.val_input.setText(hex(int(self.rs2, 2)))
            elif self.function == "0100":  # load half
                self.cb.setCurrentText("lh")
        self.execute()

    def execute(self):
        # store function
        if self.cb.currentText() in ["sb", "sh", "sw"]:
            print("Putting ", self.val_input.text(),
                  " in address location : ", self.addr_input.text())
            self.memory[self.addr_input.text()] = toHexString(
                str(self.val_input.text()))
            self._mem.item(int(self.addr_input.text(), 16) + 1).setText(
                "{:>6}{:>12}".format(self._mem.item(int(self.addr_input.text(), 16) + 1).text()[0:6], toHexString(self.val_input.text())))
            self.clock += self.mem_clock_count

        # load function
        elif self.cb.currentText() in ["lb", "lh", "lw"]:
            print("Getting data from address location : ", self.addr_input.text())
            for row in list(self.cache_l1):
                tag = str(bin(int(self.addr_input.text(), 16))[2:].zfill(32))
                index = tag[-5:-2]
                if row == index:
                    offset = int(tag[-2::], 2)
                    print('tag1: ', tag)
                    tag = tag[0:27]
                    print('tag2: ', str(hex(int(tag, 2))))
                    block = self.cache_l1[row][offset+1]
                    # print('valid: ', self.cache_l1[row])
                    # tag found in cache and valid bit is 0
                    if ['1'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000":
                        print('found in cache!')
                        fetched_data = block[1]
                        self.clock += self.l1_clock_count
                    # address in memory
                    elif self.addr_input.text() in self.memory:
                        self.clock += self.mem_clock_count
                        fetched_data = toHexString(
                            self.memory[self.addr_input.text()])
                        # populate cache
                        tag = str(bin(int(self.addr_input.text(), 16))[
                                  2:].zfill(32))
                        index = tag[-5:-2]
                        offset = int(tag[-2::], 2)
                        print('first tag is: ', tag)
                        tag = tag[0:27]
                        print('altered tag is ', tag)
                        print('final tag is: ', str(hex(int(tag, 2))))
                        self.cache_l1[index][offset+1][0] = hex(int(tag, 2))
                        self.cache_l1[index][offset+1][1] = fetched_data
                        self.cache_l1[row][0] = ["1"]
                        self._cache.item(int(index) + 1).setText("{:>4}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}".format(
                            index, str(self.cache_l1[index][0][0]), toHexString(str(self.cache_l1[index][1][0])), str(
                                self.cache_l1[index][1][1]),
                            toHexString(str(self.cache_l1[index][2][0])), str(
                                self.cache_l1[index][2][1]),
                            toHexString(str(self.cache_l1[index][3][0])), str(
                                self.cache_l1[index][3][1]),
                            toHexString(str(self.cache_l1[index][4][0])), str(self.cache_l1[index][4][1])))
                        self.clock += self.l1_clock_count
                    print("FETCHED DATA: ", fetched_data)
                    self.registers[self.addr_input.text()] = fetched_data
                    self._reg.item(int(self.addr_input.text(), 16) + 1).setText(
                        "{:>6}{:>12}".format(self._reg.item(int(self.addr_input.text(), 16) + 1).text()[0:6], fetched_data))
        elif self.cb.currentText() == "add":
            regAddress = str(self.addr_input.text())
            reg1 = str(self.val_input.text())
            reg2 = str(self.val2_input.text())
            print("adding reg1: ", reg1, " and reg2: ", reg2)
            self.registers[int(regAddress, 16)] = hex(int(self.registers[reg1], 16) +
                                                      int(self.registers[reg2], 16))
            self._reg.item(int(self.addr_input.text(), 16) + 1).setText(
                "{:>6}{:>12}".format(self._reg.item(int(self.addr_input.text(), 16) + 1).text()[0:6], toHexString(str(hex(int(self.registers[reg1], 16) +
                                                                                                                          int(self.registers[reg2], 16))))))
            print("result: ", hex(int(self.registers[reg1], 16) +
                                  int(self.registers[reg2], 16)))
            # print('addr: ', self.registers[regAddress])
            # print('1: ', self.registers[reg1])
            # print('2: ', self.registers[reg2])

        # update clock, register, memory, and cache UI
        self.cl.setText(str(self.clock))
        # dummy = QListWidget()
        # dummy.hide()
        # self.main_layout.replaceWidget(self._horizontal_group_box, dummy)
        # self.create_horizontal_group_box()
        # self.main_layout.replaceWidget(dummy, self._horizontal_group_box)
        # self.main_layout.removeWidget(dummy)


def toHexString(s):
    s = s[2:]
    newS = "0x"
    for x in range(4 - len(s)):
        newS += "0"
    newS += s
    return newS


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec())
