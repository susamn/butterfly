# Introduction
A declarative, dynamic and simple object mapper

## What is Butterfly
Butterfly is a declarative and dynamic object mapper tool built to do the object mapping seamless and easy. This tool is 
not suited to be used in an application needing high throughput as it does a lot of string a manipulation and lookups. The
real use for this library is where some dynamic behavior is needed in some app and some kind of dynamic object mapping is
required based on some mapping file.

## How does it work
The usage of butterfly is very easy. You have some date to work on and have a domain type which you need to map the data
into. Take the example data in the test data weather.json. The data looks like this:

```json
{
  "coord": {
    "lon": -0.13,
    "lat": 51.51
  },
  "weather": [
    {
      "id": 300,
      "main": "Drizzle",
      "description": "light intensity drizzle",
      "icon": "09d"
    }
  ],
  "base": "stations",
  "main": {
    "temp": 280.32,
    "pressure": 1012,
    "humidity": 81,
    "temp_min": 279.15,
    "temp_max": 281.15
  },
  "visibility": 10000,
  "wind": {
    "speed": 4.1,
    "deg": 80
  },
  "clouds": {
    "all": 90
  },
  "dt": 1485789600,
  "sys": {
    "type": 1,
    "id": 5091,
    "message": 0.0103,
    "country": "GB",
    "sunrise": 1485762037,
    "sunset": 1485794875
  },
  "id": 2643743,
  "name": "London",
  "cod": 200
}
```

and need to be mapped to a type looks like this (as some app needs the data in this format)

```json
{
	"weather": {
		"location": {
			"longitude": -0.13,
			"latitude": 51.51,
			"name": "London"
		},
		"temperature": 280.32,
		"pressure": 1012,
		"humidity": 81,
		"visibility": 10000,
		"wind": {
			"speed": 4.1,
			"degree": 80
		}
	},
	"data": [
		{
			"id": 300,
			"forcast": "light intensity drizzle"
		}
	]
}
```

For the above to achieve, here is the mapping file:

```json

{
  "coord": {
    "lon": "weather.location.longitude",
    "lat": "weather.location.latitude"
  },
  "weather": [
    {
      "id": "weather.data[].id",
      "description": "weather.data[].forcast"
    }
  ],
  "main": {
    "temp": "weather.temperature",
    "pressure": "weather.pressure",
    "humidity": "weather.humidity"
  },
  "visibility": "weather.visibility",
  "wind": {
    "speed": "weather.wind.speed",
    "deg": "weather.wind.degree"
  },
  "name": "weather.location.name"
}
```

As it can be seen the mapping file looks exactly the same like the actual data. This is because it is the data file, but
we have added the mapping keys of the type to which it needs to be mapped to. For the simple keys, it is evident how it 
is working and for the list types, we have to keep just one item in the list and have the mapping there. Butterfly will 
automatically create the list objects properly converted according to the mapping and the list will have the same number 
of items that the data file originally had.

Here in the example we have only one item, but it works for how many items it is there.

**Note** For list items, the mapping has to be correctly configured and the **[]** list operator has to be there in proper 
position according to the domain type.


## Usage

```python
from butterfly.engine import transform

result = transform("testdata/weather.json", "testdata/weather-mapping.json")
print(json.dumps(result))
```


