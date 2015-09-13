
# range_grammar.parse(raw_range)

# [
#     FilledRegion(
#         region_1=FilledRegion(region_1=Region(name="Angola"),
#                               region_2=Region(name="Namibia")),
#         region_2=Region(name="northeastern South Africa"),
#     ),
#     FilledRegion(region_1=Region(name="Mozambique"),
#                  region_2=Region(name="Kenya")),
#     Region(name="Uganda"),
# ]


# range = [habitat preposition] areas

# habitat = Montane forests | coastal areas | ...

# areas = area conjunction [area conjunction ...]

# conjunction = , | and

# area = [compass_direction] location


# compass_direction = n | e | s | w | north | east | south | west

# compass_adjective = n | e | s | w | northern | eastern | southern | western | northeastern | northwestern | southeastern | southwestern

# fill_operation = (compass_direction ("to" | "from")) | "to"


# range = location_set [fill_operation location_set]


from pyparsing import Word, alphas


# plot(parsed_range)

# find_species(polygon, parsed_regions)


def parse(range_text):
    # Output list of non-overlapping Region instances (either Regions or FilledRegions)
    pass


# EasternBorneo
# CaliforniaEastToRockies
    

# # "Angola and Namibia east to northeastern South Africa"
# region_1 = FilledRegion(Angola, Namibia)  # assert that they are adjacent!
# region_2 = Region(northeastern South Africa)
# return FilledRegion(region_1, region_2)






