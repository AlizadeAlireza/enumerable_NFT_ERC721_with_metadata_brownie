from brownie import AdvancedCollectible, network
from scripts.helpful_scripts import get_breed
from scripts.metadata.sample_metadata import metadata_template
from pathlib import Path
import requests
import json
import os

breed_to_image_uri = {
    "PUG": "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png",
    "SHIBA_INU": "https://ipfs.io/ipfs/QmYx6GsYAKnNzZ9A6NvEKV9nf1VaDzJrqDR23Y8YSkebLU?filename=shiba-inu.png",
    "ST_BERNARD": "https://ipfs.io/ipfs/QmUPjADFGEKmfohdTaNcWhp7VGk26h5jXDA7v3VtTnTLcW?filename=st-bernard.png",
}


def main():
    advanced_collectible = AdvancedCollectible[-1]
    # we want this create metadata to create the metadata
    # for every single token that we've created
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"you have create {number_of_advanced_collectibles} collectibles!")
    for token_id in range(number_of_advanced_collectibles):
        # for each we need have to get the breed
        breed = get_breed(
            advanced_collectible.tokenIdToBreed(token_id)
        )  # this return int(enum) and get breed return the str

        # check to make sure that the file doesn't exist

        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.josn"
        )

        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"a adorable {breed} pup!"
            # upload img to ipfs
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"

            image_uri = None
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
                # means isn't none
            image_uri = image_uri if image_uri else breed_to_image_uri[breed]

            collectible_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(collectible_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)  # shoud print out the metadata uri


def upload_to_ipfs(file_path):
    """to make this a little generic we'll have this upload to ipfs take a file path"""
    # taking this path here and we're opening the file rb means
    # we're opening it binary and upload binary actually to ipfs
    with Path(file_path).open("rb") as fp:
        image_binary = fp.read()
        # upload stuff
        ipfs_url = "http://127.0.0.1:5001/webui"
        # now we want api call or a post request to this endpoint
        endpoint = "/api/v0/add"
        # post request to it
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json("Hash")
        file_name = file_path.split("/")[-1:][0]
        # say if we have "./img/0-PUG.png" -> going to split it up by these slashes -> "0-PUG.png"
        # into an array and grab the last part of the array

        # this format give us ST that sample_token_uri gave
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={file_name}"
        # sample_token_uri = "https://ipfs.io/ipfs/QmSsYRx3LpDAb1GZQm7zZ1AuHZjfbPkD6J7s9r41xu1mf8?filename=pug.png"

        print(image_uri)
        return image_uri
