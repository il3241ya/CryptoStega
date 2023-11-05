# CryptoStega

This repository stores python implementation of cryptographic and steganographic algorithms. Below you can see the list of implemented algorithms

## Crypto

### Vigener cipher https://github.com/il3241ya/crypto_stegano/tree/crypto/vigener
Gamma generation involves applying a certain sequence (gamma) generated based on the encryption key to the plaintext. Applying the gamma to the plaintext typically means adding the characters of the plaintext to the characters of the gamma modulo the corresponding alphabet. However, in classical ciphers, applying the gamma may involve calculating the values of ciphertext characters based on the values of corresponding plaintext characters and the gamma using a certain rule.

One of the classic examples of a cipher that uses gamma generation is the Vigenère cipher, structured as follows. The characters of an alphabet A with a size of m are represented as elements of the set Zm. The plaintext and ciphertext are denoted as x = (x1, ..., xl) and y = (y1, ..., yl), where xi, yi ∈ Zm, i = 1, l.

The encryption key is represented as a sequence of characters from the alphabet, k = (k1, ..., kr), kj ∈ Zm, j = 1, r, with r ≤ l, used to generate the gamma γ = (γ1, ..., γr), where γi ∈ Zm, i = 1, r.

Encryption involves adding the characters of the plaintext to the characters of the gamma modulo m:

yi = (xi + γi) mod m.

Decryption involves subtracting the characters of the gamma from the characters of the ciphertext modulo m.

In the Vigenère cipher, a short phrase called the "slogan" (password) is typically used as the encryption key, and it is cyclically repeated to form the gamma.

Another approach to generating a pseudo-random key sequence is the "Vigenère self-key." Here, only one character is chosen as the initial key, and it is followed by all the characters of the plaintext, except the last one, to create the gamma. Alternatively, the gamma can be formed by adding characters from the ciphertext sequentially to the initial character.

### Hill cipher https://github.com/il3241ya/crypto_stegano/tree/crypto/hill

The Hill cipher is an example of a block cipher based on matrix transformations using modular arithmetic. This cipher is structured as follows.

The plaintext is considered as a sequence of characters from an alphabet A with a size of m, represented as elements of the set Zm. Before encryption, the plaintext is divided into blocks of length n, and each block is represented as an n-dimensional vector.

The cipher key is a square matrix of size n × n, composed of elements from the set Zm: K = (ki,j), ki,j ∈ Zm. This matrix must be invertible in Zm for decryption to be possible. The matrix will be invertible only if its determinant |K| satisfies the following two conditions: |K| ≠ 0 and GCD(|K|, m) = 1.

The encryption operation involves multiplying the key matrix by the column vector X = (x1, ..., xn)T, corresponding to a block of plaintext:

Y = EK (X) = K(x1, ..., xn)T = (y1, ..., yn)T.

To decrypt the ciphertext, it needs to be divided into blocks of length n, and each block is represented as a vector Y = (y1, ..., yn)T. Then, the inverse multiplication is performed:

X = DK (Y) = K⁻¹(y1, ..., yn)T = (x1, ..., xn)T.

In the case of the recurrent Hill cipher, a separate key matrix is formed for each plaintext block. Two invertible matrices, K1 and K2, are set up for encrypting the first two plaintext blocks. Afterward, for each subsequent block, a new key matrix is calculated based on the previous two:

Ki = Ki-1Ki-2.

To decrypt ciphertext obtained using the recurrent Hill cipher, it's necessary to find the inverse matrices for K1 and K2. After that, all subsequent inverse matrices can be calculated based on the previous ones:

K⁻¹i = K⁻¹i-2K⁻¹i-1.

## Stegano

### QIM stego https://github.com/il3241ya/crypto_stegano/tree/stegano/qim

The Quantization Index Modulation (QIM) method [3] involves changing the pixel values of an image based on the values of the embedded message bits. This operation is referred to as modulation. Embedding a bit mi is done in the container pixel Pi using formula

Here, q is the quantization step (an even number), ⌊...⌋ denotes taking the integer part of the division.

For extraction, the situation is modeled where both the zero and one bits are embedded in the pixel Pi'. The resulting bit is determined based on which of the two values, P i', is closer to the actual value P i''. The formula for extracting one bit is presented in formula.

### Watermark https://github.com/il3241ya/crypto_stegano/tree/stegano/watermark

A digital watermark (DWM) is additional information embedded in digital images for the purpose of authentication or integrity control. DWMs vary in their resistance to distortions: fragile DWMs are destroyed with any changes to the container, semi-fragile ones can withstand certain authorized transformations, and robust DWMs remain detectable even after significant image-container distortions.

Semi-fragile and robust DWMs are of great value for solving tasks related to the authentication of digital content and protecting its ownership. To achieve this, approaches to embedding additional information must leave traces of the watermark intact after various attacks on the image containing the DWM. While the literature includes analyses of the robustness of DWM embedding algorithms to a variety of attacks, not all of these attacks are practically relevant. The probability of images with watermarks being subjected to "salt-and-pepper" noise or median filtering is extremely low. Real-world scenarios involve typical image processing operations such as cropping, scaling, brightness and/or contrast adjustments, and JPEG compression. Therefore, embedding robustness relative to this list of attacks is of the utmost practical value.

In general, the frequency domain of images allows for greater robustness in embedding while preserving visual imperceptibility compared to the spatial domain. Embedding information in the frequency domain of digital images involves the prior implementation of some frequency transformation and subsequent modification of the obtained frequency coefficients. The most widely used transformations for concealing information in digital images include the discrete cosine transform (DCT), discrete Fourier transform (DFT), and discrete wavelet transform (DWT).
