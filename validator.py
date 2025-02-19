import aiohttp
import asyncio

async def validate_gamepass_code(offer_id, access_token):
    url = f"https://emerald.xboxservices.com/xboxcomfd/buddypass/ValidateOfferRedeemer?market=US&offerId={offer_id}"
    
    headers = {
        'Host': 'emerald.xboxservices.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Referer': 'https://www.xbox.com/',
        'Authorization': f'{access_token}',
        'ms-cv': '32/D+TAd5PAeBQn8G26dgi.10',
        'x-ms-api-version': '1.0',
        'Origin': 'https://www.xbox.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'Priority': 'u=4',
        'TE': 'trailers'
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                print(result)
                if result == "OfferValid":
                    return True
                elif result == "OfferNotFound" or result == "OfferAlreadyClaimed":
                    return False
                else:
                    return False
            else:
                print(f"Error: {response.status} - {await response.text()}")
                return False

async def clean_invalid_codes(file_path, access_token):
    with open(file_path, 'r', encoding='utf-8') as file:
        codes = file.readlines()
    
    # Remove duplicates and strip whitespace
    unique_codes = list(set(code.strip() for code in codes))
    
    valid_codes = []
    
    tasks = [validate_gamepass_code(code, access_token) for code in unique_codes]
    results = await asyncio.gather(*tasks)
    
    for code, is_valid in zip(unique_codes, results):
        if is_valid:
            valid_codes.append(code)
        else:
            print(f"Invalid code removed: {code}")
    
    with open(file_path, 'w', encoding='utf-8') as file:
        for valid_code in valid_codes:
            file.write(f"{valid_code}\n")

# Example usage
file_path = 'info/codes.txt'
access_token = 'XBL3.0 x=14864301795157748660;eyJlbmMiOiJBMTI4Q0JDK0hTMjU2IiwiYWxnIjoiUlNBLU9BRVAiLCJjdHkiOiJKV1QiLCJ6aXAiOiJERUYiLCJ4NXQiOiJrU1Z0emNPQVJnZ20yT1lSQUx5M3Y4djA2dEEifQ.FZe5tn9o-mKbuB2zxyQiaBarZeSeATojfotyPvdAo8K08WjzV27NqlbkSEn6YYJbgCNIShnH-sdwujN9eoBUkfblQO5sOGSC6Bc1lEIwwwGZK-KzKY4u2UNbVQqBMx3yTmZkIZXJtHN6DFTR7LVbwzOtZDTPnKEJqz9QIlLP44At5FPx8qZvgFUdQx-cb-HEnrgd5ZU3RqkcQW_c3gG2HBAQiQqvpgTk55fijRbDDij1Fhx02jCEhJAlRy-yZmB0eYHMVC83CFtrIcKvXEJJ8T8qZl02srEbIrfTv_NiZKvxDJBV7TkJXqaUTdcp1J-6b-ERlLOsfm9VL27VyuFYQg.w_ScTTXv8TiznJcxD4UKmw.PMSdTAjuSZiFjhE8nIYCmV2vk_rUsiucYTFvtvIzCvqusl2BexxODsUQ3PMRKpnbhixfLOQHBwu-GGC4euM1onKUV5-_ZILUqQNDhyWUNAmMi2xXW8Fyxb_YN8o00fRY1IVLtNC0zG5jv1YyYutrYgcOAg13fcmkcWc9zNxAgA8_a0Erd4jJHbCGlMlPAhDl6AKMePSdI6qB-ypQM4oO0OF29qbEdwgmY_aovfOVckHKN8dSR-eXBORMlFwoHd7eKZ5eH-Pg4fBGUOO2i5D5MrJvLhq0zQWbF_hmZOBFb9iXFeAM0v1K1FnrbhH4slvAE6LVO4N8iQn3Al1wrU7SUyQdXSEHfnfIfbVjIKrvDUg0bRe-EUTzSyrkRCzACcl00FX5zKC4nQBEoyjID3SsXAUSDc7YvUh14CM_z15L3tQNX8gnKhufsGS1WHiODq3XSi_G9XjLOo7Ytdq7-jmGsjxd8NQg7pDWXzc5v6zn4YOKFdxj5ev-Q6NDoAiRzCBW1KMBwXfvSAqY3PGXZh4PMAHRCwpCdyrTNKw2p032m8lwsFIAJCx9ym2cLgKjXSRPihzymfTQTf9KNFn9gb1WSOCulwFjVc9L9wWrJ0M9c1LoHjN42NP7cDfXFy10n5LjRmzq_McONBcpsuULFbNtA6yH1BuqftR1Frcg-5CJu7W7nERvo191400NuwFI0lV2Lqt0bOHQh1tkEuzbUpzwrFhmFsAwj6RsTUnpCaJU1SNNzyYrXAMMIDeD-7N-JhqBNqo0FXynsF3SSVTN-pQwY8s9qnM4j3WP5uonJiWylz3P7EN2spHN7Xp6x8YeBzc3cpwb_mD54yo3YpPhqbmwvhduayHGRdg3LGXSLwi35HkZnOSnfZ4DfdKd-t0PXPIBn6m1p0VmCR589NpHXlOIvBduJdxNvaGGOk_fK1TL5PQ9ULnvr1RzdwncoYXeTk1cVeF2ZxkIAVt85C21GKa3FFsSeq20X9t1aCMm3RqcIUuFvg5tuasaTGgknYMWpMElpF1oYpdXS7MWI_tYf9n1Z2aiTkKUxL-2W0ufxi66TBjLaA8AODHT51Nk3_3YX-id1p-uSxE1dnBIef3LFYRNjp141S8lgi6suNdMN63ACBonQcgQE0SHSpy1kPXw_MTFCp46tHceXVyPId0JNwOYyajIm4Lqi-Jam2s_dbuJQOaNkHdgzSa2FiNB4m6amZ63cGMU2aCqjRpnsmRRdiJU4vmIqyWKdxByFSDFqDME8nheNkKRdhCFTWqrm_0XdfyviXDjn6d01XWR1aL0dhCzsldz5CnwKYyY60au6nL4-ecZN0dt4rxJnLwD8erXlfcmhL0pl4Vu6y_aeS3sRH-giSY2VtKdulZ6dakGvBza9DK4hBRJwD-E64huUnwhRHGWxU-540VBEMbZYMXq5uvOA7K876z987J5t4FOEAm-2xjidDtWU5XYc5r7Q2z007yzJZaY3HyWnfiBF3EWUtG71h8zdjr2UeuVvcXYh3xtQfy3_UAcvSXFV_PIQHipdqtJ_GYFD-UbOrCW_9awqQaP1t_cM96C2jsw2BV1PWF5eTwrluT6WTscfEEOHeXbrvXm.uP5d7bg2GosKw0kvjggASI9-tNWlDc_uA_Wm8pVviH4'
print(f"Access Token: {access_token}")

asyncio.run(clean_invalid_codes(file_path, access_token))
