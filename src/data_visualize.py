import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import object_tracking

def data_visualize(data):
    fig = plt.figure()
    ims = []
    for i in range(400):
        ims.append([plt.imshow(data[i])])

    ani = animation.ArtistAnimation(fig, ims, interval=100)
    ani.save('result/data.gif', writer="imagemagick")


if __name__ == "__main__":
    path = './DataForPF'
    data = np.empty((400, 30, 40))
    data = object_tracking.load_data(path, data)
    data_visualize(data)