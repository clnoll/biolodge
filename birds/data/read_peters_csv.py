import csv

from birds.models import Subspecies

CSV_NAME = '/Users/catherine/Public/biolodge_c/birds/data/peters.csv'
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
        while True:
            try:
                line = rdr.next()
                mapped_data = map_input_to_field(line)
                Subspecies.objects.create(**mapped_data)
            except StopIteration:
                return


def map_input_to_field(line):
    data = {}
    for key, val in line.items():
        mapped_key = input_field_map[key]
        data[mapped_key] = val
    return data


if __name__ == '__main__':
    csv_to_db()
    import ipdb; ipdb.set_trace()