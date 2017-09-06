# Script For Creating Dummy records
## Related Files
* ./makeRecords.js
* ./makeRecords.json

## Description
This script can be used to create large batches of records in a DreamFactory connected database. This is useful for testing large API calls and creating data sets for demos.

## Details
The api needs to be called with the xrecords parameter to tell it how many records to create. It then gets the latest ID number from the database table and starts the counter at the next ID number. This allows you to use the increment counter for content, for example "Todo Item 506."
With that piece of information it then for loops to create the json for individual records and adds those to the master payload. After completing this loop the singular payload is POSTed to the db service. Record IDs are returned to the client.
The database table being used in the example in the script is a Todo list. The schema for this table is in resources/makeRecords.json. Each record contains an auto increment id, and name field that contains "Todo Item {increment number}", and a complete field, that is boolean. It's value is "randomly" assigned per record.
