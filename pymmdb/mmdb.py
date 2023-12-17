import os, shutil, hashlib, requests, tempfile, zipfile
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import pandas as pd
import scanpy as sc
from tqdm import tqdm
from urllib.request import urlopen, Request


class MMDB(object):
    def __init__(self, storage_path=None):
        self.server_address = "https://mmdb.piaqia.com/"
        self.package_path = os.path.split(os.path.realpath(__file__))[0]
        self.storage_path = os.path.join(self.package_path, "cache") if storage_path is None else storage_path
        self.mmdb_info = self.get_mmdb_info(self.server_address)
        os.makedirs(self.storage_path, exist_ok=True)
        
    def list_species(self):
        print("Species: ", ', '.join(self.mmdb_info['Species'].unique()))
    
    def list_tissue(self):
        print("Tissue: ", ', '.join(self.mmdb_info['Tissue'].unique()))
    
    def list_disease(self):
        print("Disease: ", ', '.join(self.mmdb_info['Disease'].unique()))
    
    def list_technology_type(self):
        print("Technology Type: ", ', '.join(self.mmdb_info['Technology_type'].unique()))
    
    def list_technology(self):
        print("Technology: ", ', '.join(self.mmdb_info['Technology'].unique()))
    
    def list_mmdb_info(self):
        print("MMDB Information: ")
        self.list_species()
        self.list_tissue()
        self.list_disease()
        self.list_technology()
        self.list_technology_type()
            
    def list_dataset(self, species=None, tissue=None, disease=None, technology_type=None):
        query = self.mmdb_info
        if species is not None: query = query[query['Species'] == species]
        if tissue is not None: query = query[query['Tissue'] == tissue]
        if disease is not None: query = query[query['Disease'] == disease]
        if technology_type is not None: query = query[query['Technology_type'] == technology_type]
        return query

    def load_dataset(self, dataset_id):
        dataset_storage_path = os.path.join(self.storage_path, dataset_id)
        if not os.path.exists(dataset_storage_path):
            print("Download dataset: [{}]".format(dataset_id))
            os.makedirs(dataset_storage_path, exist_ok=True)
            self.download_url_to_file(self.server_address + "api_dataset/{}".format(dataset_id), os.path.join(dataset_storage_path, dataset_id + ".zip"))
            with zipfile.ZipFile(os.path.join(dataset_storage_path, dataset_id + ".zip"), 'r') as zip_ref:
                zip_ref.extractall(dataset_storage_path)
                
        print("Load dataset: [{}]".format(dataset_id))
        dataset_type = self.mmdb_info[self.mmdb_info['ID'] == dataset_id]['Technology_type'].values[0]
        atac_data_file = os.path.join(dataset_storage_path, dataset_id + "_preprocessed_ACT.h5ad")
        rna_data_file = os.path.join(dataset_storage_path, dataset_id + "_preprocessed_RNA.h5ad")
        adt_data_file = os.path.join(dataset_storage_path, dataset_id + "_preprocessed_ADT.h5ad")
        if dataset_type == "ATAC_RNA":
            data = { "ATAC": sc.read_h5ad(atac_data_file), "RNA": sc.read_h5ad(rna_data_file) }
        if dataset_type == "ATAC_PROTEIN":
            data = { "ATAC": sc.read_h5ad(atac_data_file), "PROTEIN": sc.read_h5ad(adt_data_file) }
        if dataset_type == "RNA_PROTEIN":
            data = { "RNA": sc.read_h5ad(rna_data_file), "PROTEIN": sc.read_h5ad(adt_data_file) }
        if dataset_type == "ATAC_RNA_PROTEIN":
            data = { "ATAC": sc.read_h5ad(atac_data_file), "RNA": sc.read_h5ad(rna_data_file), "PROTEIN": sc.read_h5ad(adt_data_file) }
        return data
    
    @staticmethod
    def get_mmdb_info(url):
        result = requests.get(url + "api/mmdb_info")
        assert result.status_code == 200, "Failed to connect to the server"
        return pd.DataFrame(result.json())[['ID', 'Species', 'Tissue', 'Disease', 'Technology_type', 'Technology', 'Cell_num', 'Title']]

    @staticmethod
    def download_url_to_file(url, dst, hash_prefix=None, progress=True):
        """ Borrowed from torchvision. Reference: https://pytorch.org/docs/stable/_modules/torch/hub.html#download_url_to_file """
        u = urlopen(Request(url, headers={"User-Agent": "python"}))
        u_meta = u.info() # Get meta information
        content_length = u_meta.getheaders("Content-Length") if hasattr(u_meta, 'getheaders') else u_meta.get_all("Content-Length")
        file_size = int(content_length[0]) if content_length is not None and len(content_length) > 0 else None # Get file size in bytes (e.g. 1024 bytes = 1 KB)
        # print("Downloading: {} (size: {:.2f} MB)".format(url, file_size / 1024 / 1024))
        
        dst = os.path.expanduser(dst) # Expand user path if needed. (e.g. ~ -> /root)
        temp_file = tempfile.NamedTemporaryFile(delete=False, dir=os.path.dirname(dst)) # Create a temporary file
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
            os.remove(temp_file.name) if os.path.exists(temp_file.name) else None # Remove temporary file if exists
                
    def __repr__(self):
        return "MMDB(storage_path={}, server_address={})".format(self.storage_path, self.server_address)
    