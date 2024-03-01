from machine import Pin, PWM
from time import sleep

# Define pulse widths in microseconds
straight = 1500
left = 1100
right = 1900
brake = 1500
forward = 1650
reverse = 1300

# Convert pulse widths to duty cycle values
straight_duty = int(straight / 20000 * 65535)  # 1.5 ms
left_duty = int(left / 20000 * 65535)  # 1.1 ms
right_duty = int(right / 20000 * 65535)  # 1.9 ms
brake_duty = int(brake / 20000 * 65535)  # 1.5 ms
forward_duty = int(forward / 20000 * 65535)  # 1.65 ms
reverse_duty = int(reverse / 20000 * 65535)  # 1.3 ms

# Initialize state and time variables
states = [
    (straight_duty, brake_duty, 10),
    (left_duty, forward_duty, 2),
    (straight_duty, forward_duty, 2),
    (right_duty, forward_duty, 2),
    (straight_duty, brake_duty, 2),
    (straight_duty, reverse_duty, 1),
    (straight_duty, brake_duty, 1),
    (straight_duty, reverse_duty, 2),
]

current_state = 0

pwm = PWM(Pin(5))

pwm.freq(1000)

def set_pwm_state(state):
    pwm.duty_u16(state[0])
    print("moving" , state[0])
    print("sleeping for ", state[2])
    sleep(state[2])
    
    pwm.duty_u16(state[1])
    print("moving" , state[1])
    print("sleeping for ", state[2])
    sleep(state[2])
    

while True:
    for state in states:
        set_pwm_state(state)