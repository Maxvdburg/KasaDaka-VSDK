#!/bin/bash
sox "forecast*" forecast.wav
sox "maximum_temp*" temperature.wav
sox "sun*" sun.wav
sox "wind*" wind.wav
