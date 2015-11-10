************************************************************
*                                                          *
*                Hash Map Spell Checking                   *
*                   By Nick Chapman                        *
*              nlc35 at georgetown dot edu                 *
*                 Last Modified 11/09/15                   *
*                                                          *
************************************************************

Finds spelling errors in a text file

----------------------------------
		Running the program
----------------------------------
usage: hashing.py [-h] text_file dict_file [personal_dict]

positional arguments:
  text_file      Text file to check
  dict_file      Dictionary file to check against
  personal_dict  A personal dictionary file (optional)

optional arguments:
  -h, --help     show this help message and exit

----------------------------------
		Implementation
----------------------------------
The hash map is implemented using a list of HashNodes which contain key value pairs
The hashing algorithm itself implements the Fowler-Noll-Vo alternative algorithm in 64 bits
For collisions the table uses linear probing for resolution

----------------------------------
		Knowledge Gained
----------------------------------
 - Hashing
	- FNV1a_64
 - Hash tables/maps
 - Collision resolution, specifically linear probing
	- Chaining was experimented with but is not featured
 - Hash table load factor




 This project was created for Georgetown's COSC-160: Data Structures, Fall 2015