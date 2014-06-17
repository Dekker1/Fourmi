import unittest

from GUI import gui

class TestGUI(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_attributes(self):
        self.test_gui = gui.GUI(None, '../GUI/gui.cfg.sample')
        self.test_gui.window.after(9, self.test_gui.prepare_search)
        self.test_gui.window.after(11, self.test_gui.window.destroy)
        self.test_gui.run()

        output_type = self.test_gui.configurator.load_output_types().split(',')[0]

        self.assertEqual(self.test_gui.values.get('substance'), '')
        self.assertEqual(self.test_gui.values.get('output_type'), output_type)
        self.assertEqual(self.test_gui.values.get('output_name'), 'results')


    def test_no_configurations(self):
        self.test_gui = gui.GUI(None)
        self.test_gui.configurator = gui.ConfigImporter('')
        self.test_gui.finish_with_search = True
        self.test_gui.window.after(9, self.test_gui.prepare_search)
        self.test_gui.window.after(11, self.test_gui.window.destroy)
        self.test_gui.run()

        self.assertEqual(self.test_gui.values.get('substance'), '')
        self.assertEqual(self.test_gui.values.get('output_type'), 'csv')
        self.assertEqual(self.test_gui.values.get('output_name'), 'results')