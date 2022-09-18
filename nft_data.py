from docarray import DocumentArray, Document
from random import shuffle
import os
import json
from typing import Any, Dict, Optional
from dataclasses import dataclass, field
import multiprocessing as mp
from tqdm import tqdm

@dataclass
class DataPoint:
    # id: str
    text: Optional[str] = None
    image_path: Optional[str] = None
    content_type: str = 'image'
    label: str = ''
    split: str = 'none'
    tags: Dict[str, Any] = field(default_factory=lambda: {})
def _build_doc(datapoint: DataPoint) -> Document:
    # doc = Document(id=datapoint.id)
    doc = Document()
    if datapoint.content_type == 'image':
        doc.uri = datapoint.image_path
        doc.load_uri_to_image_tensor()
        doc.set_image_tensor_shape(IMAGE_SHAPE)
    else:
        doc.text = datapoint.text
    doc.tags = {'finetuner_label': datapoint.label, 'split': datapoint.split}
    doc.tags.update(datapoint.tags)
    doc.tags.update({'content_type': datapoint.content_type})
    return doc
def create_file_to_text_map(dict_list):
    file_to_text = {}
    for d in dict_list:
        meta = d['metadata']
        file = meta['image'].split('//')[-1]
        attributes = meta['attributes']
        values = [d['value'] for d in attributes]
        shuffle(values)
        text = ' '.join(values)
        file_to_text[file] = text.lower()
    return file_to_text
def build_nft(root: str, num_workers: int = 8) -> DocumentArray:
    """
    Build the nft dataset.
    Download the raw dataset from
    https://github.com/skogard/apebase
    :param root: the dataset root folder.
    :param num_workers: the number of parallel workers to use.
    :return: DocumentArray
    """
    f_labels = os.path.join(root, 'db')
    contentdir = os.path.join(root, 'ipfs')

    # read artists.csv
    with open(f_labels, 'r') as f:
        lines = f.readlines()
    dict_list = [json.loads(line) for line in lines]
    file_to_text = create_file_to_text_map(dict_list)

    data = []
    for file, text in file_to_text.items():
        data.append(DataPoint(id=file, image_path=f'{contentdir}/{file}', label=file))
        data.append(
            DataPoint(
                id=file + '_text',
                text=file_to_text[file],
                label=file,
                content_type='text',
            )
        )

    # build docs
    with mp.Pool(processes=num_workers) as pool:
        docs = list(tqdm(pool.imap(_build_doc, data)))

    return DocumentArray(docs)
build_nft("/Documents/apebase")