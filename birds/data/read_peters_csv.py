import csv

from birds.models import Subspecies

CSV_NAME = '/Users/catherine/Public/biolodge/birds/data/peters.csv'
input_field_map = {'Order': 'order',
                   'Family': 'family',
                   'Genus': 'genus',
                   'Species': 'species',
                   'Subspecies': 'subspecies',
                   'Locations': 'raw_location',
                   'Common name': 'common_name'}


def csv_to_db():
    csv_name = CSV_NAME
    with open(csv_name) as fp:
        rdr = csv.DictReader(fp)
        for line in rdr:
            mapped_data = remap_field_names(line)
            Subspecies.objects.create(**mapped_data)


def remap_field_names(line):
    data = {}
    for key, val in line.items():
        mapped_key = input_field_map[key]
        data[mapped_key] = val
    return data


if __name__ == '__main__':
    csv_to_db()
