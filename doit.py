import os
import requests


if __name__ == '__main__':
    elements_per_page = 100
    estações_convencionais_entries = 37638
    estações_convencionais_url = f'https://www.snirh.gov.br/hidroweb/rest/api/dadosHistoricos?size={elements_per_page}&page='
    dados_telemétricos_entries = 4653
    dados_telemétricos_url = f'https://www.snirh.gov.br/hidroweb/rest/api/estacaotelemetrica?size={elements_per_page}&page='

    download_prefix = 'https://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos='

    id_list = dict()
    for page in range(estações_convencionais_entries//elements_per_page):
        # target_file = f'conventional_data_{page}.zip'
        # if not os.path.exists(target_file):
        print(page)
        url = f'{estações_convencionais_url}{page}'
        contents = requests.get(url).json()
        id_list.update({
            entry['id']: (entry['longitude'], entry['latitude'])
            for entry in contents['content']})
        # break
        # download_url = (
        #     'https://www.snirh.gov.br/hidroweb/rest/api/documento/convencionais?tipo=2&documentos=' +
        #     ','.join([x for x in id_list]))

        # print(download_prefix)
        # result = requests.get(download_url)
        # print(result.status_code)
        # if not result.ok:
        #     print(f'error! {result}')
        #     break
        # print(f'downloading {target_file}')
        # with open(f'conventional_data_{page}.zip', 'wb') as fd:
        #     fd.write(result.content)
        # print(f'done with {target_file}')
    with open('coords.csv', 'w') as coords_file:
        for key in sorted(id_list):
            coords_file.write(
                f'{key},{id_list[key][0]},{id_list[key][1]}\n')