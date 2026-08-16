import os
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
from backend.config import settings

class AIService:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        self.classes = ["FAKE", "REAL"]
        self._load_model()

    def _load_model(self):
        try:
            if not os.path.exists(settings.MODEL_PATH):
                print(f"[WARN] Model file not found at {settings.MODEL_PATH}")
                return

            model = models.resnet18(weights=None)
            model.fc = nn.Linear(model.fc.in_features, 2)
            
            state_dict = torch.load(settings.MODEL_PATH, map_location=self.device)
            model.load_state_dict(state_dict)
            model.to(self.device)
            model.eval()
            
            self.model = model
            print("[INFO] PyTorch ResNet-18 Model loaded successfully.")
        except Exception as e:
            print("[ERROR] Failed to load PyTorch model:", e)
            self.model = None

    @staticmethod
    def validate_image(image_path: str) -> tuple[bool, str]:
        """
        Validates that the file exists, can be opened by PIL, has positive dimensions, and is not corrupted.
        """
        if not os.path.exists(image_path):
            return False, "File does not exist"
        try:
            with Image.open(image_path) as img:
                img.verify()
            with Image.open(image_path) as img:
                img.load()
                w, h = img.size
                if w <= 0 or h <= 0:
                    return False, "Invalid image dimensions"
            return True, "Valid"
        except Exception as e:
            return False, f"Corrupted image or unreadable format: {str(e)}"

    def predict(self, image_path: str) -> dict:
        """
        Runs PyTorch ResNet-18 inference on the given image file.
        Returns normalized AI score (0.0 to 1.0) and class label.
        """
        valid, msg = self.validate_image(image_path)
        if not valid:
            return {
                "success": False,
                "label": "UNKNOWN",
                "score": 0.5,
                "confidence": 50.0,
                "probabilities": {"REAL": 0.5, "FAKE": 0.5},
                "error": msg
            }

        if self.model is None:
            return {
                "success": False,
                "label": "UNKNOWN",
                "score": 0.5,
                "confidence": 50.0,
                "probabilities": {"REAL": 0.5, "FAKE": 0.5},
                "error": "Model not loaded"
            }

        try:
            img = Image.open(image_path).convert("RGB")
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)

            with torch.no_grad():
                output = self.model(img_tensor)
                probs = torch.softmax(output, dim=1)[0]

            fake_prob = float(probs[0])
            real_prob = float(probs[1])

            predicted_class_idx = int(torch.argmax(probs))
            label = self.classes[predicted_class_idx]
            confidence_pct = float(probs.max()) * 100.0
            
            # Score is real_prob (0.0 to 1.0)
            ai_score = round(real_prob, 4)

            return {
                "success": True,
                "label": label,
                "score": ai_score,
                "confidence": round(confidence_pct, 2),
                "probabilities": {
                    "REAL": round(real_prob * 100.0, 2),
                    "FAKE": round(fake_prob * 100.0, 2)
                },
                "error": None
            }
        except Exception as e:
            print("[ERROR] Model Prediction Exception:", e)
            return {
                "success": False,
                "label": "UNKNOWN",
                "score": 0.5,
                "confidence": 50.0,
                "probabilities": {"REAL": 0.5, "FAKE": 0.5},
                "error": str(e)
            }

ai_service = AIService()
