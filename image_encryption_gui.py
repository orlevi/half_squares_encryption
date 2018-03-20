import Tkinter as Tk

class gui_item():
    def init(self, row, col, gui_item, var=None):
        self.row = row
        self.col = col
        self.gui_item = gui_item
        self.var = var

    def get_var_val(self):
        return self.var.get()

    def put_on_frame(self):
        self.gui_item.grid(self.row, self.col)

    def remove_from_frame(self):
        self.gui_item.grid_remove()

class image_encryption_gui():
    def __init__(self, master):
        self.master = master
        master.title("Image Encryption")

        self.create_always_on_buttons()
        self.create_half_squares_buttons()
        self.create_circle_layers_buttons()

        self.load_configuration("config_name")

        self.close_button = Tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def create_always_on_buttons(self):
        pass

    def create_half_squares_buttons(self):
        pass

    def create_circle_layers_buttons(self):
        pass

    def load_configuration(self, config_name):
        pass

if __name__ == '__main__':
    root = Tk.Tk()
    my_gui = image_encryption_gui(root)
    root.mainloop()

