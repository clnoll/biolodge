import csv

from birds.models import Subspecies

CSV_NAME = '/Users/catherine/Public/biolodge/birds/data/eBird-Clements-v2015-integrated-checklist-August-2015.csv'
input_field_map = {'Order': 'order',
                   'Family': 'family',
                   'Range': 'raw_location',
                   'English name': 'common_name',
                   'SPECIES_CODE v2015': 'ebird_id'}


def csv_to_db():
    csv_name = CSV_NAME
    with open(csv_name) as fp:
        rdr = csv.DictReader(fp)
        for line in rdr:
            mapped_data = remap_field_names(line)
            Subspecies.objects.create(**mapped_data)


def remap_field_names(line):
    data = {}
    data['genus'], data['species'], data['subspecies'] = get_species_from_name(
        line['Scientific name'])
    for key, val in line.items():
        if key in input_field_map.keys():
            mapped_key = input_field_map[key]
            data[mapped_key] = val.decode(errors='ignore')
    return data


def get_species_from_name(scientific_name):
    names = scientific_name.split(' ')
    genus = names[0]
    species = names[1]
    if len(names) == 3:
        subspecies = names[2]
    else:
        subspecies = ''
    return genus, species, subspecies


if __name__ == '__main__':
    csv_to_db()
