from __future__ import division

import os
import random as rnd

import numpy as np
import scipy as sp
import skimage as ski
from matplotlib import pylab as plt
from pylab import *
from skimage import exposure
from skimage import img_as_float
from skimage import io, filters
from skimage import measure
from skimage import restoration
from skimage.color import rgb2gray
from skimage.color import rgb2hed
from skimage.morphology import remove_small_objects


def prepare_img(img):
    ihc_hed = rgb2hed(img)
    h = exposure.rescale_intensity(ihc_hed[:, :, 0], out_range=(0, 1))
    d = exposure.rescale_intensity(ihc_hed[:, :, 2], out_range=(0, 1))
    zdh = np.dstack((np.zeros_like(h), d, h))
    tmp = rgb2gray(zdh)
    p0_5, p99_5 = np.percentile(tmp, (0.5, 99.5))
    tmp = exposure.rescale_intensity(tmp, (p0_5, p99_5))
    tmp = filters.prewitt(tmp)
    tmp = restoration.denoise_nl_means(tmp, h=0.95, fast_mode=True, patch_size=3, patch_distance=7, multichannel=False)
    return tmp


def thresh_img(img):
    tmp = prepare_img(img)
    binary = (tmp > filters.threshold_minimum(tmp))
    return binary


def outline_img(img):
    tmp = thresh_img(img)
    tmp = filters.prewitt(tmp)
    tmp_outline = filters.sobel(tmp)
    tmp_outline = sp.ndimage.binary_fill_holes(tmp_outline)
    tmp_outline = remove_small_objects(tmp_outline, 10 * 10)
    return tmp_outline


def color_outlines(img, ax):
    outline_shapes = outline_img(img)
    contours = measure.find_contours(outline_shapes, 0.8)
    outlines, count = sp.ndimage.label(outline_shapes)
    outlines = measure.regionprops(outlines)
    for outline in outlines:
        centroid_x, centroid_y = outline.centroid
        circle = ski.draw.circle(int(centroid_x), int(centroid_y), 3.5)
        img[circle[0], circle[1]] = 1.0

    ax.imshow(img, cmap=plt.cm.gray)

    colors = ['g', 'r', 'c', 'm', 'y']
    for contour in contours:
        ax.plot(contour[:, 1], contour[:, 0], linewidth=7, color=rnd.choice(colors))

    ax.set_xticks([])
    ax.set_yticks([])


def find_circles_pos(game):
    # TODO wyszukiwanie kółek na planszy i zwracanie macierzy pozycji kółek na planszy
    return False    # tymczasowe


def find_crosses_pos(game):
    # TODO wyszukiwanie krzyżyków w grze i zwracanie macierzy pozycji krzyżyków na planszy
    return False    # tymczasowe


def print_game(circles, crosses):
    # TODO printowanie planszy gry
    return False    # tymczasowe


def find_game_state(game):
    # circles = find_circles_pos(game)
    # crosses = find_crosses_pos(game)
    # print_game_state(circles, crosses)
    return False    # tymczasowe


def find_games_areas(img):
    # TODO wyszukiwanie obszarów dla planszy poszczególnych gier na obrazie i zwracanie listy list koordynatów
    return False    # tymczasowe


def check_games(img):
    # games_areas = find_games_areas(img)
    # for area in games_areas:
    #     find_game_state(img[area[0]:area[2], area[1]:area[3]])
    # TODO powyższa funkcaj prituje zaznaczone wykryte figury na zdjęciach lub osobna funkcja do tego (dodatkowe)
    return False    # tymczasowe


def check_imgs_in_dir(dir):
    dir_listed = os.listdir(dir)    # lista plików w folderze
    rownum = 0
    n = 0

    fig, ax = plt.subplots(nrows=9, ncols=2, figsize=(50, 200), dpi=100)
    for img_name in dir_listed:
        img = io.imread(os.path.join(dir, img_name))
        ax[rownum, n%2].imshow(img)  # tymczasowa komenda
        if (n + 1) % 2 == 0:
            rownum += 1
        n += 1
        # check_games(img)
    fig.savefig('test.pdf')


check_imgs_in_dir('zdjęcia\\łatwe\\')
