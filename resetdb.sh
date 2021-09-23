#!/bin/sh

# A script to reset the database
# Use this when you make changes in the schema
# Fills the database with dummydata

cd schema
psql < cleardb.sql
psql < schema.sql
psql < dummydata.sql
cd ..