import io
import torchvision.transforms as transforms
import google.generativeai as genai
from PIL import Image

class Gemini_API_Zho:

    def __init__(self, api_key=None):
        self.api_key = api_key
        if self.api_key is not None:
            genai.configure(api_key=self.api_key)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "What is the meaning of life?", "multiline": True}),
                "model_name": (["gemini-pro", "gemini-pro-vision"],),
                "stream": ("BOOLEAN", {"default": False}),
                "api_key": ("STRING", {"default": ""})  # Add api_key as an input
            },
            "optional": {
                "image": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Zho模块组/✨Gemini"

    def generate_content(self, prompt, model_name, stream, api_key, image=None):
        if api_key:
            self.api_key = api_key
            genai.configure(api_key=self.api_key)
        if not self.api_key:
            raise ValueError("API key is required")

        model = genai.GenerativeModel(model_name)

        if model_name == 'gemini-pro':
            if stream:
                response = model.generate_content(prompt, stream=True)
                textoutput = "\n".join([chunk.text for chunk in response])
            else:
                response = model.generate_content(prompt)
                textoutput = response.text
        
        if model_name == 'gemini-pro-vision':
            if image == None:
                raise ValueError("gemini-pro-vision needs image")
            else:
                image_squeezed = image.squeeze(0)
                image_pil = transforms.ToPILImage()(image_squeezed)
                buf = io.BytesIO()
                image_pil.save(buf, format='JPEG')
                buf.seek(0)
                img = Image.open(buf)

                if stream:
                    response = model.generate_content([prompt, img], stream=True)
                    textoutput = "\n".join([chunk.text for chunk in response])
                else:
                    response = model.generate_content([prompt, img])
                    textoutput = response.text
        
        return (textoutput,)


# DisplayText node is forked from AlekPet，thanks to AlekPet！
class DisplayText_Zho:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):

        return {
            "required": {        
                "text": ("STRING", {"forceInput": True}),     
                },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
            }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True
    FUNCTION = "display_text"

    CATEGORY = "Zho模块组/✨Gemini"

    def display_text(self, text, prompt=None, extra_pnginfo=None):
        return {"ui": {"string": [text,]}, "result": (text,)}


NODE_CLASS_MAPPINGS = {
    "Gemini_API_Zho": Gemini_API_Zho,
    "DisplayText_Zho": DisplayText_Zho
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_API_Zho": "✨Gemini_API_Zho",
    "DisplayText_Zho": "✨DisplayText_Zho"
}
