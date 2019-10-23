import pigpio
from src.HardwareInterface import (
    send_servo_commands,
    initialize_pwm,
    PWMParams,
    ServoParams,
    pwm_to_duty_cycle
)
import numpy as np

def getMotorName(i, j):
    motor_type = {
        0: "Abduction",
        1: "Inner", #Top
        2: "Outer" #Bottom
    }
    leg_pos = {
        0: "Front Right",
        1: "Front Left",
        2: "Back Right",
        3: "Back Left"
    }
    final_name = motor_type[i] + " " + leg_pos[j]
    return final_name

def getMotorSetPoint(i, j):
    [[0, 0, 0, 0], [45, 45, 45, 45], [45, 45, 45, 45]]
def getUserInput(request):
    measured_angle = float(input(request))
    return measured_angle

def degreesToRadians(input_array):
    return (np.pi/180.0 * input_array)

def calibrateK(servo_params, pi_board, pwm_params):
    k = np.zeros((3, 4))
    b = np.zeros((3, 4))
    offset1 = 500
    offset2 = -500
    servo_base = 1500
    for j in range(4):
        for i in range(3):
            motor_name = getMotorName(i, j)
            print("Currently calibrating " + motor_name)
            motor_instructions = np.full((3, 4), servo_base)

            # set to 1500 + some offset
            motor_instructions[i][j] = servo_base + offset1
            doty = pwm_to_duty_cycle(motor_instructions[i][j], pwm_params)
            pi_board.set_PWM_dutycycle(pwm_params.pins[i, j], doty)

            #user measures robot angle
            angle1 = getUserInput("Please measure the angle of the joint for " + motor_name)

            #set to 1500 + some other offset
            motor_instructions[i][j] = servo_base + offset2
            dty = pwm_to_duty_cycle(motor_instructions[i, j], pwm_params)
            pi_board.set_PWM_dutycycle(pwm_params.pins[i, j], dty)
            #user measures again
            angle2 = getUserInput("Please measure the angle of the joint for " + motor_name)

            s = servo_params.servo_multipliers[i][j]

            k[i][j] = (offset2 - offset1) / (s * angle1 - s * angle2)
            b[i][j] = (offset1 - s * angle1 * k[i][j]) / k[i][j]

            print("k: " + "[" + str(i) + " " + str(j) + "]", k[i,j])
            print("b: " + "[" + str(i) + " " + str(j) + "]", b[i,j])

    return k, b

def stepInDirection(servo_params, pi_board, pwm_params, kValue, direction=True):
    #step in user-defined direction (True for positive, False for negative)
def stepUntil(servo_params, pi_board, pwm_params, kValue, i_index, j_index):
    #returns the (program_angle) once the real angle matches the pre-defined set point
    foundPosition = False
    zero_neutral = np.zeros(3, 4)
    
    set_names = ["horizontal", "horizontal", "vertical"]
    setPointName = set_names[i_index]

    

    while not foundPosition:
        aboveOrBelow = str(input("is the leg above or below " + setPointName))

def calibrateB(servo_params, pi_board, pwm_params):
    #Found K value of (11.4)
    kValue = getUserInput("Please provide a K value for your servos: ")
    
    beta_values = np.zeros((3, 4))
    
    servo_params.neutral_angle_degrees = zero_neutral
    
    for j in range(4):
        for i in range(3):
            motor_name = getMotorName(i, j)
            print("Currently calibrating " + motor_name + "...")
            set_point = getMotorSetPoint(i, j)

            
            
            



    #(real_angle) = s*(program_angle) - (beta)
    #(beta) = s*(program_angle) - (real_angle)

    


def main():
    """Main program
    """
    pi_board = pigpio.pi()
    pwm_params = PWMParams()
    servo_params = ServoParams()
    initialize_pwm(pi_board, pwm_params)
    new_servo_multiplier, new_neutral_angle_degrees = calibrateK(servo_params, pi_board, pwm_params)

    servo_params.neutral_angle_degrees = new_neutral_angle_degrees
    servo_params.micros_per_rad = new_servo_multiplier[0]

    """
    servo_params.neutral_angle_degrees = np.array(
        [[8, 3, 0, 0], [45, 48, 45, 45], [-50, -38, -45, -45]]
    )

    ref_position = np.pi/180.0 * np.array([[0, 0, 0, 0], [0, 0, 45, 45], [-45,-45, -45, -45]])
    send_servo_commands(pi_board, pwm_params, servo_params, ref_position)
    """



main()

self.servo_multipliers = np.array(
    [[1, 1, 1, 1], [-1, 1, 1, -1], [1, -1, 1, -1]]
)