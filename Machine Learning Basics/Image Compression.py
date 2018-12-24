from numpy import diag, zeros
from numpy.linalg import svd, norm , matrix_rank
from matplotlib.pyplot import *
import scipy.misc as miscscipy


image = miscscipy.ascent()
U, s, V = np.linalg.svd(image)
rank = np.count_nonzero(s)
image_row = image.shape[0]
image_col = image.shape[1]



# zero all but the k largest singular values.
def zero_singular_values(k):
    for i in range(k,512):
        s[i]= np.float64(0)
    S = np.diag(s)
    return S

# reconstruct the image with new compressed Sigma
def reconstruct_the_image(S):
    new_image = np.dot(np.dot(U,S),V)
    return new_image

# calculate the compression ratio with given k
def calculate_the_compression_ratio(k,S):
    none_zero = np.count_nonzero(S)
    ratio = ((none_zero*image_row + none_zero*image_col + none_zero))\
                /(rank*image_row + rank*image_col + rank)
    return ratio


def forbenius_distance(image,new_image):
    sub = np.subtract(image,new_image)
    dis = norm(sub,ord=None)
    return dis

def compression(k):
    S = zero_singular_values(k)
    new_image = reconstruct_the_image(S)
    ratio = calculate_the_compression_ratio(k,S)
    dis = forbenius_distance(image,new_image)
    return ratio,dis,new_image

def plot_forbenius():
    plot(range(511,0,-1),[compression(k)[1] for k in range(511,0,-1)])
    axis([0,512,0,norm(image,ord=None)])
    xlabel('K')
    ylabel('Distance')
    title('Forbenius Distance')
    show()

def plot_compression_ratios():
    plot(range(511,0,-1),[compression(k)[0] for k in range(511,0,-1)])
    axis([0,512,0,1])
    xlabel('K')
    ylabel('Ratio')
    title('Compression Ratio')
    show()

def plot_5_distinguished_images():
    for ratio,dis,new_image in [compression(k) for k in [256,128,64,32,16]]:
        imshow(new_image)
        title('Forbenius Distance: ' + str(dis) + ', Compression Ratio: ' + str(ratio))
        show()



plot_compression_ratios()
