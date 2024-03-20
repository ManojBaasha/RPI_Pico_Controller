import machine
import utime

# Define pin numbers for DC motor and servo
dc_motor_pin = 4  # Replace with the actual GPIO pin connected to the DC motor
servo_pin = 5     # Replace with the actual GPIO pin connected to the servo

# Define pulse width values in microseconds
straight_pw = 1500
left_pw = 1100
right_pw = 1900
brake_pw = 1500
forward_pw = 1650
reverse_pw = 1300

# Initialize PWM for DC motor and servo
dc_motor_pwm = machine.PWM(machine.Pin(dc_motor_pin))
servo_pwm = machine.PWM(machine.Pin(servo_pin))

def set_servo_pulse_width(pwm, pulse_width):
    # Set pulse width for the servo motor
    pwm.duty_u16(int((pulse_width / 20) * 65535))

def set_dc_motor_pulse_width(pwm, pulse_width):
    # Set pulse width for the DC motor
    pwm.duty_u16(int((pulse_width / 20) * 65535))

while True:
    # Step 1: Straight (1.5 ms) and Brake (1.5 ms) for 10 seconds
    set_servo_pulse_width(servo_pwm, straight_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, brake_pw)
    print("Step 1: Straight and Brake")

    # Step 2: Left (1.1 ms) and Forward (1.65 ms) for 2 seconds
    set_servo_pulse_width(servo_pwm, left_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, forward_pw)
    utime.sleep(2)
    print("Step 2: Left and Forward")

    # Step 3: Straight (1.5 ms) and Forward (1.65 ms) for 2 seconds
    set_servo_pulse_width(servo_pwm, straight_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, forward_pw)
    utime.sleep(2)
    print("Step 3: Straight and Forward")

    # Step 4: Right (1.9 ms) and Forward (1.65 ms) for 2 seconds
    set_servo_pulse_width(servo_pwm, right_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, forward_pw)
    utime.sleep(2)
    print("Step 4: Right and Forward")

    # Step 5: Straight (1.5 ms) and Brake (1.5 ms) for 2 seconds
    set_servo_pulse_width(servo_pwm, straight_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, brake_pw)
    utime.sleep(2)
    print("Step 5: Straight and Brake")

    # Step 6: Straight (1.5 ms) and Reverse (1.3 ms) for 1 second
    set_servo_pulse_width(servo_pwm, straight_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, reverse_pw)
    utime.sleep(1)
    print("Step 6: Straight and Reverse")

    # Step 7: Straight (1.5 ms) and Brake (1.5 ms) for 1 second
    set_servo_pulse_width(servo_pwm, straight_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, brake_pw)
    utime.sleep(1)
    print("Step 7: Straight and Brake")

    # Step 8: Straight (1.5 ms) and Reverse (1.3 ms) for 2 seconds
    set_servo_pulse_width(servo_pwm, straight_pw)
    set_dc_motor_pulse_width(dc_motor_pwm, reverse_pw)
    utime.sleep(2)
    print("Step 8: Straight and Reverse")
