from typing import Tuple

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import label
from sqlalchemy.types import DOUBLE_PRECISION
from geoalchemy2.types import Geometry

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER
from db import models


class TooManyResultsError(Exception):
    pass


class GeoQueries:
    def __init__(self):
        self.db_engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")
        self.session_maker = sessionmaker(bind=self.db_engine)

    def get_fields(self, query):
        if query.count() > 10000:
            raise TooManyResultsError

        result = {
            "type": "FeatureCollection",
            "features": []
        }
        for f in query.all():
            item = {
                "type": "Feature",
                "id": f.id,
                "geometry": f.geometry,
                "properties": {
                    "crop": f.crop,
                    "productivity_estimation": f.productivity,
                    "region_code": f.region,
                    "area_ha": f.area_ha,
                }
            }
            result["features"].append(item)

        return result

    def get_nearest(self, distance: int, point: Tuple[float, float]):
        with self.session_maker() as db_session:
            query = db_session.query(
                label("distance", func.ST_Distance(
                    func.ST_Transform(models.Fields.wkb_geometry, 3857),
                    func.ST_Transform(func.cast(f'SRID=4326;POINT({point[0]} {point[1]})', Geometry), 3857)
                )),
                func.ST_AsGeoJSON(models.Fields.wkb_geometry).label("geometry"),
                models.Fields.id,
                models.Fields.crop,
                models.Fields.productivity,
                func.cast(models.Fields.area_ha, DOUBLE_PRECISION).label("area_ha"),
                models.Fields.region
            ).filter(
                func.ST_Distance(
                    func.ST_Transform(models.Fields.wkb_geometry, 3857),
                    func.ST_Transform(func.cast(f'SRID=4326;POINT({point[0]} {point[1]})', Geometry), 3857)
                ) <= distance
            )

            return self.get_fields(query)

    def get_inside(self, geojson_geom: str):
        with self.session_maker() as db_session:
            query = db_session.query(
                func.ST_AsGeoJSON(models.Fields.wkb_geometry).label("geometry"),
                models.Fields.id,
                models.Fields.crop,
                models.Fields.productivity,
                func.cast(models.Fields.area_ha, DOUBLE_PRECISION).label("area_ha"),
                models.Fields.region
            ).filter(
                func.ST_Covers(
                    func.ST_Transform(func.cast(func.concat(
                        'SRID=4326;',
                        func.ST_AsText(func.ST_TRANSFORM(func.ST_GeomFromGeoJSON(geojson_geom), 4326), 3857)
                    ), Geometry), 3857),
                    func.ST_Transform(models.Fields.wkb_geometry, 3857)
                ).is_(True)
            )

            return self.get_fields(query)

    def get_intersect(self, geojson_geom: str):
        with self.session_maker() as db_session:
            query = db_session.query(
                func.ST_AsGeoJSON(models.Fields.wkb_geometry).label("geometry"),
                models.Fields.id,
                models.Fields.crop,
                models.Fields.productivity,
                func.cast(models.Fields.area_ha, DOUBLE_PRECISION).label("area_ha"),
                models.Fields.region
            ).filter(
                func.ST_Intersects(
                    func.ST_Transform(func.cast(func.concat(
                        'SRID=4326;',
                        func.ST_AsText(func.ST_TRANSFORM(func.ST_GeomFromGeoJSON(geojson_geom), 4326), 3857)
                    ), Geometry), 3857),
                    func.ST_Transform(models.Fields.wkb_geometry, 3857)
                ).is_(True)
            )

            return self.get_fields(query)

    def get_stat_by_region(self, region: str):
        with self.session_maker() as db_session:
            region_stat = db_session.query(
                func.sum(func.cast(models.Fields.area_ha, DOUBLE_PRECISION)).label("total_area"),
                func.sum(
                    models.Fields.productivity * func.cast(models.Fields.area_ha, DOUBLE_PRECISION)
                ).label("gross_yield"),
                label("wavg_yield",
                      func.sum(
                          models.Fields.productivity * func.cast(models.Fields.area_ha, DOUBLE_PRECISION)
                      ) / func.sum(func.cast(models.Fields.area_ha, DOUBLE_PRECISION)))
            ).filter(models.Fields.region == region).first()

        return region_stat._asdict()
