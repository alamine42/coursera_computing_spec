"""
Test suite for format function in "Stopwatch - The game"
"""
from __future__ import print_function

import poc_simpletest

def run_suite(clicker):
    """
    Some informal testing code
    """  
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    # test format_function on various inputs
    suite.run_test(clicker.__str__(), 
    	"At time 0.000000, we have 0.0 cookies and CPS is at 1.0.\nOverall, 0.0 cookies have been produced so far.", 
    	"Initial clicker state is off.")
    suite.run_test(clicker.get_cookies(), 0, "Houston, we have a problem in get_cookies()")
    suite.run_test(clicker.get_cps(), 1.0, "Houston, we have a problem in get_cps()")
    suite.run_test(clicker.get_time(), 0.0, "Houston, we have a problem in get_time()")
    suite.run_test(clicker.get_history(), [(0.0, None, 0.0, 0.0)], "Houston, we have a problem in get_history()")
    suite.run_test(clicker.time_until(10), 10.0, "Houston, we have a problem in time_until()")

    clicker.wait(-5)
    suite.run_test(clicker.get_cookies(), 0, "Houston, we have a problem in get_cookies() after waiting.")
    clicker.wait(17)
    suite.run_test(clicker.get_cookies(), 17, "Houston, we have a problem in get_cookies() after waiting.")

    clicker.buy_item('Temple', 100.0, 1.5)
    
    suite.run_test(clicker.get_cookies(), 17, "Houston, we have a problem in buy_item().")
    clicker.buy_item('Grandma', 5.0, 0.5)
    suite.run_test(clicker.get_cookies(), 12, "Houston, we have a problem in buy_item().")
    suite.run_test(clicker.get_cps(), 1.5, "Houston, we have a problem in buy_item().")
    suite.run_test(clicker.get_history(), [(0.0, None, 0.0, 0.0), (17.0, 'Grandma', 5.0, 17.0)], 
	 	"Houston, we have a problem with history after buying." )

    clicker.wait(8)
    suite.run_test(clicker.get_cookies(), 24, "Houston, we have a problem in buy_item().")

    suite.report_results()
