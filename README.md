# Email Service

###Problem:
This is one of the [Uber coding challenge] (https://github.com/uber/coding-challenge-tools/blob/master/coding_challenge.md) project.
Create a service that accepts the necessary information and sends emails. It should provide an abstraction between two different email service providers. If one of the services goes down, your service can quickly fail over to a different provider without affecting your customers.


###Solution:
I created a service that provides a form to allow users to specify the following information and once the user clicks on the submit button, the email will be sent to the recipient's email address.
* Sender's email address
* Recipient's email address
* CC email addresses
* Email subject
* Email message/content
* Attachment file

My email service is backed by Mailgun and Sendgrid. It always try to use Sendgrid first, and if it fails, it will try to use Mailgun to send the email.

[live site] (http://email.buyongqucai.com)

##Installation
* Install virtualenv if needed
* Install Python dependencies by running ```pip install -r requirements.txt``` from the root directory.
* Put the sendgrid API key, mailgun API key and the base API url into Development config in config.py file. 
You can get those by creating free account on [sendgrid](https://sendgrid.com/) and [mailgun](http://www.mailgun.com)
You could also set ENVVAR EMAIL_SERVICE_SETTINGS = /path/to/config to override default development config.

##Development
### Design
I implemented a abstract base class to define a interface for email providers. Each email provider is a subclass of the base class, and they all implement the ``` send ``` method. It's flexible to add more providers and add more methods in each provider.
However, I didn't implement a complex logic around how to choose which email provider to use and queue up the email sending tasks so that the distributed tasks could be executed asynchronously.
I think it's overkill for the purpose of this project and I don't have enough time to do that, but with the current design, it's flexible to do that.

###Technical Choices
####Server side

  * Python flask service. It is a light framework so I think it could be a good choice for making this small service.
  
####Client side
  * Created from through http://www.phpform.org/

### Run the Application

```sh
$ python manager.py runserver
```

Access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manager.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python manager.py test
```

With coverage:

```sh
$ python manager.py cov
```

##Usage
You can use the [live site](http://email.buyongqucai.com/)  or make a post to the ```/``` end point directly.

e.g.

```

import requests

message = {
    'to_email': 'lidayun71@gmail.com',
    'from_email': 'youremail@gmail.com',
    'subject': 'subject',
    'content': 'content to send'
    }

r = requests.post('http://email.buyongqucai.com/', message)
print r.message

# r is the result object that that contains status, status_code and message

```

* The email may not be sent immediately, it could be queued by Sendgrid or Mailgun
* If it successfully queued, the response will contain status code 200


###Future improvements
  * Beatify UI
  * Provide more features such as scheduling email delivery, multiple attachments, HTML/MIME content
  * Integrate with metrics API on email service to track how many emails are received/viewed/opened/ by recipients