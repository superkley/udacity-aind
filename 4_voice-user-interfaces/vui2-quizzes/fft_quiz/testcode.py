# import os
# import sys
#
# sys.path.append('/opt/udacity/opencv/lib/python3.4/dist-packages')
# import cv2
# import base64
# import json
# import subprocess
# import numpy as np
# from io import BytesIO
#
# image_start = "BEGIN_IMAGE_f9825uweof8jw9fj4r8"
# image_end = "END_IMAGE_0238jfw08fjsiufhw8frs"
#
# image_name_prefix = "output-"
# image_name_suffix = ".png"
# # here's a comment
# max_images = 5  # limit - no. of times imshow() calls will be entertained
# num_images = 0  # counter for imshow() calls# Import and configure matplotlib, before anything else (!)
# import matplotlib
#
# matplotlib.use('Agg')  # TODO: Configure this (and other rcParams) in ./.matplotlibrc (backend: Agg)
# import matplotlib.pyplot as plt
#
# matplotlib.rcParams['figure.figsize'] = 7.2, 4.05  # 16:9, good text size at default width (512), dpi (96)
#
#
# # matplotlib.rcParams['savefig.dpi'] = 64  # make text/outlines bigger/thicker
#
# def show(block=False, close=True):
#     """Custom version of matplotlib.pyplot.show() to send plot to stdout using savefig()."""
#
#     global max_images, num_images
#
#     # Enforce max image limit
#     if num_images >= max_images:
#         print("WARNING: Exceeded max no. of images ({}), no more will be shown.".format(max_images))
#         return
#     num_images += 1
#
#     # Store figure data as PNG image in memory (as a StringIO buffer)
#     # plt.savefig('output.png')  # [debug]
#     image_data = BytesIO()
#     plt.savefig(image_data, format='png')  # bbox_inches='tight' messes up image size
#
#     try:
#         image_name = "{}{:02d}{}".format(image_name_prefix, num_images, image_name_suffix)
#         # print "show(): Image name: {}".format(image_name)  # [debug]
#         data = {}
#         data['name'] = image_name
#         data['format'] = 'png'
#         data['bytes'] = base64.encodestring(image_data.getvalue()).decode('utf-8')
#         dump = json.dumps(data)
#         sys.stdout.write(image_start + dump + image_end)
#         image_data.close()
#     except Exception as e:
#         print(sys.stderr, "show(): Error showing figure.")
#         raise e  # should be properly handled by caller
#
#     if close:
#         plt.close()
#
#
# def cv2_imshow(image, name='name'):
#     """Display an OpenCV image (2D NumPy array) through the Udacity IDE."""
#
#     global max_images, num_images
#
#     if num_images >= max_images:
#         print("WARNING: Exceeded max no. of imshow() calls ({}), no more images will be shown.".format(max_images))
#         return
#     num_images += 1
#
#     ext = 'png'
#
#     # encodedImage = cv2.cv.EncodeImage('.' + ext, cv2.cv.fromarray(image))  # OpenCV 2.3.x
#     # bytes = encodedImage.tostring()
#
#     retval, bytes = cv2.imencode('.' + ext, image)  # OpenCV 2.4.x
#
#     output_image(name, ext, bytes)
#
#
# def output_image(name, format, bytes):
#     """Display an image file "output-image.png" through the Udacity IDE."""
#
#     global image_start, image_end
#
#     data = {}
#     data['name'] = name
#     data['format'] = format
#     data['bytes'] = base64.encodestring(bytes)
#     # print "<Image: {}>".format(name),  # [debug]
#     print(image_start + json.dumps(data) + image_end)
#
#
# plt.show = show
#
# # start of this quiz
import fft_quiz.function as function
import fft_quiz.utils as utils
import fft_quiz.dutils as dutils
# runs when student click "test"
# *****
import matplotlib.pyplot as plt
import numpy as np
import scipy.fftpack

# internal dev only end
num_samples, spacing, t = utils.get_wave_timing()

# test choose_frequencies()
freqs = function.choose_frequencies()
assert None not in freqs, 'choose_frequencies ERROR: Please replace the "None" values with values from 1 to 50.'
assert len(freqs)==3 and max(freqs)<=50 and min(freqs)>=1, 'choose_frequencies ERROR: Expected three in a range between 1 and 50, but the result was {}.'.format(freqs)
print('Frequencies look good!')

# test add_the_waves
waves = function.add_the_waves(freqs)
assert waves[3] is not None, 'add_the_waves ERROR: Please replace the "None" value with a sum of the waves'
testsum = waves[0] + waves[1] + waves[2]
assert len(waves) == 4 and len(waves[3]) == num_samples and np.allclose(waves[3],testsum), 'add_the_waves ERROR: The values were not as expected.  Add the waves with "+"'
print('Waves are summed correctly!')
plt.Figure = dutils.display_sinusoids(t, *waves)
plt.show()

# test demo_fft
xf, yf = function.demo_fft(waves[-1])
assert yf is not None, 'demo_fft ERROR: Please replace the "None" value with the FFT of the wave.'
testyf = scipy.fftpack.fft(waves[-1])
assert np.allclose(yf, testyf), 'demo_fft ERROR: The values are not as expected.'
print('FFT successful!')
plt.Figure = dutils.display_fft(xf, yf)
plt.show()

# if None not in freqs:
#     if None not in freqs \
#             or len(freqs) == 3 and max(freqs)<=50 and min(freqs)>=1:
#         print('Frequencies look good!')
#         waves = function.add_the_waves(freqs)
#         # test function.add_the_waves
#         if waves[3] is not None:
#             testsum = waves[0] + waves[1] + waves[2]
#             if len(waves) == 4 and len(waves[3]) == num_samples and np.allclose(waves[3],testsum):
#                 print('Waves are summed correctly!')
#                 plt.Figure = dutils.display_sinusoids(t, *waves)
#                 plt.show()
#                 #test function demo_fft
#                 xf, yf = function.demo_fft(waves[-1])
#                 if yf is not None:
#                     testyf = scipy.fftpack.fft(waves[-1])
#                     if np.allclose(yf, testyf):
#                         print('FFT successful!')
#                         plt.Figure = dutils.display_fft(xf, yf)
#                         plt.show()
#                     else:
#                         print('demo_fft ERROR: The values are not as expected.')
#                 else:
#                     print('demo_fft ERROR: Please replace the "None" value with the FFT of the wave.')
#             else:
#                 print('add_the_waves ERROR: The values were not as expected.  Add the waves with "+"')
#         else:
#             print('add_the_waves ERROR: Please replace the "None" value with a sum of the waves')
#     else:
#         print('choose_frequencies ERROR: Expected three in a range between 1 and 50,')
#         print('but the result was {}.'.format(freqs))
# else:
#     print('choose_frequencies ERROR: Please replace the "None" values with values from 1 to 50.')
