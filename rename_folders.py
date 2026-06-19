import os

base_dir = r"d:\PerfilDeEgresadoCopIA\docs"

mapping = {
    "ce01": "ChristianSalas",
    "ce02": "CristhianLlanque",
    "ce03": "FrankChoquehuanca"
}

for old_name, new_name in mapping.items():
    old_path = os.path.join(base_dir, old_name)
    new_path = os.path.join(base_dir, new_name)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
