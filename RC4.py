def RC4(message, S):
    stream = [int('0x'+message[i:i+2], 16) for i in range(0,len(message),2)]
    i, j = 0, 0
    ans = []
    for byte in stream:
        i = (i+1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        k = S[t]
        ans.append(hex(byte ^ k))
    return ans


def generate_K(key, K):
    key = [int('0x'+key[i:i+2], 16) for i in range(0,len(key),2)]
    for i in range(256//len(key)):
        K.extend(key)


def generate_S(K):
    init_S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j+init_S[i]+K[i]) % 256
        init_S[i], init_S[j] = init_S[j], init_S[i]
    return init_S


def pprint(Crypt):
    for i in Crypt:
        if len(i[2:]) == 1:
            print('0'+i[2:], end=' ')
        else:
            print(i[2:], end=' ')


if __name__ == '__main__':
    message = '11223344556677889900AABBCCDDEEFF'
    print("message = 11 22 33 44 55 66 77 88 99 00 aa bb cc dd ee ff")
    key = '13579BDF02468ACE1234567890ABCDEF'
    K = []
    generate_K(key=key, K=K)
    S = generate_S(K=K)
    Crypt = RC4(message=message, S=S)
    print('Crypt : ',end='')
    pprint(Crypt)
