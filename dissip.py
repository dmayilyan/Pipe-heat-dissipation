#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math as m
import matplotlib.pyplot as plt
import time

SB_const = 5.67040E-8


def get_C_ij(pipe_length, radius, deg_emission):
    A_1 = pipe_length * 2 * m.pi * radius[0]
    print(A_1)
    A_2 = pipe_length * 2 * m.pi * radius[1]
    print(A_2)
    C_ij = SB_const / (1 / deg_emission[0] +
                       A_1 / A_2 * (1 / deg_emission[1] - 1))
    return C_ij

# def tube_thermal_resistance(r_in, r_out, therm_cond_coef, length):
#     ''' Calculating thermal resistance for given layer '''
#     R = m.log(r_out - r_in) / (therm_cond_coef * 2 * m.pi * length)
#     return R


def heat_flow(length, temperature, therm_cond_coef, thickness):
    denom = 0
    nom = 2 * m.pi * length * (temperature[0] - temperature[-1])
    for i in range(len(thickness) - 1):
        denom += (1 / therm_cond_coef[i] *
                  m.log(sum(thickness[:i + 2]) /
                        sum(thickness[:i + 1])))

    return nom / denom


def gen_steps(thickness):
    ''' Get fine steps for detail propagation '''
    thickness_fine = []
    for i in range(len(thickness)):
        if i == 0:
            continue
        temp = []
        for ii in range(int(sum(thickness[:i]) * 1000),
                        int(sum(thickness[:i + 1]) * 1000 + 1)):
            temp.append(ii / 1000)
        thickness_fine.append(temp)
    thickness = thickness_fine
    return thickness


def get_temperature(length, flow, T, therm_cond_coef, thickness):
    '''  '''
    thickness_fine = gen_steps(thickness)
    T_list = []
    layer_temp = T
    for l in range(len(thickness_fine)):
        for r in range(len(thickness_fine[l])):
            layer_temp = T - flow / (2 * m.pi * length * therm_cond_coef[l]) * m.log(thickness_fine[l][r] / thickness_fine[l][0])
            T_list.append(layer_temp)

        T = layer_temp

    return [thickness_fine, T_list]


def main():

    pipe_length = 0.01

    # Part of radiation
    # Assuming we have a pipe
    radius = [0.02, 0.038]
    deg_emission = [0.79, 0.79]

    print(get_C_ij(pipe_length, radius, deg_emission))

    # Part of heat transfer
    temperature = [2500, 35]
    therm_cond_coef = [5, 0.7, 0.5, 0.2]
    thickness = [0.02, 0.09, 0.045, 0.1, 0.2]

    flow = heat_flow(pipe_length, temperature, therm_cond_coef, thickness)
    T_plot = get_temperature(pipe_length,
                             flow,
                             temperature[0],
                             therm_cond_coef,
                             thickness)
    T_x = [y for x in T_plot[0] for y in x]
    plt.plot(T_x, T_plot[1], '+')
    # plt.ion()
    plt.show()
    print(SB_const)

    # time.sleep(5)
    # plt.close()


if __name__ == '__main__':
    main()
