#!/bin/bash

mongoimport --host mongodb --db testingdb --collection SomeCollection --type json --file mongo-seed/books50.json --jsonArray