#############################################################
# Problem 0: Find base point
def GetCurveParameters():
    # Certicom secp256-k1
    # Hints: https://en.bitcoin.it/wiki/Secp256k1
    _p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    _a = 0x0000000000000000000000000000000000000000000000000000000000000000
    _b = 0x0000000000000000000000000000000000000000000000000000000000000007
    _Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    _Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    _Gz = 0x0000000000000000000000000000000000000000000000000000000000000001
    _n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    _h = 0x01
    return _p, _a, _b, _Gx, _Gy, _Gz, _n, _h


#############################################################
# Problem 1: Evaluate 4G
def compute4G(G, callback_get_INFINITY):
    """
    Compute 4G

    :param G: PointJacobi
    :param callback_get_INFINITY: Function that returns INFINITY
    :return: PointJacobi
    """

    res = G
    for i in range(2):
        res = res.double()
    return res


#############################################################
# Problem 2: Evaluate 5G
def compute5G(G, callback_get_INFINITY):
    """
    Compute 5G

    :param G: PointJacobi
    :param callback_get_INFINITY: Function that returns INFINITY
    :return: PointJacobi
    """

    result = G
    for i in range(2):
        result = result.double()
    result += G

    return result


#############################################################
# Problem 3: Evaluate dG
# Problem 4: Double-and-Add algorithm
def double_and_add(n, point, callback_get_INFINITY):
    """
    Calculate n * point using the Double-and-Add algorithm.

    :param n: int
    :param point: PointJacobi
    :param callback_get_INFINITY: Function that returns INFINITY

    :return: PointJacobi, num_doubles, num_additions
    """

    bit_sq = bin(n)[3:]

    res = point
    num_doubles = 0
    num_additions = 0

    for b in bit_sq:
        num_doubles += 1
        res = res.double()

        if b == '1':
            res += point
            num_additions += 1

    return res, num_doubles, num_additions


#############################################################
# Problem 5: Optimized Double-and-Add algorithm
def optimized_double_and_add(n, point, callback_get_INFINITY):
    """
    Optimized Double-and-Add algorithm that simplifies sequences of consecutive 2's.

    :param n: int
    :param point: PointJacobi
    :param callback_get_INFINITY: Function that returns INFINITY

    :return: PointJacobi, num_doubles, num_additions
    """

    bit_sq = bin(n)[2:]
    num_of_pos_operations = len(bit_sq[1:]) + bit_sq[1:].count('1')

    consecutive_str = '1' + ''.join(['0' if b == '1' else '1' for b in bit_sq])
    consecutive_2s = bin(int(consecutive_str, 2) + 1)[2:]
    num_of_neg_operations = len(consecutive_2s[1:]) + consecutive_2s[1:].count('1')

    is_pos_batter = num_of_pos_operations <= num_of_neg_operations

    result = point
    num_doubles = 0
    num_additions = 0

    op_sq = bit_sq[1:] if is_pos_batter else consecutive_2s[1:]
    for b in op_sq:
        result = result.double()
        num_doubles += 1
        if b == '1':
            if is_pos_batter:
                result += point
            else:
                result += -point
            num_additions += 1

    return result, num_doubles, num_additions


#############################################################
# Problem 6: Sign a Bitcoin transaction with a random k and private key d
def sign_transaction(private_key, hashID, callback_getG, callback_get_n, callback_randint):
    """Sign a bitcoin transaction using the private key."""

    G = callback_getG()
    n = callback_get_n()

    z = get_z(n, hashID)
    r = 0
    s = 0

    while r == 0 or s == 0:
        k = callback_randint(1, n - 1)
        R = G.mul_add(k, 0, 0)
        r = R.x() % n
        s = ((r * private_key + z) * pow(k, -1, n)) % n

    signature = (r, s)
    return signature


##############################################################
# Step 7: Verify the digital signature with the public key Q
def verify_signature(public_key, hashID, signature, callback_getG, callback_get_n, callback_get_INFINITY):
    """Verify the digital signature."""

    G = callback_getG()
    n = callback_get_n()

    r, s = signature
    if r <= 0 or r >= n or s <= 0 or s >= n:
        return False

    z = get_z(n, hashID)
    w = pow(s, -1, n)

    u1 = (z * w) % n
    u2 = (r * w) % n

    R = u1 * G + u2 * public_key

    is_valid_signature = R.x() % n == r
    return is_valid_signature


def get_z(n, e):
    l_n = n.bit_length()
    num_e = int(e, 16)
    ell = num_e.bit_length()

    if l_n < ell:
        return num_e >> (ell - l_n)
    else:
        return num_e
