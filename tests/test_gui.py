import unittest

from GUI import gui

class TestGUI(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_attributes(self):
        test_gui = gui.GUI(None)
        test_gui.configurator = gui.ConfigImporter('../GUI/gui.cfg')
        test_gui.window.after(10, test_gui.window.destroy)
        test_gui.run()
        test_gui.prepare_search()

    def test_no_configurations(self):
        test_gui = gui.GUI(None)
        test_gui.configurator = gui.ConfigImporter(None)
        test_gui.finish_with_search = True

        test_gui.variables= {'substance':''}
        test_gui.window.after(10, test_gui.prepare_search)
        test_gui.window.after(10, test_gui.window.destroy)
        test_gui.run()





