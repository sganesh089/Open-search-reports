# Open-search-reports
Proof of concept

Currently there is no method to creating notification to users for reports from AWS opensearch tool. So as a proof concept, have created a lambda function to access opensearch and pull data using the index and then save the data to S3 and then send SNS notification to users with S3 URL.

For this code below are the python libraries used:
1. Aws-wrangler library to access opensearch and pull data with SQL queries.
2. Boto3 to upload file to S3 and send SNS notification.
