from pathlib import Path
import os
from decouple import config
import cloudinary
from cloudinary.uploader import upload
from cloudinary.api import resources

def test_cloudinary_upload():
    """Test complet de connexion, upload et récupération sur Cloudinary"""

    # --- Définir BASE_DIR avant de l'utiliser ---
    BASE_DIR = Path(__file__).resolve().parent.parent  # ← remonte au dossier racine du projet

    # --- Configuration Cloudinary ---
    cloudinary.config(
        cloud_name=config("CLOUD_NAME"),
        api_key=config("API_KEY"),
        api_secret=config("API_SECRET"),
        secure=True
    )

    print(" Connecté :", cloudinary.api.ping())

    # --- Chemin vers ton image locale ---
    image_path = BASE_DIR / "media" / "sport_media" / "VTT_2024 (2).jpg"

    print(" Vérification du fichier :", image_path)

    if not os.path.exists(image_path):
        print(" Le fichier n'existe pas à cet emplacement.")
        return

    print(" Upload de l’image vers Cloudinary...")
    result = upload(str(image_path), folder="sport_media")

    print(" Upload réussi :", result["secure_url"])

   
   # --- Vérifier que l’image est bien enregistrée ---
resp = resources(type="upload", prefix="sport_media/")
print(f"\n {len(resp['resources'])} image(s) trouvée(s) dans Cloudinary :")

for img in resp["resources"]:
    print("-", img["public_id"], "→", img["secure_url"])

