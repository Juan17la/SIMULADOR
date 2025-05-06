import tkinter as tk
from missile_simulation import SimuladorMisiles

def main():
    root = tk.Tk()
    app = SimuladorMisiles(root)
    root.mainloop()

if __name__ == "__main__":
    main()
    

