import json

class Encoder(json.JSONEncoder):
    def default(self, obj):
        name = type(obj).__name__
        try:
            encoder = getattr(self, f"encode_{name}")
        except AttributeError:
            super().default(obj)
        else:
            encoded = encoder(obj)
            encoded["__extended_json_type__"] = name
            return encoded
        
    def encode_complex(self, c):
        return {"real": c.real, "img": c.img}

    def encode_range(self, r):
        return {"start": r.start, "stop": r.stop, "step": r.step}

class Decoder(json.JSONDecoder):
    def __init__(self, **kwargs):
        kwargs["object_hook"] = self.object_hook
        super().__init__(**kwargs)

    def object_hook(self, obj):
        try:
            name = obj["__extended_json_type__"]
            decoder = getattr(self, f"decode_{name}")
        except (KeyError, AttributeError):
            return obj
        else:
            return decoder(obj)
        
    def decode_complex(self, obj):
        return complex(obj["real"], obj["img"])

    def decode_range(self, obj):
        return range(obj["start"], obj["stop"], obj["step"])

def dumps(data, cls=Encoder):
    return json.dumps(data, cls=cls)

def loads(data, cls=Decoder):
    return json.loads(data, cls=cls)
