# -*- coding: utf-8 -*-
"""U_Netplusplus.py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1C24XMKiJozp_c3swnkRIFbU_o1a1D9D2
"""

import tensorflow as tf
from keras.layers import Conv2D, UpSampling2D
from keras.layers import concatenate
from keras.models import Model

from ConvBlock2D import conv_block_2D

def create_unetpp(img_height, img_width, input_chanels, out_classes, starting_filters):
    input_layer = tf.keras.layers.Input((img_height, img_width, input_chanels))

    print('U-Net++ 가동')

    # Encoder

    x0_0 = conv_block_2D(input_layer, starting_filters, 'double_convolution')
    px0_0 = MaxPooling2D(pool_size=2)(x0_0)

    x1_0 = conv_block_2D(px0_0, starting_filters * 2, 'double_convolution')
    px1_0 = MaxPooling2D(pool_size=2)(x1_0)

    x2_0 = conv_block_2D(px1_0, starting_filters * 4, 'double_convolution')
    px2_0 = MaxPooling2D(pool_size=2)(x2_0)

    x3_0 = conv_block_2D(px2_0, starting_filters * 8, 'double_convolution')
    px3_0 = MaxPooling2D(pool_size=2)(x3_0)


    # Skip conn
    ux1_0 = UpSampling2D(2)(x1_0)
    cx0_1 = concatenate([x0_0, ux1_0], axis=-1)
    x0_1 = conv_block_2D(cx0_1, starting_filters, 'double_convolution')

    ux2_0 = UpSampling2D(2)(x2_0)
    cx1_1 = concatenate([x1_0, ux2_0], axis=-1)
    x1_1 = conv_block_2D(cx1_1, starting_filters * 2, 'double_convolution')

    ux3_0 = UpSampling2D(2)(x3_0)
    cx2_1 = concatenate([x2_0, ux3_0], axis=-1)
    x2_1 = conv_block_2D(cx2_1, starting_filters * 4, 'double_convolution')

    ux1_1 = UpSampling2D(2)(x1_1)
    cx0_2 = concatenate([x0_0, x0_1, ux1_1], axis=-1)
    x0_2 = conv_block_2D(cx0_2, starting_filters, 'double_convolution')

    ux2_1 = UpSampling2D(2)(x2_1)
    cx1_2 = concatenate([x1_0, x1_1, ux2_1], axis=-1)
    x1_2 = conv_block_2D(cx0_2, starting_filters * 2, 'double_convolution')

    ux1_2 = UpSampling2D(2)(x1_2)
    cx0_3 = concatenate([x0_0, x0_1, x0_2, ux1_2], axis=-1)
    x0_3 = econv_block_2D(cx0_3, starting_filters, 'double_convolution')


    x4_0 = econv_block_2D(px3_0, starting_filters * 16, 'double_convolution')

    # Decoder
    ux4_0 = UpSampling2D(2)(x4_0)
    cx3_1 = concatenate([x3_0, ux4_0], axis=-1)
    x3_1 = econv_block_2D(cx3_1, starting_filters * 8, 'double_convolution')

    ux3_1 = UpSampling2D(2)(x3_1)
    cx2_2 = concatenate([x2_0, x2_1, ux3_1], axis=-1)
    x2_2 = econv_block_2D(cx2_2, starting_filters * 4, 'double_convolution')

    ux2_2 = UpSampling2D(2)(x2_2)
    cx1_3 = concatenate([x1_0, x1_1, x1_2, ux2_2], axis=-1)
    x1_3 = econv_block_2D(cx1_3, starting_filters * 2, 'double_convolution')

    ux1_3 = UpSampling2D(2)(x1_3)
    cx0_4 = concatenate([x0_0, x0_1, x0_2, x0_3, ux1_3], axis=-1)
    x0_4 = econv_block_2D(cx0_4, starting_filters, 'double_convolution')


    output1 = Conv2D(1, 1, padding='same', activation='sigmoid', kernel_initializer = 'he_normal')(x0_1)
    output2 = Conv2D(1, 1, padding='same', activation='sigmoid', kernel_initializer = 'he_normal')(x0_2)
    output3 = Conv2D(1, 1, padding='same', activation='sigmoid', kernel_initializer = 'he_normal')(x0_3)
    output4 = Conv2D(1, 1, padding='same', activation='sigmoid', kernel_initializer = 'he_normal')(x0_4)
    outputs = (output1 + output2 + output3 + output4) / 4

    model = tf.keras.Model(inputs=input_layer, outputs=outputs)
    return model