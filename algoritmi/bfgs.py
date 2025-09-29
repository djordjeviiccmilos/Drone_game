import math

H = 1.0
prev_x = None
prev_gradient = None

def grad(x, platform_x):
    return 2 * (x - platform_x)

def optimize(x, platform_x, wind, max_step=1.5):
    global prev_x, prev_gradient, H

    gradient = grad(x, platform_x)
    wind_step = -0.3 * wind

    if prev_x is None:
        step = -0.1 * gradient + wind_step
        prev_gradient = gradient
        prev_x = x

        return max(-max_step, min(step, max_step))

    s = x - prev_x
    y = gradient - prev_gradient

    if y * s != 0:
        ro = 1.0 / (y * s)
        H = (1 - ro * y * s) * H * (1 - ro * y * s) + ro * s * s

    step = -H * gradient + wind_step

    if step > max_step:
        step = max_step
    elif step < -max_step:
        step = -max_step

    prev_x = x
    prev_gradient = gradient

    return step
