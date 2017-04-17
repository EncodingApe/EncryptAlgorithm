def f(t,B,C,D):
    if 0 <= t < 20:
        return (B & C) | ((~B & 2**32-1) & D)
    elif 20 <= t < 40:
        return B ^ C ^ D
    elif 40 <= t < 60:
        return (B & C) | (B & D) | (C & D)
    else:
        return B ^ C ^ D

def K(t):
    if 0 <= t < 20:
        return 0x5a827999
    elif 20 <= t < 40:
        return 0x6ed9eba1
    elif 40 <= t < 60:
        return 0x8f1bbcdc
    else:
        return 0xca62c1d6

def rotate_move(m,k):
    binary_str = bin(m)[2:]
    if len(binary_str) < 32:
        binary_str = '0'*(32 - len(binary_str)) + binary_str
    new_str = ''.join([binary_str[(i+k)%32] for i in range(len(binary_str))])
    return int('0b'+new_str,2)

def W(t,X):
    if 0 <= t <16:
        return X[t]
    else:
        return rotate_move((W(t-16,X) ^ W(t-14,X) ^ W(t-8,X) ^ W(t-3,X)),1)

def init(message):
    """初始化二进制串"""
    l = len(message)
    if l != 448:
        message += '1'
    while len(message) % 512 != 448:
        message += '0'
    init_len_message = bin(l)[2:]
    if len(init_len_message) < 64:
        init_len_message = '0'*(64-len(init_len_message)) + init_len_message
    init_len_message = init_len_message[:64]
    message += init_len_message
    return message

def SHA(message):
    A,B,C,D,E = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0
    """message以二进制输入"""
    message = init(message=message)
    message_blocks = []
    for i in range(len(message)//512):
        message_blocks.append(message[i*512:(i+1)*512])
    for block in message_blocks:
        X = []
        for i in range(len(block)//32):
            X.append(int('0b'+block[i*32:(i+1)*32],2))
        for t in range(80):
            A,B,C,D,E = (f(t=t, B=B, C=C, D=D) ^ E ^ rotate_move(A,5) ^ W(t=t, X=X) ^ K(t=t)), A, rotate_move(B,30), C, D
    A = bin(A ^ 0x67452301)[2:]
    B = bin(B ^ 0xefcdab89)[2:]
    C = bin(C ^ 0x98badcfe)[2:]
    D = bin(D ^ 0x10325476)[2:]
    E = bin(E ^ 0xc3d2e1f0)[2:]
    if len(A) < 32:
        A = '0'*(32 - len(A)) + A
    if len(B) < 32:
        B = '0'*(32 - len(B)) + B
    if len(C) < 32:
        C = '0'*(32 - len(C)) + C
    if len(D) < 32:
        D = '0'*(32 - len(D)) + D
    return A+B+C+D
