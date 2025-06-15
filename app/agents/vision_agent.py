from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

def describe_image_with_blip(img_path):
    """Generate a professional e-commerce description of a T-shirt"""
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = model.to(device)
    model.eval()

    # Professional prompt focusing ONLY on the T-shirt (no people/background)
    prompt = (
        "Generate a concise, professional product description for this t-shirt. "
        "Describe ONLY the garment's features in this structure:\n"
        "1. **Color**: [primary color, secondary colors]\n"
        "2. **Design**: [graphics, patterns, text/logos]\n"
        "3. **Neckline**: [crew neck, V-neck, etc.]\n"
        "4. **Sleeves**: [short/long/sleeveless, fit]\n"
        "5. **Style**: [casual, sporty, vintage, etc.]\n"
        "6. **Material**: [if visible, e.g., cotton blend]\n"
        "---\n"
        "Avoid mentioning models, people, or backgrounds."
    )
    
    try:
        image = Image.open(img_path).convert("RGB")
        
        # Process image WITHOUT text first (to reduce prompt leakage)
        inputs = processor(images=image, return_tensors="pt").to(device)
        
        with torch.no_grad():
            output_ids = model.generate(
                **inputs,
                max_new_tokens=150,
                num_beams=5,
                early_stopping=True,
                do_sample=True,
                temperature=0.7,
                no_repeat_ngram_size=2
            )
        
        description = processor.decode(output_ids[0], skip_special_tokens=True)
        
        # Post-processing to clean output
        description = (
            description.replace("a photography of", "")
            .replace("a picture of", "")
            .replace("a woman", "")
            .replace("a man", "")
            .strip()
        )
        return description.capitalize()
    
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        torch.cuda.empty_cache() if torch.cuda.is_available() else None

