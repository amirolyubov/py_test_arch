# CONSTANTS
LEFT_EYE = 0
RIGHT_EYE = 1
RIGHT_SHOLDER = 2
RIGHT_HAND = 3
LEFT_HAND = 4
LEFT_LEG = 5
RIGHT_LEG = 6
RESERVED_1 = 7
RESERVED_2 = 8

# UTILS
def get_prev_from_dict(dic, elem): return dic[elem] if elem in dic else get_prev_from_dict(dic, elem - 1)

# MODEL
model = {
    'current_time': 0,
    'scenario_stack': {
        0: [ 78, 102, 212, 16, 279, 81, 339, 277, 303, 359 ],
        1: [ 159, 172, 28, 112, 351, 75, 100, 328, 323, 298 ],
        2: [ 220, 216, 65, 296, 77, 197, 43, 308, 68, 263 ],
        3: [ 251, 43, 191, 36, 154, 211, 51, 233, 77, 158 ],
        4: [ 135, 272, 179, 320, 111, 342, 228, 140, 250, 74 ],
        5: [ 156, 65, 307, 68, 189, 279, 301, 49, 287, 247 ],
        11: [ 331, 113, 140, 159, 238, 219, 108, 227, 179, 24 ],
        12: [ 69, 133, 273, 71, 99, 358, 224, 38, 19, 355 ],
        13: [ 225, 173, 299, 243, 119, 97, 350, 304, 352, 208 ],
        14: [ 65, 232, 93, 52, 318, 314, 157, 154, 338, 141 ],
        15: [ 119, 318, 293, 250, 18, 300, 210, 190, 54, 272 ],
        16: [ 21, 117, 187, 107, 139, 147, 33, 257, 163, 13 ],
        17: [ 183, 54, 261, 231, 302, 358, 278, 259, 46, 134 ],
        18: [ 119, 96, 112, 112, 173, 234, 240, 149, 252, 118 ],
        19: [ 80, 247, 220, 255, 149, 92, 2, 212, 253, 183 ]
    }
}

# CONTROLLERS
def check_servos(sec):
    if sec in model['scenario_stack']:
        setServosInGUI(model['scenario_stack'][sec])


def update_servo_controller(servo_id, value):
    if model['current_time'] in model['scenario_stack']:
        model['scenario_stack'][model['current_time']][servo_id] = value
    else:
        arr = get_prev_from_dict(model['scenario_stack'], model['current_time'])
        arr[servo_id] = value
        model['scenario_stack'][model['current_time']] = arr


# VIEWS
def setServosInGUI(servo):
    # TODO: INSERT VALUE IN INPUT
    pass

# gui update handlers
def update_slider(val):
    model['current_time'] = val
    check_servos(val)

def update_servo_input(servo_id, value):
    update_servo_controller(servo_id, value)

# RUNTIME
update_slider(10) # change slider position to 10
update_servo_input(LEFT_HAND, 45) # change servo_LEFT_HAND input to 45


print(model)
