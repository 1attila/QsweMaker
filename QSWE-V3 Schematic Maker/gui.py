from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QGridLayout, QMessageBox
from PyQt6.QtGui import QIntValidator

import sys

from schem_gen import QsweMaker


class QsweGUI(QWidget):
    """
    QsweMaker GUI
    """

    qswe_maker: QsweMaker
    input_x: QLineEdit
    input_z: QLineEdit
    input_start: QLineEdit
    input_end: QLineEdit
    label_result: QLabel
    label_height: QLabel
    label_status: QLabel


    def __init__(self):

        super().__init__()

        self.setWindowTitle("QSWE Schematic Maker")

        self.qswe_maker = QsweMaker()

        self.input_x = QLineEdit()
        self.input_z = QLineEdit()
        self.input_start = QLineEdit()
        self.input_end = QLineEdit("-59")

        int_validator = QIntValidator()
        self.input_x.setValidator(int_validator)
        self.input_z.setValidator(int_validator)
        self.input_start.setValidator(int_validator)
        self.input_end.setValidator(int_validator)

        self.input_x.setPlaceholderText("Enter X size")
        self.input_z.setPlaceholderText("Enter Z size")
        self.input_start.setPlaceholderText("Enter starting Y")

        self.label_result = QLabel("")
        self.label_height = QLabel("")
        self.label_status = QLabel("")

        btn_calc_sizes = QPushButton("Calculate Sizes")
        btn_calc_height = QPushButton("Calculate Height")
        btn_generate = QPushButton("Generate Schematic")

        btn_calc_sizes.clicked.connect(self.calculate_sizes)
        btn_calc_height.clicked.connect(self.calculate_height)
        btn_generate.clicked.connect(self.generate_schematic)

        layout = QGridLayout()

        layout.addWidget(QLabel("X Size:"), 0, 0)
        layout.addWidget(self.input_x,      0, 1)
        layout.addWidget(QLabel("Z Size:"), 1, 0)
        layout.addWidget(self.input_z,      1, 1)
        layout.addWidget(btn_calc_sizes,    0, 2)
        layout.addWidget(btn_generate,      1, 2)
        layout.addWidget(self.label_result, 2, 0, 1, 3)

        layout.addWidget(QLabel("Start Y:"), 3, 0)
        layout.addWidget(self.input_start,   3, 1)
        layout.addWidget(QLabel("End Y:"),   4, 0)
        layout.addWidget(self.input_end,     4, 1)
        layout.addWidget(btn_calc_height,    3, 2, 2, 1)
        layout.addWidget(self.label_height,  5, 0, 1, 3)

        layout.addWidget(self.label_status, 7, 0, 1 ,3)

        self.setLayout(layout)
    

    def calculate_sizes(self):

        try:
            x = int(self.input_x.text().strip())
            z = int(self.input_z.text().strip())

            sx, sz = QsweMaker.calculate_sizes(x, z)
            dx = sx - x
            dz = sz - z
            xs = str(sx)
            zs = str(sz)

            if dx > 0:
                xs += f" (+{dx})"
        
            if dz > 0:
                zs += f" (+{dz})"

            msg = f"Suggested sizes: {xs}, {zs}"
            self.label_result.setText(msg)

            self.input_x.setText(str(sx))
            self.input_z.setText(str(sz))

        except ValueError:
            self.error("Invalid size inputs")
        

    def calculate_height(self):

        try:

            start = int(self.input_start.text().strip())
            end = int(self.input_end.text().strip())

            y = QsweMaker.calculate_initial_height(start, end)

            self.label_height.setText(f"Right Height: Y={y}")

        except ValueError:
            self.error("Invalid height inputs")
        

    def generate_schematic(self):

        try:

            x = int(self.input_x.text().strip())
            z = int(self.input_z.text().strip())

            rigth_x, rigth_z = QsweMaker.calculate_sizes(x, z)

            if rigth_x != x or rigth_z != z:

                dx = rigth_x - x
                dz = rigth_z - z
                xs = str(rigth_x)
                zs = str(rigth_z)

                if dx > 0:
                    xs += f" (+{dx})"
        
                if dz > 0:
                    zs += f" (+{dz})"

                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Icon.Question)

                msg.setWindowTitle("Adjusted Sizes")
                msg.setText(
                    f"The sizes you entered were adjusted to:\n\n"
                    f"  X: {x} --> {xs}\n"
                    f"  Z: {z} --> {zs}\n\n"
                    "Do you want to continue with these sizes?"
                )

                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                result = msg.exec()

                if result != QMessageBox.StandardButton.Yes:
                    self.label_status.setText("Cancelled.")
                    return

                else:
                    x, z = rigth_x, rigth_z
                

            self.label_status.setText("Generating schematic...")
            self.qswe_maker.generate_schematic(x, z)
            self.label_status.setText(f"Saved: QSWE-V3 {x}x{z}.litematic")

        except Exception as e:
            self.error(f"Error: {e}")


    def error(self, msg):
        QMessageBox.critical(self, "Error", msg)


def main():

    app = QApplication(sys.argv)
    window = QsweGUI()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()