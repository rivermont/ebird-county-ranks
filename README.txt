Simple Python script that creates a spreadsheet containing the rank of every species in every US county, from ebird.org.

A file (counties.json) was downloaded from the eBird API containing all county and county-equivalent regions in eBird (https://api.ebird.org/v2/ref/region/list/subnational2/US).

Then for every county, the eBird Target Species page was fetched, comparing birds in the region to an empty Antarctica life list (i.e. https://ebird.org/targets?r1=US-AK-020&r2=AQ).

The ranks are then saved to a csv file.
