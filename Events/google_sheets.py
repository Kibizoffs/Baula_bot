import asyncio
import httpx
import os

from config import *

async def get_google_sheets():
    await asyncio.sleep(15 * 60) # после старта подождать 15 минут до цикла
    while True:
        db.cur.execute(f'SELECT {gr_key}, {baula_sal_key} FROM Groups WHERE {baula_sal_key} IS NOT NULL')
        res = db.cur.fetchall()

        for group in res:
            base_url = 'https://sheets.googleapis.com/v4/spreadsheets/'
            gr = group[0]
            spreadsheet_id = group[1]
            cell_range = 'Итоги'
            url = f'{base_url}{spreadsheet_id}/values/{cell_range}'
            params = {
                'key': os.getenv(env_key_googlesheets)
            }
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get(url, params=params)
                    if response.status_code != 200:
                        raise Exception
                except:
                    print("ERR: Didn't manage to fetch: ", url)
                    continue
                data = response.json()
                cell_data = data.get('values', [])
                for row in cell_data:
                    last_name = row[1].split()[0]
                    baula = row[9] if row[9] != '' else None
                    sal = row[8] if row[8] != '' else None
                    db.cur.execute(f'UPDATE Students SET {baula_key} = ?, {sal_key} = ? WHERE {gr_key} = ? AND {last_name_key} = ?', (baula, sal, gr, last_name))
        db.con.commit()

        await asyncio.sleep(60 * 60)
