class Range(object):
    """
    Range of a subspecies as given in checklist range field.

    Examples:

    - Angola and Namibia east to northeastern South Africa

    - southern Somalia, south to eastern South Africa (western KwaZulu-Natal)

    - Senegambia to Ethiopia, Kenya and Uganda; Arabian Peninsula
    """

    def __init__(self, raw_text):
        self.raw_text = raw_text
        self.parsed = None
        self.regions = None

    def parse(self):
        regions = range_grammar.parse(self.raw_text)
        return regions

    def plot(self):
        for region in self.parse():
            map_widget.plot(region.get_polygon())


def save_range(subspecies):
    """
    Write subspecies range to db.
    """
    regions = Range(subspecies.raw_range).parse()
    for region in regions:
        region_model = RegionModel(
            name=region.name,
            polygon=region.get_polygon(),
        )
        region_model.save()
        if region.is_filled_region():
            region_model.filled_from.add(region.region_A)
            region_model.filled_from.add(region.region_B)
        subspecies.regions.add(region_model)  # adds a row to SubpeciesRegion join table


class Region(object):
    """
    A contiguous area on Earth.
    """
    def __init__(self, name):
        self.name = name

    def get_polygon(self):
        # map region name to a polygon, somehow
        return qgis.get_polygon(self.name)


class FilledRegion(Region):
    """
    A contiguous area on Earth defined by filling two Regions.

    E.g. "Pacific Coast East to the Rockies"
    """

    def __init__(self, region_A, region_B):
        assert isinstance(region_A, Region), isinstance(region_B, Region),
        self.region_A = region_A
        self.region_B = region_B

    def get_polygon(self):
        polygon_A = region_A.get_polygon()
        polygon_B = region_B.get_polygon()
        return combine_and_fill_polygon(polygon_A, polygon_B)
