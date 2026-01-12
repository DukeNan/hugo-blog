import json

import requests

PAGE_SIZE = 100
URL = "https://hub.docker.com/v2/repositories/{namespace}/{repository}/tags/?page_size={PAGE_SIZE}"


def fetch_digests(namespace, repository, digest=None):
    if not digest:
        return []
    url = URL.format(namespace=namespace, repository=repository, PAGE_SIZE=PAGE_SIZE)

    while url:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        for result in data.get("results", []):
            for image in result.get("images", []):
                if image.get("digest") == digest:
                    return result
            if result.get("digest") == digest:
                return result
        url = data.get("next")

    return None


if __name__ == "__main__":
    namespace = "n8nio"
    repository = "n8n"
    digest = "sha256:4a43ddf853afe3ad44be51379e7ed85c16b974cae26cf732d2fcbf71d0cb16c4"
    result = fetch_digests(namespace, repository, digest)
    print(json.dumps(result))
