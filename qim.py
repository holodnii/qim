import numpy as np
from PIL import Image
import bitarray

# GLOBALS
# C:\Users\holod\Downloads\cat1.png
# C:\Users\holod\Downloads\EML-NET-Saliency-master\EML-NET-Saliency-master\encoded_image.png
q = 6
msg_bit_len = 24 # "hii" bit-len

def Open(src):
    img = Image.open(src)
    arr = np.array(img)
    return arr

def EncodeQim(arr, msg):
    ba = bitarray.bitarray()
    ba.frombytes(msg.encode('utf-8'))
    print("original message: ", ba)
    counter = 0
    b_counter = 0

    for i in arr:
        for pixel in i:
            for idx, c in enumerate(pixel):
                if counter < len(ba):
                    pixel[idx] = q * (c//q) + q/2 * ba[b_counter]
                # change to last elem checker
                else:
                    break
                counter = counter + 1
                b_counter = b_counter + 1
    return arr

def DecodeQim(arr):
    bit_str = ""
    counter = 0
    for i in arr:
        for pixel in i:
            for c in pixel:
                if counter < msg_bit_len:
                    C0 = q * (c//q)
                    C1 = q * (c//q) + q/2
                    if abs(c - C0) < abs(c - C1):
                        bit_str += "0"
                    else:
                        bit_str += "1"
                counter = counter + 1
    return bit_str

def SaveImage(encoded_array):
    image = Image.fromarray(encoded_array, "RGBA")
    image = image.save('encoded_image.png') 

def main(response):
    if response == "1":
        src = input("Enter image path: ")
        msg = input("Enter message to encode in image: ")
        rgb_matrix = Open(src)
        encoded_rgb_matrix = EncodeQim(rgb_matrix, msg)
        SaveImage(encoded_rgb_matrix)
    if response == "2":
        src = input("Enter image path: ")
        rgb_matrix_encoded = Open(src)
        msg = DecodeQim(rgb_matrix_encoded)
        print("decoded message: ", msg)

        


# main
print("select mode: ")
print("1. encode image")
print("2. decode image")
response = input("Enter 1/2: ")

main(response)