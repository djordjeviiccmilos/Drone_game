import math

def optimize(x, platform_x, wind):
    learning_rate = 0.006
    max_step = 1
    alpha = 0.2

    grad = 2 * (x - platform_x)
    wind_step = -0.5 * wind

    step = -learning_rate * grad + alpha * wind_step

    if step > max_step:
        step = max_step
    elif step < -max_step:
        step = -max_step

    return step