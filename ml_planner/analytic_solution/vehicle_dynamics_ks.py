__author__ = "Marc Kaufeld"
__copyright__ = "TUM Professorship Autonomous Vehicle Systems"
__version__ = "1.0"
__maintainer__ = "Marc Kaufeld"
__email__ = "marc.kaufeld@tum.de"
__status__ = "Beta"

import math
import numpy as np
from .acceleration_constraints import acceleration_constraints
from .steering_constraints import steering_constraints


def vehicle_dynamics_ks(x, u_init, p):
    """
    vehicleDynamics_ks - kinematic single-track vehicle dynamics
    reference point: rear axle

    Syntax:
        f = vehicleDynamics_ks(x,u,p)

    Inputs:
        :param x: vehicle state vector
        :param u_init: vehicle input vector
        :param p: vehicle parameter vector

    Outputs:
        :return f: right-hand side of differential equations

    Author: Matthias Althoff
    Written: 12-January-2017
    Last update: 16-December-2017
    Last revision: ---
    """
    # create equivalent kinematic single-track parameters
    length = p[0][0] + p[0][1]

    # states
    # x1 = x-position in a global coordinate system
    # x2 = y-position in a global coordinate system
    # x3 = steering angle of front wheels
    # x4 = velocity in x-direction
    # x5 = yaw angle

    # inputs
    # u1 = steering angle velocity of front wheels
    # u2 = longitudinal acceleration

    # consider steering constraints
    u = list()
    u.append(steering_constraints(x[2], u_init[0], p[1]))  # different name u_init/u due to side effects of u
    # consider acceleration constraints
    u.append(acceleration_constraints(x[3], u_init[1], p[2]))  # different name u_init/u due to side effects of u

    # system dynamics
    f = [x[3] * math.cos(x[4]),
         x[3] * math.sin(x[4]),
         u[0],
         u[1],
         x[3] / length * math.tan(x[2])]

    return f


def der_vehicle_dynamics_ks(x, u_init, p):
    """Jacobian of kinematic single-track vehicle dynamics"""
    length = p[0][0] + p[0][1]
    eps = np.sqrt(np.finfo(float).eps)
    # derivative of system dynamics
    df = [[0, 0, 0, math.cos(x[4]), -x[3] * math.sin(x[4]), 0, 0],
          [0, 0, 0, math.sin(x[4]), x[3] * math.cos(x[4]), 0, 0],
          [0, 0, 0, 0, 0, 1, 0],
          [0, 0, 0, 0, 0, 0, 1],
          [0, 0, x[3] / length * 1 / (math.cos(x[2])**2+eps), 1/length * math.tan(x[2]), 0, 0, 0]]
    return np.array(df)
