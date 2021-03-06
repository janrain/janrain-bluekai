# BlueKai

[![Build Status](https://travis-ci.org/janrain/janrain-bluekai.svg?branch=master)](https://travis-ci.org/janrain/janrain-bluekai)
[![Coverage Status](https://coveralls.io/repos/github/janrain/janrain-bluekai/badge.svg?branch=master)](https://coveralls.io/github/janrain/janrain-bluekai?branch=master)

BlueKai is a cloud-based big data platform that enables companies to personalize online, offline, and mobile marketing campaigns. The service provides an `/export` endpoint which when POSTed to instructs the service to transfer new records from Janrain to a BlueKai SFTP server in a TSV file format. An external service is then reposible for importing the TSV file into BlueKai. The intent is to have a time based service, such as a CRON job, trigger the export by POSTing to the `/export` endpoint. The service is designed to be deployed in an AWS Elastic Beanstalk Application and is configured via environment variables.

If problems arise during the process of pushing data into BlueKai you can look at the log file for visibility, open a Github Issue or contact Janrain Support (https://support.janrain.com).

## Configuration

The application reads its configuration from these environment variables:

- `DEBUG`: If this is set to anything other than empty string or the word
`FALSE`, then the app will run in debug mode. Additional info will be written
to the log.

- `JANRAIN_URI`: Hostname to use when making API calls to Capture.

- `JANRAIN_CLIENT_ID`: Janrain client Id.

- `JANRAIN_CLIENT_SECRET`: Secret for the client.

- `JANRAIN_SCHEMA_NAME`: Name of the Capture schema containing the user records.
(default: `user`)

- `JANRAIN_BATCH_SIZE_LIMIT`: Max number of records to retrieve from Janrain
at a time.
(default: `1000`)

- `JANRAIN_ATTRIBUTE_KEYS`: JSON list of schema attributes to export or a JSON dictionary of schema attribute mappings.

- `APP_LOG_FILE`: Full path to the file where the app will write the log.
(should only be used during local development, leave blank when deployed
to elastic beanstalk)

- `APP_LOG_FILESIZE`: Maximum size in bytes of the app log before it gets
rotated. (default: `10000000`)

- `APP_LOG_NUM_BACKUPS`: Number of rotated backups of the app log that will
be kept. (default: `20`)

- `AWS_DEFAULT_REGION`: AWS region the app runs in.

- `AWS_DYNAMODB_URL`: Url of the DynamoDB service to use.
(should only be used during local development, leave blank when deployed
to elastic beanstalk. [Requires having .aws/credentials file for local 
DynamoDB development](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html))

- `AWS_DYNAMODB_TABLE`: Name of the table in DynamoDB to use.

- `REMOTE_HOST`: Host name of the BlueKai SFTP Server.

- `REMOTE_PORT`: Port of the BlueKai SFTP Server.
(default: `22`)

- `REMOTE_USERNAME`: Username of the BlueKai SFTP Server.

- `REMOTE_PASSWORD`: Password of the BlueKai SFTP Server.

- `REMOTE_RSA_KEY`: RSA Private Key file of the BlueKai SFTP Server (Optional if using username and password)

- `BLUEKAI_PARTNERNAME`: BlueKai Partner Name.

- `BLUEKAI_CLIENTNAME`: BlueKai Client Name (Optional).

- `BLUEKAI_SITEID`: BlueKai SiteID.

- `SFTP_BUFFER_SIZE`: The size of the SFTP buffer.
(default: `32768`)

## Developement

### Get Source Code

* Clone from Github `git clone git@github.com:janrain/janrain-bluekai.git`

### Install Dependencies

* Create an Virtual Environment (Optional) `virtualenv -p python3 venv && source ./venv/bin/activate`
* Install dependencies `pip install -r requirements.txt`

### Run Application

* `./bin/run`

### Run Tests

* `./bin/test`
