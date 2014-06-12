from fourmi import search
from GUI import gui
from utils.sourceloader import SourceLoader


gui_window = gui.GUI(search, sourceloader=SourceLoader())
gui_window.run()
