"""
Real Baltimore MTA station data: Light Rail + Metro SubwayLink.

Shared stations (Lexington Market, Shot Tower) use the same graph node,
creating transfer points between lines for interesting Dijkstra routing.
"""

from models.station import Station
from models.transit_network import TransitNetwork


# (name, capacity, line)
LIGHT_RAIL_STATIONS = [
    ("Hunt Valley", 200, "light_rail"),
    ("Pepper Road", 120, "light_rail"),
    ("McCormick Road", 100, "light_rail"),
    ("Gilroy Road", 80, "light_rail"),
    ("Lutherville", 150, "light_rail"),
    ("Falls Road", 180, "light_rail"),
    ("Mt Washington", 160, "light_rail"),
    ("Cold Spring Lane", 140, "light_rail"),
    ("Woodberry", 130, "light_rail"),
    ("North Avenue", 250, "light_rail"),
    ("Penn Station", 400, "light_rail"),
    ("University of Baltimore", 200, "light_rail"),
    ("Centre Street", 200, "light_rail"),
    ("Lexington Market", 350, "both"),        # shared with Metro
    ("Convention Center", 300, "light_rail"),
    ("Camden Yards", 500, "light_rail"),
    ("Hamburg Street", 180, "light_rail"),
    ("Westport", 120, "light_rail"),
    ("Cherry Hill", 150, "light_rail"),
    ("Patapsco", 130, "light_rail"),
    ("Linthicum", 120, "light_rail"),
    ("Ferndale", 100, "light_rail"),
    ("Cromwell / Glen Burnie", 160, "light_rail"),
    ("BWI Airport", 300, "light_rail"),
]

# (station_name_1, station_name_2, travel_time_minutes)
LIGHT_RAIL_CONNECTIONS = [
    ("Hunt Valley", "Pepper Road", 3),
    ("Pepper Road", "McCormick Road", 2),
    ("McCormick Road", "Gilroy Road", 2),
    ("Gilroy Road", "Lutherville", 3),
    ("Lutherville", "Falls Road", 2),
    ("Falls Road", "Mt Washington", 3),
    ("Mt Washington", "Cold Spring Lane", 2),
    ("Cold Spring Lane", "Woodberry", 2),
    ("Woodberry", "North Avenue", 3),
    ("North Avenue", "Penn Station", 2),
    ("Penn Station", "University of Baltimore", 2),
    ("University of Baltimore", "Centre Street", 2),
    ("Centre Street", "Lexington Market", 2),
    ("Lexington Market", "Convention Center", 2),
    ("Convention Center", "Camden Yards", 2),
    ("Camden Yards", "Hamburg Street", 2),
    ("Hamburg Street", "Westport", 3),
    ("Westport", "Cherry Hill", 2),
    ("Cherry Hill", "Patapsco", 3),
    ("Patapsco", "Linthicum", 2),
    ("Linthicum", "Ferndale", 2),
    ("Ferndale", "Cromwell / Glen Burnie", 3),
    # BWI spur branches from Linthicum
    ("Linthicum", "BWI Airport", 5),
]

METRO_STATIONS = [
    ("Owings Mills", 300, "metro"),
    ("Old Court", 200, "metro"),
    ("Milford Mill", 180, "metro"),
    ("Reisterstown Plaza", 220, "metro"),
    ("Rogers Avenue", 160, "metro"),
    ("West Cold Spring", 140, "metro"),
    ("Mondawmin", 250, "metro"),
    ("Penn North", 200, "metro"),
    ("Upton", 180, "metro"),
    ("State Center", 220, "metro"),
    # Lexington Market is shared (already in Light Rail list)
    ("Charles Center", 300, "metro"),
    ("Shot Tower", 220, "metro"),
    ("Johns Hopkins Hospital", 280, "metro"),
]

METRO_CONNECTIONS = [
    ("Owings Mills", "Old Court", 4),
    ("Old Court", "Milford Mill", 3),
    ("Milford Mill", "Reisterstown Plaza", 2),
    ("Reisterstown Plaza", "Rogers Avenue", 3),
    ("Rogers Avenue", "West Cold Spring", 2),
    ("West Cold Spring", "Mondawmin", 3),
    ("Mondawmin", "Penn North", 2),
    ("Penn North", "Upton", 2),
    ("Upton", "State Center", 2),
    ("State Center", "Lexington Market", 2),
    ("Lexington Market", "Charles Center", 2),
    ("Charles Center", "Shot Tower", 2),
    ("Shot Tower", "Johns Hopkins Hospital", 3),
]


def build_default_network() -> TransitNetwork:
    """
    Build the full Baltimore MTA transit network.
    Handles deduplication of shared stations by name.
    Returns a fully populated TransitNetwork.
    """
    network = TransitNetwork()
    name_to_station: dict[str, Station] = {}

    # Add all Light Rail stations
    for name, capacity, line in LIGHT_RAIL_STATIONS:
        station = Station(name=name, capacity=capacity, line=line)
        network._raw_add_station(station)
        name_to_station[name] = station

    # Add Metro stations (skip duplicates by name)
    for name, capacity, line in METRO_STATIONS:
        if name in name_to_station:
            # Shared station: update line to "both"
            name_to_station[name].line = "both"
        else:
            station = Station(name=name, capacity=capacity, line=line)
            network._raw_add_station(station)
            name_to_station[name] = station

    # Add Light Rail connections
    for name1, name2, weight in LIGHT_RAIL_CONNECTIONS:
        s1 = name_to_station[name1]
        s2 = name_to_station[name2]
        network._raw_add_connection(s1.station_id, s2.station_id, weight)

    # Add Metro connections
    for name1, name2, weight in METRO_CONNECTIONS:
        s1 = name_to_station[name1]
        s2 = name_to_station[name2]
        network._raw_add_connection(s1.station_id, s2.station_id, weight)

    # Clear undo stack (don't want initial data in undo history)
    network.undo_stack.clear()

    return network
