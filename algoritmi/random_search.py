import random

def optimize(x, platform_x, wind):
    max_step = 2
    random_step = random.uniform(-max_step, max_step)
    direction_step = 0.05 * (platform_x - x)
    wind_step = -0.3 * wind

    step = random_step + direction_step + wind_step

    if step > max_step:
        step = max_step
    elif step < -max_step:
        step = -max_step

    return step