import os
import shutil
import hashlib
import requests
import tempfile
import pandas as pd

from tqdm import tqdm
from urllib.request import urlopen, Request

class MMDB(object):
    def __init__(self, storage_path=None, server_address="http://127.0.0.1:6600/"):
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        self.storage_path = os.path.join(file_dir, "cache") if storage_path is None else storage_path
        self.server_address = server_address
        self.mmdb_info = self.get_mmdb_info(self.server_address)
            
    def list_dataset(self):
        return self.mmdb_info['ID'].tolist()

    def load_dataset(self, dataset_id):
        os.makedirs(self.storage_path, exist_ok=True)
        tmp_storage_path = os.path.join(self.storage_path, dataset_id + ".csv")
        if not os.path.exists(tmp_storage_path):
            print("Download dataset[{}]".format(dataset_id))
            self.download_url_to_file(self.server_address + "api/download/{}".format(dataset_id), tmp_storage_path)
        print("Load dataset[{}]".format(dataset_id))
        data = pd.read_csv(tmp_storage_path, header=0, index_col=0, encoding='unicode_escape')
        return data
    
    @staticmethod
    def get_mmdb_info(url):
        result = requests.get(url + "api/mmdb_info")
        assert result.status_code == 200, "Failed to connect to the server"
        return pd.DataFrame(result.json())[['ID', 'Species', 'Tissue', 'Disease', 'Technology', 'cell_num', 'protein_num', 'Title']]

    @staticmethod
    def download_url_to_file(url, dst, hash_prefix=None, progress=True):
        """ Borrowed from torchvision. Reference: https://pytorch.org/docs/stable/_modules/torch/hub.html#download_url_to_file """
        u = urlopen(Request(url, headers={"User-Agent": "python"})); u_meta = u.info()
        content_length = u_meta.getheaders("Content-Length") if hasattr(u_meta, 'getheaders') else u_meta.get_all("Content-Length")
        file_size = int(content_length[0]) if content_length is not None and len(content_length) > 0 else None

        dst = os.path.expanduser(dst) 
        temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(dst))
        try:
            sha256 = hashlib.sha256() if hash_prefix is not None else None
            with tqdm(total=file_size, disable=not progress, unit='B', unit_scale=True, unit_divisor=1024, ascii=True) as pbar:
                while True:
                    buffer = u.read(8192)
                    temp_file.write(buffer)
                    pbar.update(len(buffer))
                    if len(buffer) == 0: break
                    if hash_prefix is not None: sha256.update(buffer)
            temp_file.close()
            if hash_prefix is not None:
                digest = sha256.hexdigest()
                if digest[:len(hash_prefix)] != hash_prefix:
                    raise RuntimeError('invalid hash value (expected "{}", got "{}")'.format(hash_prefix, digest))
            shutil.move(temp_file.name, dst)
        finally:
            temp_file.close()
            if os.path.exists(temp_file.name):
                os.remove(temp_file.name)
