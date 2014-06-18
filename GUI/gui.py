from Tkinter import *
import os

from configImporter import *


class GUI():
    def __init__(self, search, config_file='configuration.cfg', sourceloader=None, in_source=True):
        """Boots the window, configuration."""
        if not in_source:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            config_file = current_dir + '../' + config_file
        self.configurator = ConfigImporter(config_file)
        self.sourceloader = sourceloader
        self.finish_with_search = False
        self.values = {}
        self.required_variables = ['substance']
        self.search = search
        self.window, self.variables = self.generate_window(self.load_common_attributes(), self.load_output_types())

    def load_common_attributes(self):
        """Calls the configuration parser for common attributes."""
        return [x.strip() for x in self.configurator.load_common_attributes().split(',')]

    def load_output_types(self):
        """Calls the configuration parser for output types."""
        return [x.strip() for x in self.configurator.load_output_types().split(',')]

    def load_always_attributes(self):
        """Calls the configuration parser for attributes that are always used."""
        return ','.join([x.strip() for x in self.configurator.load_always_attributes().split(',')])

    def generate_window(self, common_attributes, output_types):
        """Creates all widgets and variables in the window."""
        window = Tk()
        window.wm_title("Fourmi Crawler")

        variables = {}

        variable_substance = StringVar(window)
        frame_substance = Frame(window)
        label_substance = Label(frame_substance, text="Substance: ")
        input_substance = Entry(frame_substance, font=("Helvetica", 12), width=25, textvariable=variable_substance)
        variables.update({"substance": variable_substance})
        frame_substance.pack(side=TOP)
        label_substance.pack()
        input_substance.pack()
        input_substance.focus()

        frame_all_attributes = Frame(window)
        frame_selecting_attributes = Frame(frame_all_attributes)
        frame_new_attributes = Frame(frame_selecting_attributes)
        label_new_attributes = Label(frame_new_attributes, text="Parameters: ")
        input_new_attributes = Text(frame_new_attributes, font=("Helvetica", 8), width=25, height=7, padx=5, pady=5)
        variables.update({"new_attributes": input_new_attributes})
        frame_new_attributes.pack(side=LEFT)
        label_new_attributes.pack()
        input_new_attributes.pack()

        frame_common_attributes = Frame(frame_selecting_attributes)
        label_common_attributes = Label(frame_common_attributes, text="Common Parameters: ")
        input_common_attributes = Listbox(frame_common_attributes, selectmode=MULTIPLE, height=7)
        scrollbar_common_attributes = Scrollbar(frame_common_attributes)
        input_common_attributes.config(yscrollcommand=scrollbar_common_attributes.set)
        scrollbar_common_attributes.config(command=input_common_attributes.yview)
        if common_attributes and len(common_attributes) > 0:
            input_common_attributes.insert(END, *common_attributes)
        variables.update({"common_attributes": input_common_attributes})
        frame_common_attributes.pack(side=RIGHT)
        label_common_attributes.pack(side=TOP)
        input_common_attributes.pack(side=LEFT)
        scrollbar_common_attributes.pack(side=RIGHT, fill=Y)
        frame_selecting_attributes.pack()

        frame_last = Frame(window)
        search_button = Button(frame_last, text="Start search", command=self.prepare_search)
        cancel_button = Button(frame_last, text="Cancel", command=window.destroy)
        frame_last.pack(side=BOTTOM)
        search_button.pack(side=LEFT)
        cancel_button.pack(side=RIGHT)

        frame_name = Frame(window)
        frame_output_name = Frame(frame_name)
        output_name = StringVar()
        output_name.set("results")
        variables.update({'output_name': output_name})
        label_output_name = Label(frame_output_name, text="Output name:")
        input_output_name = Entry(frame_output_name, font=("Helvetica", 12), width=25, textvariable=output_name)
        frame_output_name.pack(side=LEFT)
        label_output_name.pack()
        input_output_name.pack()

        if output_types and len(output_types) == 1:
            output_type = StringVar()
            output_type.set(output_types[0])
            variables.update({"output_type": output_type})
        else:
            output_type = StringVar()
            output_type.set(output_types[0] if output_types and len(output_types) != 0 else "csv")
            variables.update({"output_type": output_type})
            frame_output_type = Frame(frame_name)
            label_output_type = Label(frame_output_type, text="Extension: ")
            if output_types and len(output_types) > 0:
                input_output_type = OptionMenu(frame_output_type, output_type, *output_types)
            else:
                input_output_type = Label(frame_output_type, text="No output types in config file\nSelecting csv")
            frame_output_type.pack(side=RIGHT)
            label_output_type.pack()
            input_output_type.pack()
        frame_name.pack(side=BOTTOM)


        frame_checkboxes = Frame(window)
        frame_checkbox_attributes = Frame(frame_checkboxes)
        variable_all_attributes = BooleanVar()
        variable_all_attributes.set(True)
        input_all_attributes = Checkbutton(frame_checkbox_attributes, text="Search ALL parameters",
                                           variable=variable_all_attributes)
        variables.update({"all_attributes": variable_all_attributes})
        frame_checkbox_attributes.pack(side=LEFT)
        input_all_attributes.pack()

        frame_logging = Frame(frame_checkboxes)
        variable_logging = BooleanVar()
        variable_logging.set(False)
        input_logging = Checkbutton(frame_logging, text="Verbose logging", variable=variable_logging)
        variables.update({'logging':variable_logging})
        frame_logging.pack(side=RIGHT)
        frame_checkboxes.pack(side=BOTTOM)
        input_logging.pack()
        frame_all_attributes.pack()

        return window, variables

    def prepare_search(self):
        """Saves the values from the window for later retrieval."""
        variables = self.variables
        values = {}

        values.update({"Always attributes": self.load_always_attributes()})
        for name, var in variables.iteritems():
            if var.__class__ is StringVar:
                values.update({name: var.get()})
            elif var.__class__ is BooleanVar:
                values.update({name: var.get()})
            elif var.__class__ is Text:
                values.update({name: str(var.get("1.0", END)).strip()})
            elif var.__class__ is Listbox:
                values.update({name: ", ".join([var.get(int(i)) for i in var.curselection()])})
            else:
                print "No known class, {}, {}".format(name, var)

        self.values = values
        if all([values.get(i) != '' for i in self.required_variables]):
            self.finish_with_search = True
            self.window.destroy()
        else:
            self.finish_with_search = False
            #tkMessageBox.showinfo('Not all required information was entered!')

    def execute_search(self):
        """Calls the Fourmi crawler with the values from the GUI"""
        if self.values.get('all_attributes'):
            attributes = ".*"
        else:
            attribute_types = ['attributes', 'Common attributes', 'Always attributes']
            attributes = ','.join([str(self.values.get(attribute)) for attribute in attribute_types])

        arguments = {'--attributes': attributes,
                     '--exclude': None,
                     '--format': self.values.get('output_type'),
                     '--help': False,
                     '--include': None,
                     '--log': 'log.txt',
                     '--output': '{}.{}'.format(self.values.get('output_name'), self.values.get('output_type')),
                     '-v': 0 if self.values.get('logging') else 3,
                     '--version': False,
                     '<compound>': self.values.get('substance'),
                     'list': False,
                     'search': True}

        self.search(arguments, self.sourceloader)

    def run(self):
        """Starts the window and the search."""
        self.window.mainloop()
        if self.finish_with_search:
            self.execute_search()