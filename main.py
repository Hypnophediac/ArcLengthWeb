import tkinter as tk
from gui import BendingCalculatorGUI

def main():
    root = tk.Tk()
    app = BendingCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
