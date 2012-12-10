# RSR Reverse
===

[RSR Reverse](http://github.com/cuzzo/rsr-reverse) stands for Rails-Syle Route Reverse.  It reverses Rails-style routes.

```bash
$ pip install rsr-reverse
```

## Introduction

Beside routing, one of the most basic needs of a web framework is to reverse routes--either for embedding in generated content or for server-side redirection.

## Example

Imagine you have a rails-style route: `/eg/{param1}/{param2}[/{option}[/{nested_option}]`.  Now, suppose that you'd like to reverse that route given a few sets of parameters.

### Example 1 (Routing 101)

| `Parameter Name` | `Parameter Value` |
| ---------------- | ----------------- |
| `param1`         | examples          |
| `param2`         | are               |
| `option`         | useful            |
| `nested_option`  | duh               |

Given the route `/eg/{param1}/{param2}[/{option}[/{nested_option}]` and the above parameters, the reversed URL would be: `/eg/examples/are/useful/duh`.

### Example 2 (Options)

The default for a Rails-style route is that an option is placed inside square brackets.  The example URL `/eg/{param1}/{param2}[/{option}[/{nested_option}]` has two options:

* `/{option}[/{nested_option}]`
* `/{nested_option}`

In order for an option to be replaced, all of it's parameters must be supplied.  So, `option` can be replaced independently of `nested_option`, but `nested_option` cannot be replaced unless `option` is supplied.

| `Parameter Name` | `Parameter Value` |
| ---------------- | ----------------- |
| `param1`         | examples          |
| `param2`         | are               |
| `option`         | useful            |

Given the route `/eg/{param1}/{param2}[/{option}[/{nested_option}]` and the above parameters, the reversed URL would be: `/eg/examples/are/useful`.

| `Parameter Name` | `Parameter Value` |
| ---------------- | ----------------- |
| `param1`         | examples          |
| `param2`         | are               |
| `nested_option`  | duh               |

Given the route `/eg/{param1}/{param2}[/{option}[/{nested_option}]` and the above parameters, the reversed URL would be: `/eg/examples/are`.

### Example 3 (Irreversible Routes)

It's possible that a route cannot be reversed given a set of parameters.  For example:

| `Parameter Name` | `Parameter Value` |
| ---------------- | ----------------- |
| `param1`         | examples          |
| `option`         | fun               |
| `nested_option`  | duh               |

Given the route `/eg/{param1}/{param2}[/{option}[/{nested_option}]` and the above parameters, the route cannot be reversed.  All parameters must be supplied in order for a route to be reversed.  Calling `RSRReverse::reverse` for this example would result in the exception `RouteParameterizationIrreversibleError` being raised.

## Pro Tips

### DRY Out Your Routes

It's an anti-pattern in programming to repeat a magic string.  Therefore, it's undesirable to define routes in more than one place; i.e., once for routing and then once (or in every place) that route is reversed.

For example, imagine you have a route: `/hello/{param}` that is mapped to a callback function `say_hello`.  To reverse that route, it's recommended to do something like:

```python
def reverse_by_callback_method(method, parameters):
    route = get_route(method)
    reverser = RSRReverser(route)
    url = reverser.reverse(parameters)
    return url


parameters = {
	'param': 'World',
}
url = reverse_by_callback_method(say_hello, parameters) # url -> '/hello/World'
```

Therefore, it's desirable to design applications with a structure that maps routes to functions so that it's possible to have some function `get_route` which can determine the route to a callback function.

### (You) Only Reverse Once

Imagine that you need to generate a list of 10,000,000 reversed URLs.  Imagine that all of these URLs are mapped to a particular route: `/mixna/{artist}/{song}[/{page}[/{date}[/comment}]]]`.

Let's imagine that for all 10,000,000 of these routes, we only have the required parameters: the `artist` name and the `song` name.

You could reverse all the routes like so:

```python
reverser = RSRReverser('/mixna/{artist}/{song}[/{page}[/{date}[/comment}]]]')
for record in song_database:
    parameters = {
        'artist': record.artist,
        'song': record.song,
    }
	print reverser.reverse(parameters)
```

However, we know in advance that we only have the `artist` and `song` for every record.  Therefore, it would be ideal to optimize the route down to `/mixna/{artist}/{song}` so that the substitutions would be faster.  Luckily, RSRReverser has just the method for you!

```python
reverser = RSRReverser('/mixna/{artist}/{song}[/{page}[/{date}[/comment}]]]')
optimized_route = reverser.prune_options({'artist': '', 'song': '',})
reverser.set_route(optimized_route)

for record in song_database:
    parameters = {
        'artist': record.artist,
        'song': record.song,
    }
	print reverser.reverse(parameters)
```

Why would you do this, you might ask?  Wouldn't it be easy to just optimize the route by hand, you might think?  Yes, it would.  But, it's much better to DRY out your routes and get them by the callback function (see Pro Tip #1).  A more accurate example would be:

```python
route = get_route(song_detail)
reverser = RSRReverser(route)
optimized_route = reverser.prune_options({'artist': '', 'song': '',})
reverser.set_route(optimized_route)

for record in song_database:
    parameters = {
        'artist': record.artist,
        'song': record.song,
    }
	print reverser.reverse(parameters)
```

This assumes that you've defined a function `get_route` that will get the route to a callback function (and you should).

## Tests

Run the tests.

```bash
~/rsr-reverse$ nosetests -w tests/
..................................................................................
----------------------------------------------------------------------
Ran 82 tests in 0.017s

OK
```

## License

RSR Reverse is available as an open source product under the BSD license.

Hack your heart out, hackers.

Copyright (c) 2012 Cuzzo Yahn.
