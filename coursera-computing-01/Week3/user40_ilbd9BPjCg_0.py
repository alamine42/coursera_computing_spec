# template for "Stopwatch: The Game"
import simplegui

# define global variables
tens_counter = 0
nailed_it = 0
stopped_it = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    minutes = t / 600
    minutes_remainder = t % 600
    seconds = minutes_remainder / 10
    seconds_remainder = minutes_remainder % 10
    tenths_of_seconds = seconds_remainder % 10
        
    return '%s:%02d.%s' % (minutes, seconds, tenths_of_seconds)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    timer.start()

def stop_timer():

    global nailed_it, stopped_it
    
    if timer.is_running():
        timer.stop()
        stopped_it += 1
        if tens_counter % 10 == 0:
            nailed_it += 1
    
def reset_timer():
    global tens_counter, nailed_it, stopped_it
    timer.stop()
    tens_counter = 0
    nailed_it = 0
    stopped_it = 0

# define event handler for timer with 0.1 sec interval
def increment_timer():
    global tens_counter
    tens_counter += 1

# define draw handler
def draw_handler(canvas):
    canvas.draw_text(format(tens_counter), [120,150], 32, 'Orange')
    canvas.draw_text(str(nailed_it) + '/' + str(stopped_it), [250,20], 24, 'Green')
    
# create frame
frame = simplegui.create_frame('Stopwatch: The Game', 300, 300)

# register event handlers
timer = simplegui.create_timer(100, increment_timer)
start_button = frame.add_button('Start', start_timer, 50)
stop_button = frame.add_button('Stop', stop_timer, 50)
reset_button = frame.add_button('Reset', reset_timer, 50)
frame.set_draw_handler(draw_handler)

# start frame
frame.start()

# Please remember to review the grading rubric

