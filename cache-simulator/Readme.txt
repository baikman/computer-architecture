To run, use the following command: gcc cache-simulator.c -o simulator && ./simulator

You will be prompted to either enter a 2 digit decimal address from 0-63 or press Ctrl + C to quit.

When an address is entered (as long as it is valid), there will either be a hit or miss. A miss will output "Cache miss." and add the data to the cache. When a hit occurs, "Cache hit!" followed by "Data at dd: xx" where dd is the decimal address and xx is the hex data.