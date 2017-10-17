# Face Generation DCGAN
Using a Deep Convolutional Generative Adversarial Network (DCGAN) to generates new images of faces. The dataset that's used is the [CelebFaces Atrribute Dataset (CelebA)](http://mmlab.ie.cuhk.edu.hk/projects/CelebA.html), which contains over 200,000 celebrity faces with annotations.

This is Project 5 of Udacity's Deep Learning Nanodegree Foundation Program. The aim of the project is to go through the process of building a Generative Adversarial Network (GAN) in TensorFlow by creating the generator and discriminator architectures, as well as their loss and optimization models so they can compete against each other (an consequently improve each other).

### Files

[Jupyter Notebook](https://github.com/nehal96/Face-Generation-DCGAN/blob/master/dlnd_face_generation.ipynb)

### Hyperparameters

Hyperparameter          | Number |
----------------------- | ------ |
Epochs                  | 1      |
Batch size              | 64     |
Learning rate           | 0.0002 |
Z dimension             | 100    |
Alpha                   | 0.1    |
Beta 1                  | 0.5    |
