# PySpeckle
A Python Speckle Client

[Speckle.Works](https://www.speckle.works)

> Speckle: open digital infrastructure for designing, making and operating the built environment.
> We reimagine the design process from the Internet up: Speckle is an open source (MIT) initiative for developing an extensible Design & AEC data communication and collaboration platform.

## Installation
PySpeckle can be installed through `pip`:
`pip install speckle`

## Disclaimer
This code is very WIP and as such should be used with extreme caution, on non-sensitive projects.

## Description

PySpeckle is a light Python wrapper / interface for the Speckle framework. It can be used independently through Python scripts, or as a base for building various plug-ins, such as [SpeckleBlender](https://github.com/speckleworks/SpeckleBlender). 

At the moment, it copies the same method names from the .NET `SpeckleApiClient`, for consistency's sake. Although the functions are mostly labelled 'Async', they are not yet. This could eventually be implemented with `requests_futures` or `grequests` or similar.

## Notes
SpeckleBlender is written and sort of maintained by [Tom Svilans](http://tomsvilans.com) ([Github](https://github.com/tsvilans)).
