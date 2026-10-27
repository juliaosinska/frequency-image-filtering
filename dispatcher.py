from PIL import Image
from filters_config import FILTER_CONFIG

from convolution_processors import CONVOLUTION_PROCESSOR_REGISTRY
from frequency_processors import FREQUENCY_PROCESSOR_REGISTRY

PROCESSOR_REGISTRY = {
    **CONVOLUTION_PROCESSOR_REGISTRY,
    **FREQUENCY_PROCESSOR_REGISTRY
}

# ==========================================
# HELPER FUNCTION TO APPLY FILTERS BASED ON CONFIGURATION
# ==========================================

def apply_filter(image: Image.Image, filter_name: str, params: dict, optimized: bool = True) -> Image.Image:
    if filter_name not in FILTER_CONFIG:
        raise ValueError(f"Filter '{filter_name}' is not defined in FILTER_CONFIG.")

    filter_config = FILTER_CONFIG[filter_name]
    filter_type = filter_config["type"]
    filter_processor_key = filter_config["processor"]

    if filter_processor_key not in PROCESSOR_REGISTRY:
        raise ValueError(f"Processor '{filter_processor_key}' for filter '{filter_name}' is not registered.")

    processor_function = PROCESSOR_REGISTRY[filter_processor_key]


    if filter_type == "basic":
        result_image = processor_function(image, **params, optimized=optimized)
        return {
            filter_config["previews"][0]: image,
            filter_config["previews"][1]: result_image
        }
    elif filter_type == "combination":
        return processor_function(image, **params, optimized=optimized)
    elif filter_type == "frequency":
        return processor_function(image, **params)