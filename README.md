## Start

Put dataset into data/ folder before starting compose.

```commandline
docker-compose up
```

It will start postgis container, initialize db with fr subset data and start web app container.

## API

Provides 4 REST enpoints:

1. /nearest
 ```commandline
 localhost:5000/nearest?lon=5.052151216702413&lat=47.31569840213254&distance=4000
 ```
2. /inside
 ```commandline
 localhost:5000/inside?geometry={"coordinates": [[[5.026712933712133, 47.347241255341146], [5.0385262948850595, 47.347241255341146], [5.042264700319691, 47.351496472825005], [5.030700566175682, 47.35169909367167], [5.026712933712133, 47.347241255341146]]], "type": "Polygon"}
 ```
3. /intersect
 ```commandline
 localhost:5000/intersect?geometry={"coordinates": [[[5.035289535499118, 47.348837023862615], [5.035289535499118, 47.348582174958125], [5.0357668932713295, 47.348582174958125], [5.0357668932713295, 47.348837023862615], [5.035289535499118, 47.348837023862615]]], "type": "Polygon"}
 ```
4. /region_stat
 ```commandline
 localhost:5000/region_stat?region=FR-21
 ```

Accessed from browser at `localhost:5000`.

## Performance

In general possible performance improvements depends on data access patterns.

Possible options (at low level):
1. Add spatial indexes for geometry column (this already is done)
2. Add B-tree or other index for region column for `/region_stat` endpoint.

At high level:
1. Add partitioning by date/year for instance to store historical data separately from active one (what kind of history will be stored?). 
   Add partitioning by country if data accessed on country basis.
2. PostgreSQL configuration tuning as [described](https://postgis.net/docs/manual-3.0/performance_tips.html#database_tuning_configuration).
3. Use PostgreSQL sharding to store data accessed separately in different shards (horizontal scaling).
4. Store preaggregated data in separate tables or storage and recalculate it periodically using separate process.
5. Use caching. There is caching on DB level and additional layer of caching could be implemented in Redis.
6. Use replication: use read replicas of DB to access read-only copy of data decreasing load on main server.
