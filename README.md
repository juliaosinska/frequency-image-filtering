# Image Filtering App

1st part of this solution: [image-filtering](https://github.com/juliaosinska/image-filtering)

2nd part of this solution: [advanced-image-filtering](https://github.com/juliaosinska/advanced-image-filtering)

Part 3 - Current project repository: [frequency-image-filtering](https://github.com/juliaosinska/frequency-image-filtering)

#### Note for the professor
 Please be aware that the new GENAI usage marking is applied only to the part that has been added in this 3rd incremental part of the solution. Other markings developed in previous tasks stay unchanged and true to the 1st version of our commenting practices.

A small Python desktop app for applying convolution-based and frequency-domain image filters.

## Overview

Upload an image, choose a filter, adjust its parameters, inspect the result and intermediate processing stages, and save the output. Convolution filters use NumPy and Pillow, with a choice between basic and optimized convolution. Frequency-domain filters use the 2D Fourier transform and display the image spectrum and filter mask alongside the result.

## Included filters

- Averaging
- Separable Gaussian
- Sharpening
- Laplacian
- Unsharp Mask (USM)
- High-Boost Filter
- Difference of Gaussians (DoG)
- Laplacian of Gaussian (LoG)

### Frequency-domain filters

- Ideal Low-Pass Filter
- Gaussian Low-Pass Filter
- High-Pass Filter
- Band-Pass Filter
- Band-Stop Filter

## Features

- Upload an image from disk
- Preview the original image, filtered output, and intermediate processing stages
- Adjust filter parameters, including kernel size, sigma, strength, boost factor, and frequency cutoffs
- View the log-scaled Fourier spectrum and frequency mask when using a frequency-domain filter
- Set low-pass and high-pass cutoff frequencies, or lower and upper cutoffs for band filters
- Toggle between optimized and basic convolution for convolution filters; this option is disabled for frequency-domain filters
- Automatically limit frequency cutoff sliders to the selected image dimensions
- Save the filtered image as PNG or JPG

## Filter descriptions and parameter effects

### Averaging
- Purpose: smooths the image and reduces noise by replacing each pixel with the average of nearby pixels.
- Effect of parameters: the `Kernel Size` controls the neighborhood size. A larger kernel produces stronger blur, softer transitions, and less visible detail.

### Separable Gaussian
- Purpose: applies Gaussian blur, commonly used to smooth images and prepare them for other enhancement techniques.
- Effect of parameters: the `Sigma` value controls the amount of blur. Larger sigma values produce stronger smoothing and suppress fine details and edges more aggressively.

### Sharpening
- Purpose: increases local contrast around edges to make the image appear sharper.
- Effect of parameters: the `Strength` parameter controls the amount of edge enhancement. Higher values produce stronger sharpening but may introduce halos or unnatural artifacts if set too high.

### Laplacian
- Purpose: highlights rapid intensity changes and detects edges in the image.
- Effect of parameters: the `Laplacian Size` changes the kernel size used for edge detection. Larger kernels detect broader transitions and produce heavier, thicker edge responses.

#### Note: you can see the examples for those basic filters in the related repo: [image-filtering](https://github.com/juliaosinska/image-filtering)

### Unsharp Mask (USM)
- Purpose: creates a sharper image by emphasizing the difference between the original image and its blurred version.
- Effect of parameters: `Sigma` defines the blur used to create the mask; larger sigma gives a smoother base image and a broader sharpening effect. `Alpha` controls the strength of the enhancement; higher values make edges more pronounced but can over-sharpen the image.

### High-Boost Filter
- Purpose: enhances fine details more strongly than a standard unsharp mask while preserving contrast in the image.
- Effect of parameters: `Sigma` controls the amount of initial blur, while `A (Boost Factor)` controls the enhancement strength. Larger values increase detail contrast and edge emphasis, but too high a value can make the image look exaggerated or unnatural.

### Difference of Gaussians (DoG)
- Purpose: detects edges and features by subtracting one blurred version of the image from another with a different blur scale.
- Effect of parameters: `Sigma 1` and `Sigma 2` control the two Gaussian blurs. Increasing either sigma emphasizes larger image structures, while the difference between the values determines which details stand out most.

### Laplacian of Gaussian (LoG)
- Purpose: combines Gaussian smoothing and Laplacian edge detection to detect edges and blob-like structures.
- Effect of parameters: `Sigma` sets the smoothing scale; larger values suppress fine details and emphasize larger structures. `Laplacian Size` changes the sensitivity and thickness of the detected edges.

#### Note: you can see the examples for those advanced filters in the related repo: [advanced-image-filtering](https://github.com/juliaosinska/advanced-image-filtering)

## Frequency-domain filters

These filters convert the image to grayscale, compute its 2D Fourier transform, apply a mask in the frequency domain, and transform the result back to an image. Their previews include the original image, the log-scaled spectrum, the mask, and the filtered result. High-pass results are shifted for grayscale visualization.

### Ideal Low-Pass Filter
- Purpose: keeps frequencies within a circular cutoff and removes higher frequencies, smoothing the image.
- Effect of parameters: `D_0` sets the cutoff radius. As the cutoff radius decreases, the image becomes increasingly blurred, accompanied by noticeable circular ringing artifacts (waves) around high-contrast edges due to the sharp rectangular cutoff.
<img width="1198" height="880" alt="image" src="https://github.com/user-attachments/assets/17d7a464-6ef4-4303-903f-e42d484efb36" />

### Gaussian Low-Pass Filter
- Purpose: weakens higher frequencies smoothly to blur the image with fewer abrupt transitions than an ideal low-pass filter.
- Effect of parameters: `D_0` controls the frequency scale. A smaller cutoff progressively softens the image with natural, smooth transitions, entirely avoiding the artificial ringing halos seen in the ideal low-pass filter.
<img width="1195" height="880" alt="image" src="https://github.com/user-attachments/assets/73c58604-5284-46d7-92c4-bca551f9d585" />

### High-Pass Filter
- Purpose: removes low frequencies and emphasizes fine detail and rapid intensity changes.
- Effect of parameters: `D_0` sets the cutoff radius. Increasing the cutoff radius strips away broader structural shapes, leaving a striking, high-contrast outline of sharp edges and fine textures displayed on a neutral gray background.
<img width="1197" height="874" alt="image" src="https://github.com/user-attachments/assets/90838f38-4408-4f8f-9819-a3d482161203" />

### Band-Pass Filter
- Purpose: keeps frequencies between two cutoff values and removes frequencies outside that band.
- Effect of parameters: `D_1` is the lower cutoff and `D_2` is the upper cutoff. Isolating narrow or shifted frequency bands highlights specific mid-scale structural textures, while pushing the band to the extreme outer edges results in a nearly black image due to the lack of high-frequency energy.
<img width="1194" height="875" alt="image" src="https://github.com/user-attachments/assets/8dcf6058-9eb6-4439-b03c-e83a20d948b5" />

### Band-Stop Filter
- Purpose: removes frequencies between two cutoff values while keeping frequencies outside that band.
- Effect of parameters: `D_1` and `D_2` set the lower and upper cutoffs of the rejected band. Removing a specific band of intermediate frequencies suppresses corresponding mid-scale details while keeping the overall image brightness and primary structure remarkably stable.
<img width="1192" height="876" alt="image" src="https://github.com/user-attachments/assets/992a609c-89b1-4150-acd9-48431125e0da" />

## Project structure

- `gui.py` — Tkinter GUI and user controls
- `filters_config.py` — filter definitions, parameter metadata, and preview labels
- `dispatcher.py` — routes the selected filter to its processor
- `convolution.py` — basic and optimized spatial convolution implementations
- `convolution_processors.py` — spatial and combined-filter implementations
- `frequency_processors.py` — Fourier transform processing and frequency masks
- `test_images/` — sample images for testing and comparing filters

## Requirements

Python, NumPy, and Pillow are required. Tkinter is included with most standard Windows Python installations.

Install the libraries using the same Python interpreter you will use to run the app:

```powershell
python -m pip install Pillow numpy
```

## Run the app

From this project folder:

```powershell
python gui.py
```

## Notes

  ### Comparison of the Ideal Low-Pass Filter and Gaussian Low-Pass Filter with the same D_0 parameter value
  <img width="1193" height="876" alt="image" src="https://github.com/user-attachments/assets/057a8c04-b915-42f8-849d-e8091dece72c" />
  <img width="1193" height="873" alt="image" src="https://github.com/user-attachments/assets/95f7ebff-8d9a-4fad-86e1-a49f3e75fc1b" />

  We can clearly observe that the Ideal Low-Pass filter provides heavy blurring, but because the mask is sharp and "rectangular" (abrupt change from 1 to 0) the frequency suppression is not natural. There are ringing artifacts - wavy halos around the high-contrast edges.

  Meanwhile, Gaussian Low-Pass filter provides more natural and soft blurring effect which is because of the exponential roll-off in distance from the center of the mask. There are no ringing artifacts.

  ### AI usage
  - Added the +128 shift for the high-pass filter. It's for the purpose of better visualization. Avoiding pitch black backgroundd.
  - Added an optimized version of the mask builder for ideal low-pass and Gaussian low-pass filters. Instead of using nested loops that are extremely inefficient for large images - we use numpys vectorization to speed up tghe process around 50x.

   
