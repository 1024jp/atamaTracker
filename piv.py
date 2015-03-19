"""piv
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


def find_flow(img1, img2, ii_all, jj_all,
              kernel_size=(25, 25), di_range=(-5, 5), dj_range=(-5, 5)):
    shape_org = ii_all.shape
    ii_all = ii_all.reshape(ii_all.size)
    jj_all = jj_all.reshape(jj_all.size)
    di_all = numpy.zeros(ii_all.size)
    dj_all = numpy.zeros(ii_all.size)
    cc_max_all = numpy.zeros(ii_all.size)

    for i_point in range(ii_all.size):
        ii = ii_all[i_point]
        jj = jj_all[i_point]
        li_half = (kernel_size[0] - 1) / 2
        lj_half = (kernel_size[1] - 1) / 2
        kernel = img1[ii - li_half:ii + li_half + 1,
                      jj - lj_half:jj + lj_half + 1]
        img = img2[ii + di_range[0] - li_half:ii + di_range[1] + li_half + 1,
                   jj + dj_range[0] - lj_half:jj + dj_range[1] + lj_half + 1]
        cc = xcorr_norm(img, kernel)
        cc_shape = cc.shape
        (di, dj) = numpy.unravel_index(numpy.argmax(cc), img.shape)

        if (di == 0 or di == cc_shape[0] - 1 or dj == 0 or
                dj == cc_shape[1] - 1 or numpy.max(cc) < 0.5):
            di_all[i_point] = 0
            dj_all[i_point] = 0
            # cc_max_all[i_point] = 0
        else:
            # subpixel analysis
            cc_C = cc[di, dj]
            cc_N = cc[di - 1, dj]
            cc_S = cc[di + 1, dj]
            cc_W = cc[di, dj - 1]
            cc_E = cc[di, dj + 1]
            di = (di - 0.5 * (numpy.log(cc_S) - numpy.log(cc_N)) /
                  (numpy.log(cc_S) - 2 * numpy.log(cc_C) + numpy.log(cc_N)))
            dj = (dj - 0.5 * (numpy.log(cc_E) - numpy.log(cc_W)) /
                  (numpy.log(cc_E) - 2 * numpy.log(cc_C) + numpy.log(cc_W)))
            di = di - li_half + di_range[0]
            dj = dj - lj_half + dj_range[0]
            di_all[i_point] = di
            dj_all[i_point] = dj
            cc_max_all[i_point] = cc.max()

    di_all.reshape(shape_org)
    dj_all.reshape(shape_org)
    cc_max_all.reshape(shape_org)

    return di_all, dj_all, cc_max_all
