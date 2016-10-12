"""
Cookie Clicker Simulator
"""

# import simpleplot

# # Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)
import math

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._game_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        msg = "At time %f, we have %.1f cookies and CPS is at %.1f.\n" % (self._game_time, self._current_cookies, self._current_cps)
        msg += "Overall, %.1f cookies have been produced so far." % (self._total_cookies)
        return msg

    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._game_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies <= self._current_cookies:
            time_to_wait = 0.0
        else:
            time_to_wait = math.ceil((cookies - self._current_cookies) / self._current_cps)

        return time_to_wait
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0:
            cookies_produced = time * self._current_cps
            self._current_cookies += cookies_produced
            self._total_cookies += cookies_produced
            self._game_time += time
            # print('While waiting, we produced %f cookies.' % cookies_produced)
            # print('We now have %f cookies.' % self.current_cookies)
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if item_name is not None and cost >= 0 and cost <= self._current_cookies:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._game_time, item_name, cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    build = build_info.clone()
    clicker = ClickerState()

    while clicker.get_time() <= duration:
        
        next_item_to_buy = strategy(
            clicker.get_cookies(), 
            clicker.get_cps(),
            clicker.get_history(),
            duration - clicker.get_time(),
            build)

        if next_item_to_buy is None:
            break
        else:
            cost_of_item = build.get_cost(next_item_to_buy)
            time_to_wait = clicker.time_until(cost_of_item)
            if clicker.get_time() + time_to_wait > duration:
                break
            clicker.wait(time_to_wait)
            clicker.buy_item(next_item_to_buy, cost_of_item, build.get_cps(next_item_to_buy))
            build.update_item(next_item_to_buy)

    remaining_time = duration - clicker.get_time()
    # print('Simulation ended with %s seconds to spare.' % remaining_time)
    clicker.wait(remaining_time)
    next_item_to_buy = strategy(
            clicker.get_cookies(), 
            clicker.get_cps(),
            clicker.get_history(),
            0,
            build)

    if next_item_to_buy is not None:
        cost_of_item = build.get_cost(next_item_to_buy)
        add_cps = build.get_cps(next_item_to_buy)
        buy_all_items(next_item_to_buy, cost_of_item, add_cps, clicker)

    return clicker

def buy_all_items(item, cost, add_cps, clicker):
    """
    Buys as many of the specified item as possible, given the amount
    of cookies available.
    """
    available_cookies = clicker.get_cookies()
    items_to_buy = int(math.floor(available_cookies / cost))
    for dummy_cookie in range(items_to_buy):
        clicker.buy_item(item, cost, add_cps)


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    buildable_items = build_info.build_items()
    cheapest_item = None
    cheapest_price = float("inf")
    for item in buildable_items:
        if build_info.get_cost(item) < cheapest_price:
            cheapest_price = build_info.get_cost(item)
            cheapest_item = item

    ending_cookies = cookies + cps * time_left
    if ending_cookies >= cheapest_price:
        return cheapest_item
    else:
        return None

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    buildable_items = build_info.build_items()
    priciest_item = None
    highest_price = 0
    for item in buildable_items:
        item_cost = build_info.get_cost(item)
        time_needed = item_cost / cps
        if cookies >= item_cost or (item_cost >= highest_price and time_needed <= time_left):
            highest_price = item_cost
            priciest_item = item
    
    ending_cookies = cookies + cps * time_left
    if ending_cookies >= highest_price and priciest_item is not None:
        return priciest_item
    else:
        return None

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    buildable_items = build_info.build_items()
    best_item = None
    best_item_price = 0
    small_recoup_time = float("inf")

    for item in buildable_items:
        if item != 'Cursor':
            item_cost = build_info.get_cost(item)
            added_cps = build_info.get_cps(item)
            time_to_recoup_cost = item_cost / added_cps
            if time_to_recoup_cost < small_recoup_time:
                small_recoup_time = time_to_recoup_cost
                best_item = item
                best_item_price = item_cost

    ending_cookies = cookies + cps * time_left
    if ending_cookies > best_item_price:
        return best_item
    else:
        return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
# run()

