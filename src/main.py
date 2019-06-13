import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import itertools


def load_data(path, data):
    npy = '/img_data.npy'

    if os.path.exists(path+npy):
        data = np.load(path+npy)
        return data
    else:
        for i in range(400):
            frame = '/txt/img{0:03d}.txt'.format(i+1)
            with open(path+frame) as f:
                file = f.readlines()
                for j, line in enumerate(file):
                    line = list(line)
                    line.remove('\n')
                    # data[i][j] = np.array(list(map(int, line)), dtype='bool')
                    data[i][j] = list(map(int, line))
        np.save(path+npy, data)
        return data


def data_visualize(data):
    fig = plt.figure()
    ims = []
    for i in range(400):
        ims.append([plt.imshow(data[i])])

    ani = animation.ArtistAnimation(fig, ims, interval=100)
    ani.save('test.gif', writer="imagemagick")


class ParticleFilter:
    def __init__(self, time=400, v_size=30, s_size=40, sampling_size=1000):
        self.time = time
        self.v_size = v_size
        self.s_size = s_size
        self.sample_size = sampling_size

        # particle
        self.x = np.vstack((np.random.randint(0, v_size, sampling_size),
                            np.random.randint(0, s_size, sampling_size))).transpose()
        # weight
        w = np.random.randint(1, 10, sampling_size)
        self.w = w/np.sum(w)

    def predict(self):
        self.x = self.x + np.random.normal(loc=0, scale=3, size=(self.sample_size, 2))
        self.x = np.round(self.x)

    def update_weight(self, observe):
        base_p = np.sum(observe)/(self.v_size*self.s_size)
        memory = dict()
        for i in range(self.sample_size):
            v, s = int(self.x[i][0]), int(self.x[i][1])
            if (v, s) in memory.keys():
                p = memory[(v, s)]
            else:
                n = 0
                p = 0
                for mv, ms in itertools.permutations([-2, -1, 0, 1, 2], 2):
                    if 0 <= v+mv < self.v_size and 0 <= s+ms < self.s_size:
                        n += 1
                        if observe[v+mv][s+ms] == 1:
                            p += 1
                p /= n if n != 0 else 1
                memory[(v, s)] = p
            self.w[i] *= p/base_p

    def resampling_x(self):
        print(np.sum(self.w))
        self.w = self.w / np.sum(self.w)

        while min(self.w) < 1/(self.sample_size*1000):
            min_index = np.argmin(self.w)
            max_index = np.argmax(self.w)
            self.x[min_index] = self.x[max_index]
            new_weigt = (self.w[max_index] + self.w[min_index])/2
            self.w[min_index] = new_weigt
            self.w[max_index] = new_weigt

    def make_map(self):
        heatmap = np.zeros((self.v_size, self.s_size))
        n = 0
        for i in range(self.sample_size):
            v, s = int(self.x[i][0]), int(self.x[i][1])
            if 0 <= v < self.v_size and 0 <= s < self.s_size:
                heatmap[v][s] += 1
                n += 1
        heatmap = heatmap/n if n != 0 else np.zeros((self.v_size, self.s_size))
        return heatmap

if __name__ == '__main__':
    path = './../DataForPF'
    data = np.empty((400, 30, 40))
    data = load_data(path, data)
    # print(data)

    fig = plt.figure()
    ims = []
    ax1 = plt.subplot(1,2,1)
    ax2 = plt.subplot(1,2,2)
    ax1.set_title('data')
    ax2.set_title('estimation')

    pf = ParticleFilter(sampling_size=100000)
    for t in range(400):
        print('t =', t)
        pf.resampling_x()
        pf.predict()
        pf.update_weight(data[t])
        heatmap = pf.make_map()
        title = fig.text(0.48, 0.8, 't = {}'.format(t), fontsize='large')
        ims.append([ax1.imshow(data[t]), ax2.imshow(heatmap), title])
        # plt.imshow(heatmap)
        # plt.show()
    print('end')
    ani = animation.ArtistAnimation(fig, ims, interval=100)
    ani.save('result_{}.gif'.format(pf.sample_size), writer="imagemagick")

