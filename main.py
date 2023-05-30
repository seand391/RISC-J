# Sean Driscoll
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
    memOffset = 0
    progLen = 0
    fLockedUntil = 0
    dLockedUntil = 0
    eLockedUntil = 0
    mLockedUntil = 0
    wLockedUntil = 0
    newInstr = False
    newDecode = False
    pipeEnabled = True
    cacheEnabled = True
    nextAddress = "0x0000"
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
    # index, valid bit, [tag, data]x4 (rightmost 5 address bits = [4:2]  3 bits for index, [1:0]  2 bits for offset within row)
    cache_l1 = {
        "000": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "001": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "010": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "011": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "100": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "101": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "110": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]],
        "111": [["0"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]]
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
        self.create_form_group_box()

        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        self.main_layout = QVBoxLayout()
        self.main_layout.setMenuBar(self._menu_bar)
        self.main_layout.addWidget(self._form_group_box)
        self.main_layout.addWidget(self._horizontal_group_box)
        self.main_layout.addWidget(button_box)
        self.setLayout(self.main_layout)
        self.resize(1920, 1015)
        self.setWindowTitle("RISC-J Simulation Driver")

    def create_cache(self):
        self._cache = QListWidget(self)
        self._cache.setGeometry(50, 70, 150, 80)
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
            self._cache.addItem(item1)
        self._cache.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self._cache.resetHorizontalScrollMode()

    def create_mem(self):
        self._mem = QListWidget(self)
        self._mem.setMaximumWidth(130)
        self._mem.addItem("address     value")
        for addr in self.memory:
            item1 = QListWidgetItem("{:>6}{:>12}".format(
                addr, self.memory[addr]))
            self._mem.addItem(item1)
        self._mem.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self._mem.resetHorizontalScrollMode()

    def create_reg(self):
        self._reg = QListWidget(self)
        self._reg.addItem("register     value")
        self._reg.setMaximumWidth(130)
        for addr in self.registers:
            item1 = QListWidgetItem("{:>6}{:>12}".format(
                addr, self.registers[addr]))
            self._reg.addItem(item1)
        self._reg.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
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

    def create_form_group_box(self):
        self._form_group_box = QGroupBox("Controls")
        layout = QFormLayout()
        self.cl = QLabel(str(self.clock))
        layout.addRow(QLabel("Clock:"), self.cl)
        self.addr_input = QLineEdit()
        self.val_input = QLineEdit()
        self.val2_input = QLineEdit()
        self.breakline_input = QLineEdit()
        self.cachePipe = QComboBox()
        self.cachePipe.addItem("Both on")
        self.cachePipe.addItem("Cache only")
        self.cachePipe.addItem("Pipe only")
        self.cachePipe.addItem("Both off")
        self.cachePipe.setMaximumWidth(100)
        layout.addRow(QLabel("Cache / Pipe:"), self.cachePipe)
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
        self.fun_button = QPushButton("Manual Instruction")
        self.fun_button.setCheckable(False)
        self.fun_button.setMaximumWidth(120)
        self.fun_button.setStyleSheet("background: lightgreen")
        self.fun_button.clicked.connect(self.execute)
        layout.addWidget(self.fun_button)
        self.step_button = QPushButton("Step 1 Instruction")
        self.step_button.setCheckable(False)
        self.step_button.setMaximumWidth(120)
        self.step_button.setStyleSheet("background: yellow")
        self.step_button.clicked.connect(self.read_file_1)
        layout.addWidget(self.step_button)
        self.step_button = QPushButton("Step 1 Clock Cycle")
        self.step_button.setCheckable(False)
        self.step_button.setMaximumWidth(120)
        self.step_button.setStyleSheet("background: lightblue")
        self.step_button.clicked.connect(self.cycle1)
        layout.addWidget(self.step_button)
        self._form_group_box.setLayout(layout)

    def cycle1(self):
        self.breakline_input.setText("1 cycle")
        self.read_file()

    def create_menu(self):
        self._menu_bar = QMenuBar()

        self._file_menu = QMenu("&File", self)
        self._open_dialog = QFileDialog()
        self._open_action = self._file_menu.addAction("Open")
        self._open_action.triggered.connect(self.read_file)
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)
        self._exit_action.triggered.connect(self.accept)

    def nextAddr(self):
        temp = self.nextAddress
        self.nextAddress = toHexString(str(hex(int(self.nextAddress, 16) + 1)))
        return temp

    def loadToMemory(self, fileName):
        self.file = open(fileName, 'r')
        self.setWindowTitle(
            "RISC-J Simulation Driver - reading " + fileName)
        for line in self.file.readlines():
            self.progLen += 1
            self.memOffset += 2
            firstHalf = hex(int(line[0:16], 2))
            lastHalf = hex(int(line[16:32], 2))
            a = self.nextAddr()
            self.memory[a] = toHexString(
                str(firstHalf))
            if int(a, 16) + 1 < self._mem.count():
                self._mem.item(int(a, 16) + 1).setText(
                    "{:>6}{:>12}".format(self._mem.item(int(a, 16) + 1).text()[0:6], toHexString(str(firstHalf))))
            else:
                item = QListWidgetItem("{:>6}{:>12}".format(
                    a, self.memory[a]))
                self._mem.addItem(item)
            a = self.nextAddr()
            self.memory[a] = toHexString(
                str(lastHalf))
            if int(a, 16) + 1 < self._mem.count():
                self._mem.item(int(a, 16) + 1).setText(
                    "{:>6}{:>12}".format(self._mem.item(int(a, 16) + 1).text()[0:6], toHexString(str(lastHalf))))
            else:
                item = QListWidgetItem("{:>6}{:>12}".format(
                    a, self.memory[a]))
                self._mem.addItem(item)
        self.file.close()

    def read_file(self):
        # first time opening
        if self.file_name == '':
            self.file_name = QFileDialog.getOpenFileName(
                self, "Open", "D:\Classes\CS 535\Binary files")[0]
            self.loadToMemory(self.file_name)
        self.breakLine = self.breakline_input.text()

        while (self.pc < self.progLen) or self.eLockedUntil > self.clock - 1:
            if str(self.pc) == str(self.breakLine):
                self.file.close()
                break
            else:
                self.fetch()
                if self.breakLine == "1 cycle":
                    self.file.close()
                    break

    def read_file_1(self):
        self.breakline_input.setText(str(self.pc + 1))
        self.read_file()

    def fetch(self):
        if self.clock == self.fLockedUntil and self.pc < self.progLen and (self.cachePipe.currentText() in ["Both on", "Pipe only"] or self.clock > self.eLockedUntil):
            if self.cachePipe.currentText() in ["Both on", "Cache only"]:
                for row in list(self.cache_l1):
                    tag = str(bin(int(toHexString((str(hex(self.pc * 2)))), 16))
                              [2:].zfill(32))
                    index = tag[-5:-2]
                    if row == index:
                        offset = int(tag[-2::], 2)
                        tag = tag[0:27]
                        block = self.cache_l1[row][offset+1]
                        # tag found in cache and valid bit is 0
                        if ['1'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000":
                            fetched_data = block[1]
                        # address in memory
                        elif toHexString((str(hex(self.pc * 2)))) in self.memory:
                            fetched_data = toHexString(
                                self.memory[toHexString((str(hex(self.pc * 2))))])
                            # populate cache
                            tag = str(bin(int(toHexString((str(hex(self.pc * 2)))), 16))[
                                2:].zfill(32))
                            index = tag[-5:-2]
                            offset = int(tag[-2::], 2)
                            tag = tag[0:27]
                            self.cache_l1[index][offset +
                                                 1][0] = hex(int(tag, 2))
                            self.cache_l1[index][offset+1][1] = fetched_data
                            self.cache_l1[row][0] = ["1"]
                            self._cache.item(int(index, 2) + 1).setText("{:>4}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}".format(
                                index, str(self.cache_l1[index][0][0]), toHexString(str(self.cache_l1[index][1][0])), str(
                                    self.cache_l1[index][1][1]),
                                toHexString(str(self.cache_l1[index][2][0])), str(
                                    self.cache_l1[index][2][1]),
                                toHexString(str(self.cache_l1[index][3][0])), str(
                                    self.cache_l1[index][3][1]),
                                toHexString(str(self.cache_l1[index][4][0])), str(self.cache_l1[index][4][1])))
                        instP1 = fetched_data

                    for row in list(self.cache_l1):
                        tag = str(bin(int(toHexString((str(hex(self.pc * 2)))), 16))
                                  [2:].zfill(32))
                        index = tag[-5:-2]
                        if row == index:
                            offset = int(tag[-2::], 2)
                            tag = tag[0:27]
                            block = self.cache_l1[row][offset+1]
                            # tag found in cache and valid bit is 0
                            if ['1'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000":
                                fetched_data = block[1]
                            # address in memory
                            elif toHexString((str(hex(self.pc * 2 + 1)))) in self.memory:
                                fetched_data = toHexString(
                                    self.memory[toHexString((str(hex(self.pc * 2 + 1))))])
                                # populate cache
                                tag = str(bin(int(toHexString((str(hex(self.pc * 2 + 1)))), 16))[
                                    2:].zfill(32))
                                index = tag[-5:-2]
                                offset = int(tag[-2::], 2)
                                tag = tag[0:27]
                                self.cache_l1[index][offset +
                                                     1][0] = hex(int(tag, 2))
                                self.cache_l1[index][offset +
                                                     1][1] = fetched_data
                                self.cache_l1[row][0] = ["1"]
                                self._cache.item(int(index, 2) + 1).setText("{:>4}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}".format(
                                    index, str(self.cache_l1[index][0][0]), toHexString(str(self.cache_l1[index][1][0])), str(
                                        self.cache_l1[index][1][1]),
                                    toHexString(str(self.cache_l1[index][2][0])), str(
                                        self.cache_l1[index][2][1]),
                                    toHexString(str(self.cache_l1[index][3][0])), str(
                                        self.cache_l1[index][3][1]),
                                    toHexString(str(self.cache_l1[index][4][0])), str(self.cache_l1[index][4][1])))
                            instP2 = fetched_data

            instP1 = self.memory[toHexString((str(hex(self.pc * 2))))]
            instP2 = self.memory[toHexString(str(hex(self.pc * 2 + 1)))]
            self.registers["0x0002"] = instP1
            self.registers["0x0003"] = instP2
            self.pc += 1
            self.registers["0x0001"] = toHexString(str(self.pc))
            self._reg.item(2).setText(
                "{:>6}{:>12}".format(self._reg.item(2).text()[
                    0:6], toHexString(str(self.pc))))
            self._reg.item(3).setText(
                "{:>6}{:>12}".format(self._reg.item(3).text()[
                    0:6], instP1))
            self._reg.item(4).setText(
                "{:>6}{:>12}".format(self._reg.item(4).text()[
                    0:6], instP2))
            self.newInstr = True
        elif self.clock > self.fLockedUntil:
            inCache = False
            if self.cachePipe.currentText() in ["Both on", "Cache only"]:
                # check if instructions are already in cache
                for row in list(self.cache_l1):
                    tag = str(bin(int(toHexString((str(hex(self.pc * 2)))), 16))
                              [2:].zfill(32))
                    index = tag[-5:-2]
                    if row == index:
                        offset = int(tag[-2::], 2)
                        tag = tag[0:27]
                        block = self.cache_l1[row][offset+1]
                        # tag found in cache and valid bit is 0
                        if ['1'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000":
                            inCache = True
            if inCache == False:
                self.fLockedUntil = self.clock + self.mem_clock_count
            else:
                self.fLockedUntil = self.clock + self.l1_clock_count
        # else:
        self.decode()

    def decode(self):
        if self.clock > self.eLockedUntil and self.newInstr == True:
            self.newInstr = False
            self.newDecode = True
            lineP1 = str(bin(int(self.registers["0x0002"], 16)))[2::].zfill(16)
            lineP2 = str(bin(int(self.registers["0x0003"], 16)))[2::].zfill(16)
            line = lineP1 + lineP2

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
                elif self.function == "0001":
                    self.cb.setCurrentText("sub")
                elif self.function == "0010":
                    self.cb.setCurrentText("mul")
                elif self.function == "0011":
                    self.cb.setCurrentText("div")
                elif self.function == "0100":
                    self.cb.setCurrentText("mod")
                elif self.function == "0101":
                    self.cb.setCurrentText("xor")
                elif self.function == "0110":
                    self.cb.setCurrentText("or")
                elif self.function == "0111":
                    self.cb.setCurrentText("and")
                elif self.function == "1000":
                    self.cb.setCurrentText("sll")
                elif self.function == "1001":
                    self.cb.setCurrentText("srl")
            elif self.opcode == "0001":  # I-format
                self.rd = line[-9:-4]
                self.function = line[-13:-9]
                self.rs1 = line[-18:-13]
                self.immediate = line[-32:-18]
                self.addr_input.setText(hex(int(self.rd, 2)))
                self.val_input.setText(hex(int(self.rs1, 2)))
                self.val2_input.setText('')
                if self.function == "0000":
                    self.cb.setCurrentText("addi")
                elif self.function == "0001":
                    self.cb.setCurrentText("xori")
                elif self.function == "0010":
                    self.cb.setCurrentText("ori")
                elif self.function == "0011":
                    self.cb.setCurrentText("andi")
                elif self.function == "0100":
                    self.cb.setCurrentText("slli")
                elif self.function == "0101":
                    self.cb.setCurrentText("srli")
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
                    self.val_input.setText(hex(int(self.rs2, 2)))
            elif self.opcode == "0100":  # C-format
                self.function = line[-8:-4]
                if self.function == "0000":
                    self.cb.setCurrentText("beq")
                elif self.function == "0001":
                    self.cb.setCurrentText("bne")
                elif self.function == "0010":
                    self.cb.setCurrentText("blt")
                elif self.function == "0011":
                    self.cb.setCurrentText("bge")
                self.rs1 = line[-13:-8]
                self.rs2 = line[-18:-13]
                self.immediate = line[-31:-18]
                self.sign = line[-32]
            elif self.opcode == "0101":  # J-format
                self.function = line[-4]
                if self.function == "1":
                    self.cb.setCurrentText("jalr")
                else:
                    self.cb.setCurrentText("jal")
                self.rd = line[-10:-5]
                self.immediate = line[-31:-10]
                self.sign = line[-32]
        # else:
        self.execute()

    def execute(self):
        if self.clock == self.eLockedUntil and self.clock != 0:
            # store function
            if self.cb.currentText() in ["sb", "sh", "sw"]:
                self.memory[toHexString(str(hex(int(self.registers[toHexString(str(self.addr_input.text()))], 16) + self.memOffset)))] = toHexString(
                    str(self.registers[toHexString(self.val_input.text())]))
                if self._mem.item(int(self.addr_input.text(), 16) + 1 + self.memOffset) != None:
                    self._mem.item(int(self.addr_input.text(), 16) + 1 + self.memOffset).setText(
                        "{:>6}{:>12}".format(self._mem.item(int(self.addr_input.text(), 16) + 1 + self.memOffset).text()[0:6], toHexString(self.registers[toHexString(self.val_input.text())])))
                else:
                    row = toHexString(
                        str(hex(int(self.registers[toHexString(str(self.addr_input.text()))], 16) + 1 + self.memOffset)))
                    item1 = QListWidgetItem("{:>6}{:>12}".format(
                        row, self.memory[toHexString(str(hex(int(self.registers[toHexString(str(self.addr_input.text()))], 16) + self.memOffset)))]))

                    self._mem.addItem(item1)

            # load function
            elif self.cb.currentText() in ["lb", "lh", "lw"]:
                #      self.addr_input.text())
                for row in list(self.cache_l1):
                    tag = str(bin(int(self.addr_input.text(), 16))
                              [2:].zfill(32))
                    index = tag[-5:-2]
                    if row == index:
                        offset = int(tag[-2::], 2)
                        tag = tag[0:27]
                        block = self.cache_l1[row][offset+1]
                        fetched_data = "0"
                        if ['1'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000" and self.cachePipe.currentText() in ["Both on", "Cache only"]:
                            fetched_data = block[1]
                        # address in memory
                        elif toHexString(str(hex(int(self.registers[toHexString(str(self.addr_input.text()))], 16) + self.memOffset))) in self.memory:
                            fetched_data = toHexString(
                                self.memory[toHexString(
                                    str(hex(int(self.registers[toHexString(str(self.addr_input.text()))], 16) + self.memOffset)))])
                            if self.cachePipe.currentText() in ["Both on", "Cache only"]:
                                # populate cache
                                tag = str(bin(int(self.addr_input.text(), 16))[
                                    2:].zfill(32))
                                index = tag[-5:-2]
                                offset = int(tag[-2::], 2)
                                tag = tag[0:27]
                                self.cache_l1[index][offset +
                                                     1][0] = hex(int(tag, 2))
                                self.cache_l1[index][offset +
                                                     1][1] = fetched_data
                                self.cache_l1[row][0] = ["1"]
                                self._cache.item(int(index, 2) + 1).setText("{:>4}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}{:>10}".format(
                                    index, str(self.cache_l1[index][0][0]), toHexString(str(self.cache_l1[index][1][0])), str(
                                        self.cache_l1[index][1][1]),
                                    toHexString(str(self.cache_l1[index][2][0])), str(
                                        self.cache_l1[index][2][1]),
                                    toHexString(str(self.cache_l1[index][3][0])), str(
                                        self.cache_l1[index][3][1]),
                                    toHexString(str(self.cache_l1[index][4][0])), str(self.cache_l1[index][4][1])))
                        self.registers[toHexString(str(
                            self.val_input.text()))] = fetched_data
                        self._reg.item(int(self.val_input.text(), 16) + 1).setText(
                            "{:>6}{:>12}".format(self._reg.item(int(self.val_input.text(), 16) + 1).text()[0:6], fetched_data))
            elif self.cb.currentText() in ["add", "sub", "mul", "div", "mod", "xor", "or", "and", "sll", "srl"]:
                regAddress = toHexString(str(self.addr_input.text()))
                reg1 = toHexString(str(self.val_input.text()))
                reg2 = toHexString(str(self.val2_input.text()))
                if self.cb.currentText() == "add":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) + int(self.registers[reg2], 16))))
                elif self.cb.currentText() == "sub":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) - int(self.registers[reg2], 16))))
                elif self.cb.currentText() == "mul":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) * int(self.registers[reg2], 16))))
                elif self.cb.currentText() == "div":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) / int(self.registers[reg2], 16))))
                elif self.cb.currentText() == "xor":
                    res = toHexString(
                        str(hex(bool(int(self.registers[reg1], 16)) ^ bool(int(self.registers[reg2], 16)))))
                elif self.cb.currentText() == "mod":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) % int(self.registers[reg2], 16))))
                elif self.cb.currentText() == "or":
                    res = toHexString(
                        str(hex(bool(int(self.registers[reg1], 16)) or bool(int(self.registers[reg2], 16)))))
                elif self.cb.currentText() == "and":
                    res = toHexString(
                        str(hex(bool(int(self.registers[reg1], 16)) and bool(int(self.registers[reg2], 16)))))
                elif self.cb.currentText() == "sll":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) << int(self.registers[reg2], 16))))
                elif self.cb.currentText() == "srl":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) >> int(self.registers[reg2], 16))))
                self.registers[regAddress] = res
                self._reg.item(int(self.addr_input.text(), 16) + 1).setText(
                    "{:>6}{:>12}".format(self._reg.item(int(self.addr_input.text(), 16) + 1).text()[0:6], res))
            elif self.cb.currentText() in ["addi", "xori", "ori", "andi", "slli", "srli"]:
                regAddress = toHexString(str(self.addr_input.text()))
                reg1 = toHexString(str(self.val_input.text()))
                if self.cb.currentText() == "addi":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) + int(self.immediate, 2))))
                elif self.cb.currentText() == "xori":
                    res = toHexString(
                        str(hex(bool(self.registers[reg1], 16) ^ bool(self.immediate, 2))))
                elif self.cb.currentText() == "ori":
                    res = toHexString(
                        str(hex(bool(self.registers[reg1], 16) or bool(self.immediate, 2))))
                elif self.cb.currentText() == "andi":
                    res = toHexString(
                        str(hex(bool(self.registers[reg1], 16) and bool(self.immediate, 2))))
                elif self.cb.currentText() == "ori":
                    res = toHexString(
                        str(hex(bool(self.registers[reg1], 16) or bool(self.immediate, 2))))
                elif self.cb.currentText() == "slli":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) << int(self.immediate, 2))))
                elif self.cb.currentText() == "srli":
                    res = toHexString(
                        str(hex(int(self.registers[reg1], 16) >> int(self.immediate, 2))))
                self.registers[regAddress] = res
                self._reg.item(int(self.addr_input.text(), 16) + 1).setText(
                    "{:>6}{:>12}".format(self._reg.item(int(self.addr_input.text(), 16) + 1).text()[0:6], res))

            elif self.cb.currentText() in ["beq", "bne", "blt", "bge"]:

                # flush pipeline
                self.newInstr = False
                self.newDecode = False
                self.fLockedUntil = 0

                self.sign = int(self.sign)
                firstOP = self.registers[toHexString(
                    str(hex(int(self.rs1, 2))))]
                secondOP = self.registers[toHexString(
                    str(hex(int(self.rs2, 2))))]
                if self.cb.currentText() == "beq":
                    if firstOP == secondOP:
                        if self.sign == 0:
                            self.pc += int(self.immediate, 2)
                        else:
                            self.pc -= int(self.immediate, 2)
                elif self.cb.currentText() == "bne":
                    if firstOP != secondOP:
                        if self.sign == 0:
                            self.pc += int(self.immediate, 2)
                        else:
                            self.pc -= int(self.immediate, 2)
                if self.cb.currentText() == "blt":
                    if firstOP < secondOP:
                        self.fLockedUntil = 0
                        self.dLockedUntil = 0
                        self.eLockedUntil = 0
                        self.mLockedUntil = 0
                        self.wLockedUntil = 0
                        self.newInstr = False
                        self.newDecode = False
                        if self.sign == 0:
                            self.pc += int(self.immediate, 2)
                        else:
                            self.pc -= int(self.immediate, 2)
                if self.cb.currentText() == "bge":
                    if firstOP >= secondOP:
                        if self.sign == 0:
                            self.pc += int(self.immediate, 2)
                        else:
                            self.pc -= int(self.immediate, 2)
                self.registers["0x0001"] = toHexString(str(self.pc))
                self._reg.item(2).setText(
                    "{:>6}{:>12}".format(self._reg.item(2).text()[
                        0:6], toHexString(str(self.pc))))
            elif self.cb.currentText() in ["jalr", "jal"]:
                if self.sign == "0":  # branch to future instruction
                    self.pc += int(self.immediate, 2)
                else:  # branch to earlier instruction
                    self.pc -= int(self.immediate, 2)
                self.registers["0x0001"] = toHexString(str(self.pc))
                self._reg.item(2).setText(
                    "{:>6}{:>12}".format(self._reg.item(2).text()[
                        0:6], toHexString(str(self.pc))))

        elif self.clock >= self.eLockedUntil and self.newDecode == True:

            self.newDecode = False
            numMemAccesses = 0
            numCacheAccesses = 0
            if self.cb.currentText() in ["lb", "lh", "lw"]:
                for row in list(self.cache_l1):
                    tag = str(bin(int(self.addr_input.text(), 16))
                              [2:].zfill(32))
                    index = tag[-5:-2]
                    if row == index:
                        offset = int(tag[-2::], 2)
                        tag = tag[0:27]
                        block = self.cache_l1[row][offset+1]
                        if ['1'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000":
                            numCacheAccesses += 1
                        else:
                            numMemAccesses += 1
            elif self.cb.currentText() in ["sb", "sh", "sw"]:
                numMemAccesses += 1

            self.eLockedUntil = self.clock + 2 +\
                (numMemAccesses * self.mem_clock_count) + \
                (numCacheAccesses * self.l1_clock_count)
        # else:
        self.clock += 1
        self.cl.setText(str(self.clock))


def toHexString(s):
    if s[0:2] == "0x":
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
