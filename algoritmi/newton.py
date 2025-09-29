import math


def optimize(x, platform_x, wind):
    alpha = 0.8
    max_step = 3

    f_prime = 2 * (x - platform_x)
    f_second = 2

    wind_step = -0.3 * wind

    step = -(f_prime / f_second) * alpha + wind_step

    if step > max_step:
        step = max_step
    elif step < -max_step:
        step = -max_step

    return step
