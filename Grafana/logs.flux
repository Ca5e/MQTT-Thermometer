// Variable Sensor
import "influxdata/influxdb/schema"

schema.tagValues(
  bucket: "${organization}",
  tag: "sensor",
  predicate: (r) => true,
  start: -30d
)


// Variable Organization
buckets()
//  Custom regex to negate any values starting with _
//  ^(?!.*?^_).*


// Triggers exceeded map
//  Transformed using 'Labels to fields'

//  Query A
lng = from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/geo" and
    r._field == "lng" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()

lat = from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/geo" and
    r._field == "lat" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()

join(tables: {lng, lat}, on: ["_time", "_measurement", "sensor"])

//  Query B
from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "result" and
    r._value == 1 and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> count()



// Mean ambient temperature
//  Transformed using 'Series to rows'
from(bucket: "${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "ambient" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> aggregateWindow(
    every: 1m,
    fn: mean
  )



// Measurement logs
//  Transformed using 'Labels to fields'
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



// Last reading
from(bucket: "${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "reading" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()



// Status/online logs
//  Transformed using 'Labels to fields'
from(bucket:"${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> toString()



// Online sensor(s)
//  Transformed using 'Labels to fields' and 'Filter data by values' (exclude value false)

//  Query A
online = from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> toString()
  |> last()

mode = from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/mode" and
    r._field == "mode" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()

join(tables: {mode, online}, on: ["sensor"])

//  Query B
import "strings"

from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/online" and
    r._field == "online" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()
  |> toString()
  |> map(fn: (r) => ({
    r with
    duration:
      if r._value == "true" then string(v: duration(v: uint(v: now()) - uint(v: r._time)))
      else "offline"
    })
  )
  |> map(fn: (r) => ({
      r with
      duration: strings.splitAfter(v: r.duration, t: "s")[0]
    })
  )



// Last location data
//  Transformed using 'Labels to fields' and 'Merge'
lng = from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/geo" and
    r._field == "lng" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()

lat = from(bucket:"${organization}")
  |> range(start: -30d)
  |> filter(fn:(r) =>
    r._measurement == "status/geo" and
    r._field == "lat" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> last()

join(tables: {lng, lat}, on: ["_time", "_measurement", "_start", "_stop", "sensor"])



// Mean reply processing time
//  Transformed using 'Series to rows'
from(bucket: "${organization}")
  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
  |> filter(fn:(r) =>
    r._measurement == "reading/reply" and
    r._field == "duration" and
    contains(value: r.sensor, set: ${sensor:json})
  )
  |> aggregateWindow(
    every: 1m,
    fn: mean
  )
