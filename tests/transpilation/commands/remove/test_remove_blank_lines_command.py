from dragon.transpilation.commands.remove.remove_blank_lines_command import RemoveBlankLinesCommand
from helpers import test_data
import unittest

class TestRemoveBlankLinesCommand(unittest.TestCase):
    def test_execute_removes_blank_lines(self):
        output = RemoveBlankLinesCommand.execute(test_data.MAIN_HX_PYTHON)
        for line in output.splitlines():
            self.assertGreater(len(line.strip()), 0)