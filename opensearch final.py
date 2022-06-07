import awswrangler as wr
import boto3 
import logging

## Opensearch link to access
host= 'https://search-testopen-g23sew4mxkqxpbkvm7mo5wkgoe.us-east-1.es.amazonaws.com/'
port=443 #change if port is not 443
username='testuser'
password= '######'

s3_client = boto3.resource('s3').meta.client


#s3 = boto3.client('s3')







def lambda_handler(event, context):
    
    os_connection = wr.opensearch.connect(host='https://search-testopen-g23sew4mxkqxpbkvm7mo5wkgoe.us-east-1.es.amazonaws.com/',
                                          port=port,
                                          username= username,
                                          password= password )
    
    ## saving as dataframe with the help of SQL queries
    df2 = wr.opensearch.search_by_sql(
                    client=os_connection,
                    sql_query='SELECT * FROM movies')
    ## saving to lambda default library for storing files.                    
    df2.to_csv('/tmp/sorted.csv', index=False)
    #print (df2)
    ## uploading to S3
    s3_client.upload_file('/tmp/sorted.csv', 'ganeshtestupload', '{}{}'.format('opensearch','.csv'))
        
    ##sending SNS notfication    
        #s3_client = boto3.resource('s3').meta.client
    s3 = boto3.resource('s3')
    sns = boto3.client('sns')
    bucket_name = s3.Bucket('ganeshtestupload')
    key = 'opensearch.csv'
    URL='https://ganeshtestupload.s3.amazonaws.com/opensearch.csv'
    uri='s3://ganeshtestupload/opensearch.csv'


    obj = list(bucket_name.objects.filter(Prefix=key)) 
    
    if obj:
        print ('file found')
        sns.publish(TopicArn='arn:aws:sns:us-east-1:878228182481:ganesh',Message= URL, Subject='report urilink:')
    
    else:
        print('file not found')
