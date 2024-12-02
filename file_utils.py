import os
import aiohttp
import ssl


def directory(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path)


async def save_image(directory: str, image_url: str) -> None:
    if image_url is None:
        print(f"URL gambar tidak valid: {image_url}")
        return

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    filename = os.path.basename(image_url)
    path = os.path.join(directory, filename)

    async with aiohttp.ClientSession() as session:
        async with session.get(image_url, ssl=ssl_context) as response:
            if response.status == 200:
                with open(path, 'wb') as f:
                    f.write(await response.read())
            else:
                print(f"Gagal mengunduh gambar dari {image_url}: {response.status}")
