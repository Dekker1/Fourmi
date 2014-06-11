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
        test_gui = gui.GUI()
        #test_gui.
        test_gui.run()
        test_gui.prepare_search()

