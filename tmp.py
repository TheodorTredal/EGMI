from huggingface_hub import hf_hub_download, snapshot_download
from secret_stuff import HF_TOKEN
# file_path = hf_hub_download(repo_id="ericwi09/ROSIE", filename="model.pth")


#TOKEN1 (Huggingface token - readonly)



folder_path = snapshot_download(
    repo_id="ericwu09/ROSIE",
    token=HF_TOKEN
    )


print(f"Downloaded contents to: {folder_path}")

