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

As nootification relies on 3 parts:

- The django application
- The redis queue
- A Flask service to answer messages

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

