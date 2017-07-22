"""@author Kushal Jaligama"""


class PID:
    p_gain = 0.0
    i_gain = 0.0
    d_gain = 0.0

    setpoint = 0.0
    process_var = 0.0

    i_accum = 0.0
    # TODO: i_accum_cutoff = DETERMINE THIS LATER

    error = 0.0
    time_step = 0.1  # This represents the interval in seconds at which PID runs

    def compute():
        error = setpoint - process_var

        p_term = p_gain * error
        i_accum += error * time_step
        i_term = i_accum * i_gain
        d_term = error / time_step

        return (p_term + i_term + d_term)