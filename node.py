import time
import base64
import requests
import numpy as np

from io import BytesIO
from PIL import Image, ImageOps

#You can use this node to save full size images through the websocket, the
#images will be sent in exactly the same format as the image previews: as
#binary images on the websocket with a 8 byte header indicating the type
#of binary message (first 4 bytes) and the image format (next 4 bytes).

#Note that no metadata will be put in the images saved with this node.

class SendHttpRequest:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"images": ("IMAGE", ),
                              "url": ("STRING", {"multiline": False, "default": "https:yourdomain..."}),
                             },
               
                }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "api/image"

    def save_images(self, images, url):
        step = 0
        for image in images:
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            rawBytes = BytesIO()
            img.save(rawBytes, "PNG")
            rawBytes.seek(0)
            requests.post(url,data={'img': base64.b64encode(rawBytes.read()).decode('utf-8')})
            step += 1

        return {}

    def IS_CHANGED(s, images):
        return time.time()

NODE_CLASS_MAPPINGS = {
    "Send Http Request": SendHttpRequest,
}
