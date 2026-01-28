# purpose

set up logging using the Python Standard Library

# topics

- create log records with various levels

- format log records

- log to console

- log to jsonl file

- create a new log file each time the application is started

- delete oldest log files to prevent consuming too much storage

# definitions

[loggers](https://docs.python.org/3/library/logging.html#logger-objects)
are used to create log records

[log records](https://docs.python.org/3/library/logging.html#logrecord-objects)
capture information about an event

[log record attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)
store specific information about the event

[handlers](https://docs.python.org/3/library/logging.html#handler-objects)
manage where logs are sent to, for example:

- console

- log files

- email

[formatters](https://docs.python.org/3/library/logging.html#formatter-objects)
are used by handlers to format the log before sending it to its destination, for example:

- a brief line with few attributes for the console

- a csv with many attributes for a log file

- a json document for structured logs

[logging levels](https://docs.python.org/3/library/logging.html#logging-levels)
can be set to determine at which level and greater log records should be created or handled, for example:

- info and higher are logged to the console

- debug and higher are written to a file

- warning and higher are emailed

# logging

## loggers

- the ```getLogger()``` function is used to create and get loggers

    - loggers should never be instantiated from the ```Logger()``` class

    - ```getLogger()``` creates a logger if it doesn't exist and then returns it

- loggers are singleton

    - multiple calls to ```getLogger()``` with the same name and from any module will always call the same logger

        - ```getLogger()``` will not overwrite a logger

        - ```getLooger()``` will not create a logger with the same name for a different namespace

- the root logger is returned by calling ```getLogger()``` without an argument

    ```
    root_logger = logging.getLogger()
    ```

- a custom named logger is returned by passing in a name

    ```
    my_logger = logging.getLogger('my_logger')
    ```

- hierarchical loggers can be created using periods in the name

    ```
    child_logger = logging.getLogger('my_logger.child_logger')
    ```

## handlers

- loggers can have 0, 1, or many handlers

- the lastResort handler is used when no other handler is available

- the same handler can be used by different loggers

- log records propagate to the root

    - the current logger iterates up the hierarchy from the originating logger to and including the root logger

    - each logger's handlers will handle the log record

## formatters

- the same formatter can be used by many handlers

## how it all works
the [logging flow diagram](https://docs.python.org/3/howto/logging.html#logging-flow)
shows how it all works together
