# Sean Driscoll
# CS 535
# RISC-J ISA Simulator

import sys

from PySide6.QtWidgets import (QApplication, QComboBox, QDialog,
                               QDialogButtonBox, QGridLayout, QGroupBox,
                               QFormLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton, QSpinBox,
                               QTextEdit, QListWidget, QVBoxLayout, QListWidgetItem, QAbstractItemView)


class Dialog(QDialog):
    num_grid_rows = 3
    num_buttons = 4
    clock = 0
    mem_clock_count = 100
    l1_clock_count = 5
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
        "111": [["1"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"], ["0x0000", "0x0000"]]
        # set 111's valid bit to 1 for demo purposed, change back to 0 for testing
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
                addr, str(self.cache_l1[addr][0][0]), str(self.cache_l1[addr][1][0]), str(
                    self.cache_l1[addr][1][1]),
                str(self.cache_l1[addr][2][0]), str(
                    self.cache_l1[addr][2][1]),
                str(self.cache_l1[addr][3][0]), str(
                    self.cache_l1[addr][3][1]),
                str(self.cache_l1[addr][4][0]), str(self.cache_l1[addr][4][1])))
            # adding items to the list widget
            self._cache.addItem(item1)

        # setting vertical scroll mode
        self._cache.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # resetting horizontal scroll mode
        self._cache.resetHorizontalScrollMode()

    def create_mem(self):
        self._mem = QListWidget(self)
        self._mem.setGeometry(50, 70, 150, 80)
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
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)

        self._exit_action.triggered.connect(self.accept)

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QGroupBox("Memory and Cache")
        layout = QHBoxLayout()
        self.create_mem()
        self.create_cache()
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
        layout.addRow(QLabel("Address:"), self.addr_input)
        layout.addRow(QLabel("Value:"), self.val_input)
        self.cb = QComboBox()
        self.cb.addItem("Store")
        self.cb.addItem("Load")
        layout.addRow(QLabel("Function:"), self.cb)
        self.fun_button = QPushButton("Go")
        self.fun_button.setCheckable(False)
        self.fun_button.clicked.connect(self.go_clicked)
        layout.addWidget(self.fun_button)
        self._form_group_box.setLayout(layout)

    def go_clicked(self):
        # store function
        if self.cb.currentText() == "Store":
            print("Putting ", self.val_input.text(),
                  " in address location : ", self.addr_input.text())
            self.memory[self.addr_input.text()] = str(self.val_input.text())
            self.clock += self.mem_clock_count

        # load function
        else:
            print("Getting data from address location : ", self.addr_input.text())
            for row in list(self.cache_l1):
                tag = str(bin(int(self.addr_input.text(), 16))[2:].zfill(32))
                index = tag[-5:-2]
                if row == index:
                    offset = int(tag[-2::], 2)
                    # print('tag: ', tag)
                    tag = tag[0:27]
                    # print('tag: ', str(hex(int(tag, 2))))
                    block = self.cache_l1[row][offset+1]
                    # print('valid: ', self.cache_l1[row])
                    # tag found in cache
                    if ['0'] in self.cache_l1[row] and int(block[0], 16) == int(hex(int(tag, 2)), 16) and block[1] != "0x0000":
                        print('found in cache!')
                        fetched_data = block[1]
                        self.cache_l1[row][0] = ["0"]
                        self.clock += self.l1_clock_count
                    # address in memory
                    elif self.addr_input.text() in self.memory:
                        self.clock += self.mem_clock_count
                        fetched_data = self.memory[self.addr_input.text()]
                        # populate cache
                        tag = str(bin(int(self.addr_input.text(), 16))[
                                  2:].zfill(32))
                        index = tag[-5:-2]
                        offset = int(tag[-2::], 2)
                        # print('first tag is: ', tag)
                        tag = tag[::27]
                        # print('final tag is: ', str(hex(int(tag, 2))))
                        self.cache_l1[index][offset+1][0] = hex(int(tag, 2))
                        self.cache_l1[index][offset+1][1] = fetched_data
                        self.clock += self.l1_clock_count
                    print("FETCHED DATA: ", fetched_data)
                    self.val_input.setText(str(fetched_data))

        # update clock,  memory, and cache UI
        self.cl.setText(str(self.clock))
        dummy = QListWidget()
        dummy.hide()
        self.main_layout.replaceWidget(self._horizontal_group_box, dummy)
        self.create_horizontal_group_box()
        self.main_layout.replaceWidget(dummy, self._horizontal_group_box)
        self.main_layout.removeWidget(dummy)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = Dialog()
    sys.exit(dialog.exec())
