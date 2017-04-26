# cdc-kinesis-demo

This is a demo implementations in terms of stream-based Change Data Capture (CDC) for real-time data sync from MySQL Binlog. 
Please see below architecture for details. We are leveraging Maxwell's Daemon (in docker version) to capture MySQL binlog and ingest into Kinesis live stream. Then the backend lambda function will keep consuming the binlog (which was embedded in json format) and further sync into different data destinations. In this architecutre, we are using Kinesis Firehose to easily further copy changed data onto S3/Redshift. Note that the changed data is in the format of changed rows along with database update operations (like update, delete, insert, table creations and etc). You need to further merge the changed data residing in staging table into the destination table. Please refer to Amazon's documentation for details - http://docs.aws.amazon.com/redshift/latest/dg/t_updating-inserting-using-staging-tables-.html 

#Archiecture
![Architecture](https://cloud.githubusercontent.com/assets/23010188/25442856/bd7f8f92-2ad8-11e7-903f-36ec390a0056.png)

Reference:
====================
Maxwell's Daemon - http://maxwells-daemon.io/ 

