import numpy as np
from PIL import Image

# ==========================================
# BASE FOR FREQUENCY DOMAIN FILTERING
# ==========================================

# MY OWN CODE: manually implemented the pipeline defined in the task for frequency domain filtering
def apply_frequency_filter(image: Image.Image, mask_function, **params) -> dict:
    grayscale_image = image.convert("L")
    image_array = np.array(grayscale_image)
    N, M = image_array.shape

    # 1a. compute the 2D Fourier Transform of the image
    F = np.fft.fft2(image_array)
    # 1b. shift to the center of the spectrum
    F_shifted = np.fft.fftshift(F)

    # spectrum log needed for visualization of the frequency spectrum
    spectrum_log = np.log(1 + np.abs(F_shifted))
    # normalize the spectrum log to the range [0, 255] for preview
    spectrum_log = np.clip(255 * (spectrum_log / np.max(spectrum_log)), 0, 255).astype(np.uint8)

    # 2. apply the frequency mask
    H = mask_function(N, M, **params)
    mask_visual = (H * 255).astype(np.uint8)  # for preview

    # 3. filtration in the frequency domain
    G_shifted = F_shifted * H

    # 4a. shift back to the original position of the spectrum
    G = np.fft.ifftshift(G_shifted)
    # 4b. compute the inverse 2D Fourier Transform to get the filtered image and get the real part
    filtered_image_array = np.real(np.ifft2(G))

    # clip the filtered image to the range [0, 255]
    filtered_image_array = np.clip(filtered_image_array, 0, 255).astype(np.uint8)

    return {
        "Original": image,
        "Spectrum (log)": Image.fromarray(spectrum_log),
        "Mask H(u,v)": Image.fromarray(mask_visual),       
        "Filtered Result": Image.fromarray(filtered_image_array)
    }

# ==========================================
# MASKS
# ==========================================

# MY OWN CODE: manually implemented the mask for ideal low-pass filter
def build_ideal_low_pass_mask(N, M, D_0):
    # column vector
    u = np.arange(N).reshape(-1, 1)
    # row vector
    v = np.arange(M).reshape(1, M)

    # broadcast to create a grid of distances from the center
    D = np.sqrt((u - N/2)**2 + (v - M/2)**2)

    H = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            if D[i, j] <= D_0:
                H[i, j] = 1
            else:
                H[i, j] = 0

    return H

# MY OWN CODE: manually implemented the mask for gaussian low-pass filter
def build_gaussian_low_pass_mask(N, M, D_0):
    # column vector
    u = np.arange(N).reshape(-1, 1)
    # row vector
    v = np.arange(M).reshape(1, M)

    # broadcast to create a grid of distances from the center
    D = np.sqrt((u - N/2)**2 + (v - M/2)**2)

    H = np.zeros((N, M))
    for i in range(N):
        for j in range(M):
            H[i, j] = np.exp(-(D[i, j]**2) / (2 * (D_0**2)))

    return H

# MY OWN CODE: manually implemented the mask for high-pass filter
def build_high_pass_mask(N, M, D_0):
    # I will base it on the ideal low-pass mask
    H_low_pass = build_ideal_low_pass_mask(N, M, D_0)
    H = 1 - H_low_pass

    return H

# MY OWN CODE: manually implemented the mask for band-pass filter
def build_band_pass_mask(N, M, D_1, D_2):
    # I will base it on the ideal low-pass mask
    H_low_pass_D1 = build_ideal_low_pass_mask(N, M, D_1)
    H_low_pass_D2 = build_ideal_low_pass_mask(N, M, D_2)

    H = H_low_pass_D2 - H_low_pass_D1

    return H

# MY OWN CODE: manually implemented the mask for band-stop filter
def build_band_stop_mask(N, M, D_1, D_2):
    H_band_pass = build_band_pass_mask(N, M, D_1, D_2)
    H = 1 - H_band_pass

    return H

# ==========================================
# HELPER WRAPPERS TO STAY CONSISTENT THROUGH THE ARCHITECTURE
# ==========================================

def run_ideal_low_pass(image: Image.Image, D_0: float = 30.0) -> dict:
    return apply_frequency_filter(image, build_ideal_low_pass_mask, D_0=D_0)

def run_gaussian_low_pass(image: Image.Image, D_0: float = 30.0) -> dict:
    return apply_frequency_filter(image, build_gaussian_low_pass_mask, D_0=D_0)

def run_high_pass(image: Image.Image, D_0: float = 30.0) -> dict:
    return apply_frequency_filter(image, build_high_pass_mask, D_0=D_0)

def run_band_pass(image: Image.Image, D_1: float = 10.0, D_2: float = 50.0) -> dict:
    return apply_frequency_filter(image, build_band_pass_mask, D_1=D_1, D_2=D_2)

def run_band_stop(image: Image.Image, D_1: float = 10.0, D_2: float = 50.0) -> dict:
    return apply_frequency_filter(image, build_band_stop_mask, D_1=D_1, D_2=D_2)

# ==========================================
# PROCESSORS REGISTRY
# ==========================================

FREQUENCY_PROCESSOR_REGISTRY = {
    "run_ideal_low_pass": run_ideal_low_pass,
    "run_gaussian_low_pass": run_gaussian_low_pass,
    "run_high_pass": run_high_pass,
    "run_band_pass_": run_band_pass,
    "run_band_stop": run_band_stop,
}