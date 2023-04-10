from flask import Flask
from flask_restful import Resource, Api, reqparse
from werkzeug.exceptions import BadRequest

from geo_queries import GeoQueries, TooManyResultsError

app = Flask(__name__)
api = Api(app)


class Welcome(Resource):
    def get(self):
        return {'data': 'Welcome!'}


class GetNearest(Resource):
    """
    Get geometries which lay within given distance from  provided point (defined as lon/lat)

    Example: /nearest?lon=5.052151216702413&lat=47.31569840213254&distance=4000
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lon', type=float, location=['args', 'form'])
        parser.add_argument('lat', type=float, location=['args', 'form'])
        parser.add_argument('distance', type=str, location=['args', 'form'])
        args = parser.parse_args(strict=False)

        q = GeoQueries()
        try:
            fields = q.get_nearest(args.distance, (args.lon, args.lat))
        except TooManyResultsError:
            raise BadRequest("Response contains more than 10 000 items")
        return fields


class GetInside(Resource):
    """
    Get field geometries inside given one parallelogram (provided as geojson polygon).

    Example: /inside?geometry={"coordinates": [[[5.026712933712133, 47.347241255341146], [5.0385262948850595, 47.347241255341146], [5.042264700319691, 47.351496472825005], [5.030700566175682, 47.35169909367167], [5.026712933712133, 47.347241255341146]]], "type": "Polygon"}

    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('geometry', type=str, location=['args', 'form'])
        args = parser.parse_args(strict=False)

        q = GeoQueries()
        try:
            fields = q.get_inside(args.geometry)
        except TooManyResultsError:
            raise BadRequest("Response contains more than 10 000 items")
        return fields


class GetIntersect(Resource):
    """
    Get field geometries which intersect with given one (provided as geojson polygon).

    Example: /intersect?geometry={"coordinates": [[[5.035289535499118, 47.348837023862615], [5.035289535499118, 47.348582174958125], [5.0357668932713295, 47.348582174958125], [5.0357668932713295, 47.348837023862615], [5.035289535499118, 47.348837023862615]]], "type": "Polygon"}
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('geometry', type=str, location=['args', 'form'])
        args = parser.parse_args(strict=False)

        q = GeoQueries()
        try:
            fields = q.get_intersect(args.geometry)
        except TooManyResultsError:
            raise BadRequest("Response contains more than 10 000 items")
        return fields


class RegionStat(Resource):
    """
    Get the area, gross yield, and weighted average yield per hectare in a region.

    Example: /region_stat?region=FR-21
    """
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('region', type=str, location=['args', 'form'])
        args = parser.parse_args()

        q = GeoQueries()
        stat = q.get_stat_by_region(args.region)

        return stat


api.add_resource(Welcome, '/')
api.add_resource(GetNearest, '/nearest', endpoint='nearest')
api.add_resource(GetInside, '/inside', endpoint='inside')
api.add_resource(GetIntersect, '/intersect', endpoint='intersect')
api.add_resource(RegionStat, '/region_stat', endpoint='region_stat')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
