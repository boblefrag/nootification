# Nootification

Nootification is a notification system aiming to be robust, scalable
and easily maintainable.

The notification application sends alerts to users associated with
shops, based on their individual notification preferences.

## Preferences system

This part of the application let a user change their preferences about
alerting.

Those preferences are changed via a `PUT` on the `/preferences`
endpoint. The payload should be as follow :

```json

{
  "user_id": <USER_ID>,
  "level": <CRITICAL|STANDARD>
}

```

Selecting the STANDARD level allows users to receive all
notifications, while choosing CRITICAL limits notifications to only
critical alerts.

## WebHook and notifications framework

Alerts are received on the `POST /webhook/notifications` endpoint wich
validate and record the alert in the system.

The notifications to the enduser are managed using RQ (Redis Queue).

RQ is simple, easy to set up, and integrates well with Django.

However, if the number of users or the volume of notifications increases significantly,
a more scalable solution would be preferred, such as RabbitMQ or Kafka

## WorkFlow

### Receiving an alert

Alerts are received on `POST /webhooks/alerts/`

with a payload format like:

```json
{
  "url": "https://media.veesion.io/b36006d7-adfa-4f3c-a56c-addcb4e4f95d.mp4",
  "location": "fr-auchan-larochelle",
  "alert_uuid": "33cbb18c-3e9d-4acc-9667-2fbe7bf29137",
  "label": "theft",
  "time_spotted": 1742470260.083
}
```

When an alert is received it's validated and saved in DB. The `save`
method trigger the `publish` function from the `message` app. That
take care of creating the payload and send it to the revelant users.

### Creating the payload

the `publish` function is responsible of creating the payload and
sending a new task for each users.

- the `alerts` API is responsible for returning the Alert payload
- the `store` API is responsible for returning the revelant users

### Sending the notification to users

To ensure the users receive the notifications, the `send_notification`
function use `tenacity` wich is a retry framework. If we get an error
other than 4xx, we retry with a grace time of 3 seconds between each
atempts. In every case the reesult is logged with the correct level.

After 3 attempts, the systems stop trying and a log.error is issued


## Installation

You should first clone the repository with:

```
git clone git@github.com:boblefrag/nootification.git
```

Nootification use `poetry` as dependencies manager. To install all the
dependencies, once in the cloned repository,  run :

```bash
poetry install
```

### Run the tests

You can run the tests with :

```bash
cd nootification
coverage run manage.py test && coverage report
```

### Run the end to end tests

Nootification relies on 3 parts:

- The django application
- The redis queue
- A Flask service to answer messages

You'll need a functioning database configuration for PostgreSQL 
cf. https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-connection-settings

First install the initial data with :

```bash
cd nootification
./manage.py loaddata initial_data.json
```

to launch the django application run:

```bash
cd nootification
./manage.py runserver
```

In another terminal launch the redis queue with:

```bash
cd nootification
./manage.py rqworker default
```

Then launch the third party app to respond in another terminal:

```bash
python third_party.py
```

With another termainl (The last!)

```bash
python e2e.py
```

## Why is it reliabale ?

The system is tested both functionaly and end to end. To get
enterprise grade we should add strong monitoring on the queue system.

## Why is it Scalable ?

Both the Django application and the queue system can be distributed
amongst as many server as needed. In professional usage the Queue
system could be switched to something more robust than RQ.

## Exensibility


Sending a message use the `MessageSender` base class that allow to add
other senders to do so. If we wanted to add support for SMS and email
we should do the floowing:

- change `get_location_recipients` to return not only the `user_uuid`
  but also the `email`and `tel` field:
  
  ```python
  list(recipients.values('user_uuid', 'email', 'tel'))
  ```
- change `publish` to correctly fill the payload: 
 
 
 ```python
 for user in recipients:
    payload = {"target_user_uuid": str(user['user_uuid'])}
 ```

- call the correct backend depending on environment variable, settings
  or user preferences depending on the decision we choose.
