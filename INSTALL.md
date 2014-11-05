# Install FusionManager

We're assuming you're familiar with python virtual environment.

## Setup

The following is the basic procedure to setup the application:
```shell
$ git clone --verbose https://github.com/pabloripolles/FusionManager.git

$ virtualenv FusionManager

$ cd FusionManager
$ source bin/activate

(FusionManager) ... $ pip install python-gflags
(FusionManager) ... $ pip install google-api-python-client

(FusionManager) ... $ deactivate
$
```

## Run

The following is the basic procedure to run the application:
```shell
$ cd FusionManager
$ source bin/activate

(FusionManager) ... $ python manager.py <client_id> <client_secret>
```

On the default browser, FusionManager would like to: Manage your Fusion Tables
```shell
(FusionManager) ... $ deactivate
$
```


