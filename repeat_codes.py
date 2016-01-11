"""
Author: Billy Weir
Date: 2016-01-11

Noisy communication channel simulation.
Created for final assignment of Quantum Information, Autumn 2015 at The University of Edinburgh.

Dependencies: NumPy (http://www.numpy.org/); PIL (https://python-pillow.github.io/)
"""

from collections import Counter
from PIL import Image
import numpy as np


def encode(n, message):
    """ Repeat each symbol in the input message n times. """
    return "".join([i * n for i in message])


def noise(p, message):
    """ Add noise with probability of error p to the encoded message.
        This is the transmission. """

    # Error is a bernoulli trial with probability of success (error) p.
    # Given a success, 1 is taken from the current bit value and the absolute value is returned.
    m = np.abs(map(int, message) - np.random.binomial(1, p, len(message)))
    return "".join(map(str, m))


def decode(n, message):
    """ Decode the noisy message using majority vote decoder algorithm. """

    # Split the message into blocks of size n.
    m = [message[i:i+n] for i in range(0, len(message), n)]

    # Decode each block using majority vote decoder.
    # The most common symbol in the code must be the transmitted symbol
    s = [Counter(i).most_common(1)[0][0] for i in m]
    return "".join(s)


def sim(m, n, p):
    """ Chain together the channel functions to produce the noisy channel simulation. """
    return decode(n, noise(p, encode(n, m)))


if __name__ == "__main__":

    # Probability of error
    p = 0.1

    # Load the image data in greyscale format and convert data into binary format
    img = Image.open('mona_lisa.png').convert('L').getdata()
    binary = map(lambda x: format(x, '#010b')[2:], img)

    # Loop over values of n, the number of repeats in the code
    for n in range(1, 10, 2):

        # Transmit binary data down the noisy channel
        noisy_data = map(lambda x: sim(x, n, p), binary)

        # Convert the binary back to integer format
        ints = np.array(map(lambda x: int(x, 2), noisy_data)).reshape((100, 100))

        # Convert image data into image and save
        Image.fromarray(np.uint8(ints)).save(str(n)+'.png')
