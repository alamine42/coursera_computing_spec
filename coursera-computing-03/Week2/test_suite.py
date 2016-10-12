"""
Test suite for format function in "Stopwatch - The game"
"""
import poc_simpletest

def run_suite(game_object, height, width):
    """
    Some informal testing code
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    # test format_function on various inputs
    suite.run_test(game_object.get_grid_height(), height, "Test get_grid_height():")
    suite.run_test(game_object.get_grid_width(), width, "Test get_grid_height():")
    suite.report_results()
