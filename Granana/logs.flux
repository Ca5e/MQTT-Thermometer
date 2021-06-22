// sensor variable
import "influxdata/influxdb/schema"

schema.tagValues(
  bucket: v.bucket,
  tag: "sensor",
  predicate: (r) => true,
  start: v.timeRangeStart
)


// mean temperature
from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "ambient" and
    contains(value: r.sensor, set: ${sensor:json})
  )


// logs
reading = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "reading" and
    contains(value: r.sensor, set: ${sensor:json})
  )

accuracy = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "accuracy" and
    contains(value: r.sensor, set: ${sensor:json})
  )

ambient = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "ambient" and
    contains(value: r.sensor, set: ${sensor:json})
  )

duration = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "duration" and
    contains(value: r.sensor, set: ${sensor:json})
  )

result = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "result" and
    contains(value: r.sensor, set: ${sensor:json})
  )

trigger = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "trigger" and
    contains(value: r.sensor, set: ${sensor:json})
  )

union(tables: [ambient, reading, accuracy, duration, result, trigger])

// status/online logs
from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> map(fn: (r) => ({
    _time: r._time,
    _value: if r._value > 99.2 then true else false
  }))

// 
online = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> toString()
  |> last()

lng = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/geo" and
    r._field == "lng" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> toString()
  |> last()

lat = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/geo" and
    r._field == "lat" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> toString()
  |> last()

geo = join(tables: {lng, lat}, on: ["sensor"])

join(tables: {geo, online}, on: ["sensor"])


// online status difference
f = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    r._value == false and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()
  |> toString()

t = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    r._value == true and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()
  |> toString()

duration = from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()
  |> toString()
  |> map(fn: (r) => ({
    r with
    level:
      if r._value == "true" then now() - r._time
      else if r._value >= 85.0000001 and r._value <= 95.0 then "warning"
      else "normal"
    })
  )

union(tables: [t, f])


// Data verwijderen:
// .\influx delete --bucket 5Groningen --org Johma --start '2021-05-16T00:00:00Z' --stop '2021-05-18T00:00:00Z'
