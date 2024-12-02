import asyncio
from kpu_api import KPU
from file_utils import directory, save_image
from csv_utils import write_csv


async def main(province=None, city=None, kecamatan=None, kelurahan=None):
    kpu = KPU()

    cari_wilayah = False

    provinces = (await kpu.get_provinces())["contents"]
    for v_province in provinces:
        province_name = v_province['nama']
        province_code = v_province['kode']
        if province and province_name != province:
            continue
        cari_wilayah = True

        cities = (await kpu.get_cities(province_code))["contents"]
        for v_city in cities:
            city_name = v_city['nama']
            city_code = v_city['kode']
            if city and city_name != city:
                continue
            cari_wilayah = True

            kecamatan_data = (await kpu.get_kec(province_code, city_code))["contents"]
            for v_kecamatan in kecamatan_data:
                kecamatan_name = v_kecamatan['nama']
                kecamatan_code = v_kecamatan['kode']
                if kecamatan and kecamatan_name != kecamatan:
                    continue
                cari_wilayah = True

                kelurahan_data = (await kpu.get_kel(province_code, city_code, kecamatan_code))["contents"]
                for v_kelurahan in kelurahan_data:
                    kelurahan_name = v_kelurahan['nama']
                    kelurahan_code = v_kelurahan['kode']
                    if kelurahan and kelurahan_name != kelurahan:
                        continue
                    cari_wilayah = True

                    file_name = f"./datasets/{province_name}_{city_name}_{kecamatan_name}.csv"

                    tps = (await kpu.get_tps(province_code, city_code, kecamatan_code, kelurahan_code))["contents"]

                    for v_tps in tps:
                        tps_name = v_tps['nama']
                        tps_code = v_tps['kode']

                        tps_data = (await kpu.get_tps_data(province_code, city_code, kecamatan_code, kelurahan_code, tps_code)).get("contents")

                        if not tps_data:
                            print(f"Tidak ada data untuk TPS {tps_name}.")
                            continue

                        fields = [
                            'ID Provinsi', 'Nama Provinsi', 'ID Kota/Kabupaten', 'Nama Kota/Kabupaten',
                            'ID Kecamatan', 'Nama Kecamatan', 'ID Kelurahan/Desa', 'Nama Kelurahan/Desa',
                            'ID TPS', 'Nama TPS', 'DPT', 'DPTb', 'DPK', 
                            'Paslon 01', 'Paslon 02', 'Paslon 03',
                            'Suara Sah', 'Suara Tidak Sah', 'Total Suara', 'Status',
                            'Gambar Formulir Model C.Hasil-PPWP ke-1', 'Gambar Formulir Model C.Hasil-PPWP ke-2', 'Gambar Formulir Model C.Hasil-PPWP ke-3'
                        ]

                        administrative = tps_data.get('administrasi', {})
                        if administrative:
                            DPT = administrative.get('pemilih_dpt_j', "null")
                            DPTb = administrative.get('pengguna_dptb_j', "null")
                            DPK = administrative.get('pengguna_non_dpt_j', "null")

                            valid_vote = administrative.get('suara_sah', "null")
                            invalid_vote = administrative.get('suara_tidak_sah', "null")
                            total_vote = administrative.get('suara_total', "null")
                        else:
                            DPT, DPTb, DPK = "null", "null", "null"
                            valid_vote, invalid_vote, total_vote = "null", "null", "null"

                        chart = tps_data.get('chart', {})
                        if chart:
                            pres_data = sum([0 if v is None else v for v in chart.values()])

                            if pres_data == valid_vote and valid_vote + invalid_vote == total_vote:
                                paslon_1 = chart.get('100025', "null")
                                paslon_2 = chart.get('100026', "null")
                                paslon_3 = chart.get('100027', "null")
                                status = 'VALID'
                            else:
                                paslon_1 = chart.get('100025', "null")
                                paslon_2 = chart.get('100026', "null")
                                paslon_3 = chart.get('100027', "null")
                                status = 'INVALID'
                        else:
                            paslon_1, paslon_2, paslon_3 = "null", "null", "null"
                            status = 'PROCESS'

                        images = tps_data.get('images', [])
                        image_keys = {}
                        if images:
                            tasks = []
                            for i, img in enumerate(images, start=1):
                                key = f'Gambar Formulir Model C.Hasil-PPWP ke-{i}'
                                image_keys[key] = img or "null"
                                if img:
                                    cform_path = f"./formc/{province_name}/{city_name}/{kecamatan_name}/{kelurahan_name}/{tps_name}".replace(" ", "_")
                                    directory(cform_path)
                                    task = asyncio.create_task(save_image(cform_path, img))
                                    tasks.append(task)
                            await asyncio.gather(*tasks)
                        else:
                            for i in range(1, 4):
                                key = f'Gambar Formulir Model C.Hasil-PPWP ke-{i}'
                                image_keys[key] = "null"

                        data = {
                            'ID Provinsi': province_code or "null",
                            'Nama Provinsi': province_name or "null",
                            'ID Kota/Kabupaten': city_code or "null",
                            'Nama Kota/Kabupaten': city_name or "null",
                            'ID Kecamatan': kecamatan_code or "null",
                            'Nama Kecamatan': kecamatan_name or "null",
                            'ID Kelurahan/Desa': kelurahan_code or "null",
                            'Nama Kelurahan/Desa': kelurahan_name or "null",
                            'ID TPS': tps_code or "null",
                            'Nama TPS': tps_name or "null",
                            'DPT': DPT,
                            'DPTb': DPTb,
                            'DPK': DPK,
                            'Paslon 01': paslon_1,
                            'Paslon 02': paslon_2,
                            'Paslon 03': paslon_3,
                            'Suara Sah': valid_vote,
                            'Suara Tidak Sah': invalid_vote,
                            'Total Suara': total_vote,
                            'Status': status,
                            **image_keys
                        }

                        write_csv(file_name, data, fields)

                        print(f"\n[{province_name} | {city_name} | {kecamatan_name} | {kelurahan_name} | {tps_name}] Data Disimpan!")
                        print(f"Data\t\t: {file_name}")
                        print(f"Gambar Form C\t: ./formc/{province_name}/{city_name}/{kecamatan_name}/{kelurahan_name}/{tps_name}")
                        
    return cari_wilayah


if __name__ == "__main__":
    province = input("Input Provinsi (atau kosongkan)\t\t: ").strip() or None
    city = input("Input Kota/Kabupaten (atau kosongkan)\t: ").strip() or None
    kecamatan = input("Input Kecamatan (atau kosongkan)\t: ").strip() or None
    kelurahan = input("Input Kelurahan/Desa (atau kosongkan)\t: ").strip() or None

    print(f"\nWilayah: Provinsi={province} | Kota/Kabupaten={city} | Kecamatan={kecamatan} | Kelurahan/Desa={kelurahan}")

    cari_wilayah = asyncio.run(main(province, city, kecamatan, kelurahan))
    
    if cari_wilayah:
        print("\nProgram selesai. Data berhasil dimuat.")
    else:
        print("\nData wilayah tidak ditemukan! Silakan periksa input Anda!")