import time
from event_publisher import Publisher
import logging
import json


dispatcher = Publisher()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())

#
# @app.route("/")
# def index():
#     return "This is the Event generator.  To send an event to the stats " + \
#            "processor POST to the /events endpoint."


# this creates an endpoint, the body of this post request will be dispatched
# notice how dispatcher is an instance of Publisher
# @app.route("/events", methods=['POST'])
# def post_event():
#     message = request.get_json()
#     logger.debug("request had the following data: {0}".format(message))
#     dispatcher.push(message)
#     return json.dumps({'status': 'success'}), 200


if __name__ == '__main__':
    print("YOOOOYYOOOOOOOOOOOO")
    logging.info("Dispatching")
    dispatcher.run()
    # app.run(host='0.0.0.0', port=80, debug=True)
