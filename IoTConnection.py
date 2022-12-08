from Adafruit_IO import *
from datetime import date

def Data_Collection_Pub_IoT(TestName, Value):
    ADAFRUIT_IO_USERNAME = "AutomateUCL"
    ADAFRUIT_IO_KEY = "aio_NDNb02B6OZ3wy6t3G4CXNQW8l9xK"

    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    group = aio.groups("spatialdatacollection")

    if "Spatial" in TestName:
        feedName = "spatialdatacollection" + ".datacollection"
    if "Speech" in TestName:
        feedName = "speechdatacollection" + ".datacollection"
    else:
        feedName = "default" + ".testing"
    
    try:
        feed = aio.feeds(feedName)
        print("Feed Already Exists")
        check = 1

    except:
        feed = aio.create_feed(Feed(name=feedName))
        print(print("Creating Feed"))
        check = 0

    Val = TestName + " " + Value

    aio.send_data(feed.key, Val)


def Data_Collection_Sub_IoT(TestName):
    ADAFRUIT_IO_USERNAME = "AutomateUCL"
    ADAFRUIT_IO_KEY = "aio_NDNb02B6OZ3wy6t3G4CXNQW8l9xK"

    aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    if "Spatial" in TestName:
        feedName = "spatialdatacollection" + ".datacollection"
    if "Speech" in TestName:
        feedName = "speechdatacollection" + ".datacollection"
    else:
        feedName = "default" + ".testing"

    data = aio.receive(feedName)

    print(data)

    data = data[3].split(" ")

    ExperimentName = data[0]
    print("Experiment Name : " + ExperimentName)
    for i in range(1,len(data)):
        print("{} degee" + chr(176) +"{}% Completed".format(data[i].split(":")[0], data[i].split(":")[1]))
    return data

# val = "30:10 30:10 0:100 60:0 90:0 120:0"

# Data_Collection_Pub(Value=val, TestName="Speech-30Deg-360-Test")