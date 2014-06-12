import unittest

from GUI import gui

class TestGUI(unittest.TestCase):
    def setUp(self):
        pass

    def test_empty_attributes(self):
        test_gui = gui.GUI()
        test_gui.run()
        test_gui.prepare_search()

    def test_no_configurations(self):
        import os
        config_name = 'gui.cfg'
        with open(config_name) as config_file:
            file_contents = config_file.read()
        os.remove(config_name)

        test_gui = gui.GUI()
        test_gui.finish_with_search = True
        test_gui.run()


