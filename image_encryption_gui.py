import Tkinter as Tk


class GuiItem():
    def __init__(self, row, col, gui_item, var=None):
        self.row = row
        self.col = col
        self.gui_item = gui_item
        self.var = var

    def get_var_val(self):
        return self.var.get()

    def put_on_grid(self):
        self.gui_item.grid(row=self.row, column=self.col)

    def remove_from_grid(self):
        self.gui_item.grid_remove()

class image_encryption_gui():
    def __init__(self, master):
        self.master = master
        master.title("Image Encryption")

        self.always_on_widgets = {}
        self.active_widgets = {}

        self.create_always_on_buttons()
        self.create_half_squares_buttons()
        self.create_circle_layers_buttons()

        self.load_configuration("config_name")


    def create_always_on_buttons(self):
        var = Tk.StringVar()
        options_list = ["Half Squares", "Circle Layers"]
        self.encryption_type = options_list[0]
        var.set(self.encryption_type)
        type_button = Tk.OptionMenu(self.master, var, *options_list, command=self.on_type_sel)
        self.always_on_widgets["type_button"] = GuiItem(row=0, col=0, gui_item=type_button, var=var)

        for widget in self.always_on_widgets.values():
            widget.put_on_grid()

    def create_half_squares_buttons(self):
        pass

    def create_circle_layers_buttons(self):
        pass

    def load_configuration(self, config_name):
        pass

    def on_type_sel(self, val):
        if val != self.encryption_type:
            print "type changed to {}".format(val)
            self.encryption_type = val

if __name__ == '__main__':
    root = Tk.Tk()
    my_gui = image_encryption_gui(root)
    root.mainloop()

