import json
from pprint import pprint

from geo_queries import GeoQueries


def main():
    q = GeoQueries()

    # 1st task
    nearest = q.get_nearest(4000, (5.052151216702413, 47.31569840213254))
    pprint(nearest)

    # 2nd task
    geometry = {
        "coordinates": [
            [
                [
                    5.026712933712133,
                    47.347241255341146
                ],
                [
                    5.0385262948850595,
                    47.347241255341146
                ],
                [
                    5.042264700319691,
                    47.351496472825005
                ],
                [
                    5.030700566175682,
                    47.35169909367167
                ],
                [
                    5.026712933712133,
                    47.347241255341146
                ]
            ]
        ],
        "type": "Polygon"
    }

    fields = q.get_inside(json.dumps(geometry))
    pprint(fields)
    pprint([i['id'] for i in fields["features"]])

    # 3rd task
    geometry = {
        "coordinates": [
            [
                [
                    5.035289535499118,
                    47.348837023862615
                ],
                [
                    5.035289535499118,
                    47.348582174958125
                ],
                [
                    5.0357668932713295,
                    47.348582174958125
                ],
                [
                    5.0357668932713295,
                    47.348837023862615
                ],
                [
                    5.035289535499118,
                    47.348837023862615
                ]
            ]
        ],
        "type": "Polygon"
    }

    fields = q.get_intersect(json.dumps(geometry))
    pprint(fields)
    pprint([i['id'] for i in fields["features"]])

    # 4th task
    stat = q.get_stat_by_region("FR-21")
    pprint(stat)


if __name__ == "__main__":
    main()
