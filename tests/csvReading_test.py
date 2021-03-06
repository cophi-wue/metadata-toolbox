import pytest
import csv
import os
import sys
sys.path.append('..')
from metadata_toolbox import utils


def test_readFromCsv_wrong_delimiter(caplog):
    with open('test.csv', 'w') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(['Titel', 'Autor', 'Erscheinungsjahr', 'ISBN'])
        csvwriter.writerow(['Titel1', 'Autor1', 'Jahr1', 'ISBN1'])
        csvwriter.writerow(['Titel2', 'Autor2', 'Jahr2', 'ISBN2'])
    utils.readMetadataFromCsv("test.csv", delimiter='#')
    os.remove("test.csv")
    assert "CSV-File has only 1 column. Please check delimiter." in caplog.text

def test_readFromCsv_no_file():
    with pytest.raises(FileNotFoundError):
        utils.readMetadataFromCsv("test.csv")

def test_readFromCsv_empty_file(caplog):
    with open('test.csv', 'w') as file:
        csvwriter = csv.writer(file)
    utils.readMetadataFromCsv("test.csv")
    os.remove("test.csv")
    assert "CSV-File is empty." in caplog.text
