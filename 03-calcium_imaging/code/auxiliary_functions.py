#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Melisa
Auxiliary functions created to help in the neural analysis course, assignment4 related to calcium imaging analysis.
"""

import os
import caiman as cm
import matplotlib.pyplot as plt
import math
import numpy as np
from caiman.motion_correction import high_pass_filter_space
from caiman.source_extraction.cnmf.cnmf import load_CNMF
from matplotlib.patches import Rectangle
from random import randrange


def plot_FOV(FOV_file=None, ROI_file=None):

    FOV = cm.load(FOV_file)
    ROI = cm.load(ROI_file)

    figure = plt.figure(constrained_layout=True)
    gs = figure.add_gridspec(1, 2)

    figure_ax1 = figure.add_subplot(gs[0, 0])
    figure_ax1.set_title('FOV', fontsize=15)

    figure_ax2 = figure.add_subplot(gs[0, 1])
    figure_ax2.set_title('ROI', fontsize=15)

    figure_ax1.imshow(FOV[0, :, :], cmap='gray')
    [x_, _x, y_, _y] = [100, 500, 200, 600]
    rect = Rectangle((y_, x_), _y - y_, _x - x_, fill=False,
                     color='r', linestyle='-', linewidth=2)
    figure_ax1.add_patch(rect)

    figure_ax2.imshow(ROI[0, :, :], cmap='gray')


    return


def temporal_evolution(file_name=None, output_file_name=None):
    '''
    After decoding this plots the time evolution of some pixel values in the ROI, the histogram if pixel values and
    the ROI with the mark of the position for the randomly selected pixels
    '''

    movie_original = cm.load(file_name)

    figure = plt.figure(constrained_layout=True)
    gs = figure.add_gridspec(5, 6)

    figure_ax1 = figure.add_subplot(gs[0:2, 0:3])
    figure_ax1.set_title('ROI', fontsize=15)
    figure_ax1.set_yticks([])
    figure_ax1.set_xticks([])

    figure_ax2 = figure.add_subplot(gs[2:5, 0:3])
    figure_ax2.set_xlabel('Time [s]', fontsize=15)
    figure_ax2.set_ylabel('Pixel value', fontsize=15)
    figure_ax2.set_title('Temporal Evolution', fontsize=15)
    figure_ax2.set_ylim((300, 1000))

    figure_ax1.imshow(movie_original[0, :, :], cmap='gray')
    color = ['b', 'r', 'g', 'c', 'm']
    for i in range(5):
        x = randrange(movie_original.shape[1]-5)+5
        y = randrange(movie_original.shape[2]-5)+5
        [x_, _x, y_, _y] = [x-5, x+5, y-5, y+5]
        rect = Rectangle((y_, x_), _y - y_, _x - x_, fill=False,
                         color=color[i], linestyle='-', linewidth=2)
        figure_ax1.add_patch(rect)
        figure_ax2.plot(np.arange(
            0, movie_original.shape[0],)/10, movie_original[:, x, y], color=color[i])

        figure_ax_i = figure.add_subplot(gs[i, 4:])
        figure_ax_i.hist(movie_original[:, x, y], 50, color=color[i])
        figure_ax_i.set_xlim((300, 1000))
        figure_ax_i.set_ylabel('#')
        figure_ax_i.set_xlabel('Pixel value')

    figure.set_size_inches([5., 5.])
    figure.savefig(output_file_name)

    return


def get_fig_gSig_filt_vals(file_name=None, gSig_filt_vals=None, output_file=None):
    '''
    Plot original FOV and several versions of spatial filtering for comparison
    :param row: analisis state row for which the filtering is computed
    :param gSig_filt_vals: array containing size of spatial filters that will be applyed
    :return: figure
    '''
    m = cm.load(file_name)
    temp = cm.motion_correction.bin_median(m)
    N = len(gSig_filt_vals)
    fig, axes = plt.subplots(2, int(math.ceil((N + 1) / 2)))
    axes[0, 0].imshow(temp, cmap='gray')
    axes[0, 0].set_title('Unfiltered', fontsize=12)
    axes[0, 0].axis('off')
    for i in range(0, N):
        gSig_filt = gSig_filt_vals[i]
        m_filt = [high_pass_filter_space(
            m_, (gSig_filt, gSig_filt)) for m_ in m]
        temp_filt = cm.motion_correction.bin_median(m_filt)
        axes.flatten()[i + 1].imshow(temp_filt, cmap='gray')
        axes.flatten()[
            i + 1].set_title(f'gSig_filt = {gSig_filt}', fontsize=12)
        axes.flatten()[i + 1].axis('off')
    if N + 1 != axes.size:
        for i in range(N + 1, axes.size):
            axes.flatten()[i].axis('off')
    # Save figure
    fig.suptitle('Spatial filtering', fontsize=15)
    fig.set_size_inches([7., 7.])
    fig.savefig(output_file)

    return


def summary_images(corr_image=None, pnr_image=None):

    figure, axes = plt.subplots(1, 2)
    axes[0].imshow(corr_image, cmap='viridis')
    axes[0].set_title('Correlation image', fontsize=12)
    axes[1].imshow(pnr_image, cmap='viridis')
    axes[1].set_title('PNR image', fontsize=12)
    figure.set_size_inches([7., 7.])

    return
