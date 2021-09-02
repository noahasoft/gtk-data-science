import gi
import pandas as pd
from matplotlib.backends.backend_gtk3agg import FigureCanvasGTK3Agg as FigureCanvas
import matplotlib.pyplot as plt

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Plotter:
    def __init__(self):
        self.column_names = False
        self.drop_nan = False
        self.df = None

        self.builder = Gtk.Builder()
        self.builder.add_from_file("plotter.glade")
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window1")
        self.window.show_all()

    def load_table(self, filename):
        if filename is not None:
            fn = filename.split("/")[-1]
            if self.column_names:
                df = pd.read_csv(filename, sep=",", engine="python")
                header_list = list(df.columns)
                data = df[1:].values.tolist()
            else:
                df = pd.read_csv(filename, sep=",", engine="python", header=None)
                header_list = ["column" + str(x) for x in range(len(df.iloc[0]))]
                df.columns = header_list
                data = df.values.tolist()
            if self.drop_nan:
                df = df.dropna()

            self.df = df

    def on_open_dialog(self, widget):
        dialog = self.builder.get_object("dialog")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            self.load_table(filename)
        elif response == Gtk.ResponseType.CANCEL:
            dialog.close()
        dialog.close()

    def on_close_dialog(self, widget, event):
        return self.builder.get_object("dialog").hide_on_delete()

    def on_column_switch(self, switch, gparam):
        self.column_names = bool(switch.get_active())

    def on_nan_switch(self, switch, gparam):
        self.drop_nan = bool(switch.get_active())

    def on_plot(self, button):
        if self.df is None:
            return
        canvas_window = self.builder.get_object("plot1")
        if canvas_window.get_child():
            canvas_window.show_all()
            return
        fig = plt.figure(dpi=100)
        x = list(self.df.columns)[3]
        y = list(self.df.columns)[5]
        fig.add_subplot(111).scatter(
            self.df[x], self.df[y], color="blue", edgecolor="k"
        )
        plt.xlabel(x)
        plt.ylabel(y)

        canvas = FigureCanvas(fig)
        canvas.set_size_request(800, 600)
        canvas_window.add(canvas)
        canvas_window.show_all()

    def on_plot_close(self, widget, event):
        return self.builder.get_object("plot1").hide_on_delete()

    def on_destroy(self, event):
        Gtk.main_quit()


if __name__ == "__main__":
    Plotter()
    Gtk.main()
