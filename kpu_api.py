import aiohttp
import ssl


class KPU:
    def __init__(self) -> None:

        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    async def fetch_json(self, session, url):
        async with session.get(url, ssl=self.ssl_context) as response:
            return await response.json()

    async def get_provinces(self) -> dict:
        ENDPOINT = 'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/0.json'
        async with aiohttp.ClientSession() as session:
            contents = await self.fetch_json(session, ENDPOINT)
        return {"name": "provinces", "length": len(contents), "contents": contents}

    async def get_cities(self, prov_id: str) -> dict:
        ENDPOINT = f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{prov_id}.json'
        async with aiohttp.ClientSession() as session:
            contents = await self.fetch_json(session, ENDPOINT)
        return {"name": "city", "length": len(contents), "contents": contents}

    async def get_kec(self, prov_id: str, city_id: str) -> dict:
        ENDPOINT = f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{prov_id}/{city_id}.json'
        async with aiohttp.ClientSession() as session:
            contents = await self.fetch_json(session, ENDPOINT)
        return {"name": "kec", "length": len(contents), "contents": contents}

    async def get_kel(self, prov_id: str, city_id: str, kec_id: str) -> dict:
        ENDPOINT = f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{prov_id}/{city_id}/{kec_id}.json'
        async with aiohttp.ClientSession() as session:
            contents = await self.fetch_json(session, ENDPOINT)
        return {"name": "kel", "length": len(contents), "contents": contents}

    async def get_tps(self, prov_id: str, city_id: str, kec_id: str, kel_id: str) -> dict:
        ENDPOINT = f'https://sirekap-obj-data.kpu.go.id/wilayah/pemilu/ppwp/{prov_id}/{city_id}/{kec_id}/{kel_id}.json'
        async with aiohttp.ClientSession() as session:
            contents = await self.fetch_json(session, ENDPOINT)
        return {"name": "tps", "length": len(contents), "contents": contents}

    async def get_tps_data(self, prov_id: str, city_id: str, kec_id: str, kel_id: str, tps_id: str) -> dict:
        ENDPOINT = f'https://sirekap-obj-data.kpu.go.id/pemilu/hhcw/ppwp/{prov_id}/{city_id}/{kec_id}/{kel_id}/{tps_id}.json'
        async with aiohttp.ClientSession() as session:
            contents = await self.fetch_json(session, ENDPOINT)
        return {"name": "tps_data", "length": len(contents), "contents": contents}