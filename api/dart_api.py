import requests
import zipfile
import io
import xml.etree.ElementTree as ET
from config import DART_API_KEY
import pandas as pd

def call_open_dart_api_json(corp_code=None, bgn_de=None, end_de=None, last_reprt_at=None, pblntf_ty=None,
                            pblntf_detail_ty=None, corp_cls=None, sort='date', sort_mth='desc',
                            page_no='1', page_count='10'):
    url = 'https://opendart.fss.or.kr/api/list.json'
    params = {
        'crtfc_key': DART_API_KEY,
        'corp_code': corp_code,
        'bgn_de': bgn_de,
        'end_de': end_de,
        'last_reprt_at': last_reprt_at,
        'pblntf_ty': pblntf_ty,
        'pblntf_detail_ty': pblntf_detail_ty,
        'corp_cls': corp_cls,
        'sort': sort,
        'sort_mth': sort_mth,
        'page_no': page_no,
        'page_count': page_count
    }
    params = {key: value for key, value in params.items() if value is not None}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_corp_code(corp_name):
    url = 'https://opendart.fss.or.kr/api/corpCode.xml'
    params = {'crtfc_key': DART_API_KEY}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            xml_filename = zip_file.namelist()[0]
            with zip_file.open(xml_filename) as xml_file:
                tree = ET.parse(xml_file)
                root = tree.getroot()
                for corp in root.findall('list'):
                    name = corp.find('corp_name').text
                    corp_code = corp.find('corp_code').text
                    if name == corp_name:
                        return corp_code
        return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_financial_statement(crtfc_key, corp_code, bsns_year, reprt_code, fs_div):
    url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json'
    params = {
        'crtfc_key': crtfc_key,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code,
        'fs_div': fs_div
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_financial_data(corp_code, bsns_year, reprt_code, idx_cl_code):
    url = 'https://opendart.fss.or.kr/api/fnlttCmpnyIndx.json'
    params = {
        'crtfc_key': DART_API_KEY,
        'corp_code': corp_code,
        'bsns_year': bsns_year,
        'reprt_code': reprt_code,
        'idx_cl_code': idx_cl_code
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == '013':
        print(f"Error: {data['message']}")
        return []
    else:
        if 'list' in data:
            return [(item.get('idx_nm', '지표명 없음'), item.get('idx_val', '지표값 없음')) for item in data['list']]
        else:
            return []