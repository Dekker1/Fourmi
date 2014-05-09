from Tkinter import *
import tkMessageBox
from fourmi import search
from sourceloader import SourceLoader


class GUI():
    def __init__(self):
        self.finish_with_search = False
        self.values = {}
        self.window, self.variables = self.generate_window(self.load_common_parameters(), self.load_output_types())

    def load_common_parameters(self):
        return ["Boiling Point", "Density", "Molecular Formula", "More0", "More1", "More2", "More3", "More4"]

    def load_output_types(self):
        return ["json", "csv", "xlsx"]

    def generate_window(self, common_parameters, output_types):
        window = Tk()
        window.wm_title("Fourmi Crawler")

        variables = {}

        variable_substance = StringVar(window)
        frame_substance = Frame(window)
        label_substance = Label(frame_substance, text="Substance: ")
        input_substance = Entry(frame_substance, font=("Helvetica",12), width=25, textvariable=variable_substance)
        variables.update({"substance":variable_substance})
        frame_substance.pack(side=TOP)
        label_substance.pack()
        input_substance.pack()

        frame_all_parameters = Frame(window)

        frame_new_parameters = Frame(frame_all_parameters)
        label_new_parameters = Label(frame_new_parameters, text="Parameters: ")
        input_new_parameters = Text(frame_new_parameters, font=("Helvetica",8), width=25, height=7, padx=5, pady=5)
        variables.update({"new_parameters":input_new_parameters})
        frame_new_parameters.pack(side=LEFT)
        label_new_parameters.pack()
        input_new_parameters.pack()

        frame_common_parameters = Frame(frame_all_parameters)
        label_common_parameters = Label(frame_common_parameters, text="Common Parameters: ")
        input_common_parameters = Listbox(frame_common_parameters, selectmode=MULTIPLE, height=7)
        scrollbar_common_parameters = Scrollbar(frame_common_parameters)
        input_common_parameters.config(yscrollcommand=scrollbar_common_parameters.set)
        scrollbar_common_parameters.config(command=input_common_parameters.yview)
        if common_parameters and len(common_parameters) > 0:
            input_common_parameters.insert(END,*common_parameters)
        variables.update({"common_parameters":input_common_parameters})
        frame_common_parameters.pack(side=RIGHT)
        label_common_parameters.pack(side=TOP)
        input_common_parameters.pack(side=LEFT)
        scrollbar_common_parameters.pack(side=RIGHT, fill=Y)

        frame_all_parameters.pack()

        output_type = StringVar()
        output_type.set(output_types[0] if output_types and len(output_types) != 0 else "json")
        variables.update({"output_type":output_type})
        frame_output_type = Frame(window)
        label_output_type = Label(frame_output_type, text="Output: ")
        if output_types and len(output_types) > 0:
            input_output_type = OptionMenu(frame_output_type, output_type, *output_types)
        else:
            input_output_type = Label(frame_output_type, text="No output types in config file\nSelecting json")
        frame_output_type.pack()
        label_output_type.pack()
        input_output_type.pack()

        frame_last = Frame(window)
        search_button = Button(frame_last, text="Start search", command=self.prepare_search)
        cancel_button = Button(frame_last, text="Cancel", command=window.destroy)
        frame_last.pack(side=BOTTOM)
        search_button.pack(side=LEFT)
        cancel_button.pack(side=RIGHT)

        return window, variables

    def prepare_search(self):
        self.finish_with_search = True

        variables = self.variables
        values = {}

        for name, var in variables.iteritems():
            if var.__class__ is StringVar:
                values.update({name: var.get()})
            elif var.__class__ is Text:
                values.update({name: str(var.get("1.0", END)).strip()})
            elif var.__class__ is Listbox:
                values.update({name: ", ".join([var.get(int(i)) for i in var.curselection()])})
            else:
                print "No known class"

        self.values = values
        self.window.destroy()

    def execute_search(self):
        print self.values
        arguments = {'--exclude': None,
                     '--format': self.values.get('output_type'),
                     '--help': False,
                     '--include': None,
                     '--log': None,
                     '--output': 'result.*format*',
                     '--verbose': False,
                     '--version': False,
                     '<compound>': self.values.get('substance'),
                     'list': False,
                     'search': True}
        source_loader = SourceLoader()
        search(arguments, source_loader)

    def run(self):
        self.window.mainloop()
        if self.finish_with_search:
            self.execute_search()
        else:
            tkMessageBox.showinfo("Notice", "No search was executed!")

GUI().run()