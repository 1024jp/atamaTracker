"""piv - Particle Image Velocimetry
"""

import warnings

import numpy
import scipy
import scipy.signal
import scipy.ndimage


warnings.simplefilter('ignore', numpy.ComplexWarning)


def xcorr_norm(img, kernel):
    """normalize kernel"""
    kernel = kernel - scipy.mean(kernel)
    kernel = kernel / scipy.sqrt(scipy.sum(kernel ** 2))
    kernel_sum = scipy.sum(kernel)
    filter_kernel = numpy.ones(kernel.shape) / kernel.size
    filter_sum = numpy.ones(kernel.shape)
    img_mean = scipy.signal.convolve2d(img, filter_kernel, 'same')
    img_sq = img ** 2
    img_sq_sum = scipy.signal.convolve2d(img_sq, filter_sum, 'same')
    cc = scipy.ndimage.correlate(img, kernel)
    cc_norm = ((cc - img_mean * kernel_sum) /
               scipy.sqrt(img_sq_sum - kernel.size * img_mean ** 2))

    return cc_norm


def find_flow(image1, image2, i_all, j_all,
              kernel_size=(25, 25), di_range=(-5, 5), dj_range=(-5, 5)):
    di_all = numpy.zeros(i_all.size)
    dj_all = numpy.zeros(i_all.size)
    cc_max_all = numpy.zeros(i_all.size)

    for idx, (i, j) in enumerate(zip(i_all, j_all)):
        di, dj, cc_max = find_point(image1, image2, i, j, kernel_size,
                                    di_range, dj_range)
        di_all[idx] = di
        dj_all[idx] = dj
        cc_max_all[idx] = cc_max

    return di_all, dj_all, cc_max_all


def find_point(image1, image2, i, j, kernel_size, di_range, dj_range):
    li_half = (kernel_size[0] - 1) / 2
    lj_half = (kernel_size[1] - 1) / 2

    kernel = image1[i - li_half:i + li_half + 1,
                    j - lj_half:j + lj_half + 1]
    image = image2[i - li_half + di_range[0]:i + li_half + 1 + di_range[1],
                   j - lj_half + dj_range[0]:j + lj_half + 1 + dj_range[1]]
    cc = xcorr_norm(image, kernel)
    cc_shape = cc.shape
    di, dj = numpy.unravel_index(numpy.argmax(cc), image.shape)

    if (di == 0 or di == cc_shape[0] - 1 or dj == 0 or
            dj == cc_shape[1] - 1 or numpy.max(cc) < 0.5):
        return 0, 0, 0

    # subpixel analysis
    cc_C = cc[di, dj]
    cc_N = cc[di - 1, dj]
    cc_S = cc[di + 1, dj]
    cc_W = cc[di, dj - 1]
    cc_E = cc[di, dj + 1]
    di -= (0.5 * (numpy.log(cc_S) - numpy.log(cc_N)) /
           (numpy.log(cc_S) - 2 * numpy.log(cc_C) + numpy.log(cc_N)))
    dj -= (0.5 * (numpy.log(cc_E) - numpy.log(cc_W)) /
           (numpy.log(cc_E) - 2 * numpy.log(cc_C) + numpy.log(cc_W)))
    di += di_range[0] - li_half
    dj += dj_range[0] - lj_half

    return di, dj, cc.max()
