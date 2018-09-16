import EAPPnP
import numpy as np


def gen_stretched_transform(n):
    R = np.random.randn(n, 3, 3).astype(np.float32)
    S = np.exp(np.random.randn(n, 3).astype(np.float32))
    T = np.random.randn(n, 3, 1).astype(np.float32)
    X = np.random.randn(n, 3, 10).astype(np.float32)
    Y = np.zeros_like(X)
    for r, s, t, x, y in zip(R, S, T, X, Y):
        r[...] = EAPPnP.procrutes.np_orthogonal_polar_factor(r)
        y[...] = np.matmul(r*s, x) + t
        y[-1, :] += 10

    Y = Y[:,:-1,:]/Y[:,-1,:]
    X = np.swapaxes(X, -1, -2)
    Y = np.swapaxes(Y, -1, -2)

    return X, Y

def get_func(method):
    if method == 'EAPPnP':
        func = EAPPnP.EAPPnP
        data_func = gen_stretched_transform
        stat_func = lambda x, y, o: (x, y, *o[:-1], \
                np.linalg.norm(np.matmul(o[0]*o[2], x) + o[1] - y)/\
                np.linalg.norm(x))
        print_fmt = 'matrix X:\n{}\nmatrix Y:\n{}\nmatrix R:\n{}\n' \
                   +'matrix T:\n{}\nmatrix S:\n{}\nerror: {}'

    return data_func, func, stat_func, print_fmt


def test_correctness(data_func, func, stat_func, print_fmt):

    datas = data_func(1)
    for data in zip(*datas):
        out = stat_func(*data, func(*data))
        print(print_fmt.format(*out))
    return


def benchmark_accuracy(data_func, func, stat_func):

    datas = data_func(N)
    err_sum = 0
    for data in zip(*datas):
        err_sum += stat_func(*data, func(*data))[-1]

    print('Average error over {} random samples: {}'.format(N, err_sum/N))

    return


def benchmark_speed(data_func, func):

    datas = data_func(N)

    start = timer()
    for data in zip(*datas):
        _ = func(*data)
    end = timer()

    print('Average execution time over {} random samples: {} us'.format(N, (end-start)/N*1e6))

    return


def test_method_correctness(method):
    print('Testing method: {}'.format(method))
    funcs = get_func(method)
    test_correctness(*funcs)
    return


def benchmark_method_accuracy(method):
    print('Benchmarking accuracy: {}'.format(method))
    funcs = get_func(method)
    benchmark_accuracy(*funcs[:-1])
    return


def benchmark_method_speed(method):
    print('Benchmarking speed: {}'.format(method))
    funcs = get_func(method)
    benchmark_speed(*funcs[:-2])
    return



if __name__ == '__main__':
    test_method_correctness('EAPPnP')



