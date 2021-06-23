import time
import numpy as np
import cv2
import ast
import os
import random

import config

# Sensor data size and creation of frame
mlx_shape = (24, 32)
frame = np.zeros((24 * 32,))

scale = config.scale

# Load the template
template = cv2.imread(config.template)
h, w, _ = template.shape


def td_to_image(f):
    """Convert thermals to an image.
       Edits to np array should be done here.
    """
    norm = np.uint8((f + 40) * 6.4)
    norm.shape = (24, 32)
    return norm


def process(frame, display=config.display, sensor=None):
    start_time = int(round(time.time() * 1000)) # Time in ms
    try:
        try:
            # convert binary string to list:
            frame = ast.literal_eval(frame.payload.decode('ascii'))
        except:
            # test frames will not get decoded:
            pass

        # Frame processing
        frame = np.fliplr(np.reshape(frame, mlx_shape))
        img = td_to_image(frame)

        # Image processing
        img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
        img = cv2.resize(img, (32 * scale, 24 * scale), interpolation=cv2.INTER_CUBIC)
        img = cv2.flip(img, 1)

        # Face detection
        res = cv2.matchTemplate(img, template, eval(config.method))
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # max_val being the accuracy of the face detection
        if max_val > 60000000:
            # draw rectangle around face
            top_left = max_loc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            cv2.rectangle(img, top_left, bottom_right, 255, 2)

            # draw circle around forehead
            forehead = (top_left[0] + int(w/2), top_left[1] + int(h/2) - 30)
            cv2.circle(img, forehead, 20, 255, 2)

            x, y = forehead
            
            # set the maximum (forehead) temperature in a 3x3 as reading
            fh_max = np.min(frame)
            for a in range(-1, 2):
                for b in range(-1, 2):
                    t = frame[y//scale+a][x//scale+b]
                    if t > fh_max:
                        fh_max = t
                        accuracy = max_val
            reading = fh_max
        else:
            reading = None
            accuracy = 0

        # ambient is simply np.mean for now
        ambient = np.mean(frame)

        # Display
        if reading == None:
            text = 'Forehead: None Ambient: {:.3f}'.format(ambient)
        else:
            text = 'Forehead: {:.3f} Ambient: {:.3f}'.format(reading, ambient)
        cv2.putText(img, text, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

        if display:
            cv2.imshow('MLX90640', img)

            # stop if escape key is pressed
            key = cv2.waitKey(30) & 0xff
            if key == 27:
                print('Exiting display')

    except KeyboardInterrupt:
        # terminate the cycle
        cv2.destroyAllWindows()
        print('Exiting display')
    cv2.destroyAllWindows()

    # duration is time between now and start in ms
    duration = int(round(time.time() * 1000)) - start_time

    # accuracy is a 0-100 int based on the max_val
    if accuracy != 0:
        accuracy = int(accuracy / 1000000 * 1.8 - 35)

    # add values to dictionary inside sensor dictionary
    for x in list(config.results[sensor].keys()):
        config.results[sensor][x].append(eval(x))

    # save the current image when the temperature is the highest in the batch
    try:
        if reading >= max(config.results[sensor]["reading"]):
            cv2.imwrite(os.path.join(config.path, sensor + ".jpg"), img)
    except TypeError:
        pass


def parse(sensor):
    results = config.results[sensor]

    detected = [x for x in results["reading"] if x != None]

    if len(detected) > 0:
        max_index = results["reading"].index(max(detected))
        accuracy = results["accuracy"][max_index]
    else:
        accuracy = 0
    
    ambient = round(sum(results["ambient"]) / len(results["ambient"]), 3)
    duration = sum(results["duration"]) / config.batch
    

    # trigger might change based on ambient
    trigger = config.standard_trigger

    # more than 3 frames with faces must be measured
    # otherwise reading = None and accuracy = 0.
    if len(detected) < 1:
        # no faces detected
        reading = None
        accuracy = 0
        result = 2
    elif len(detected) < 3:
        # object possibly too close or too far.
        reading = None
        accuracy = 0
        result = 3
    else:
        # detection successful, setting actual measurements
        if config.randomness:
            reading = round(max(detected) + random.uniform(-1, 6), 3)
        else:
            reading = round(max(detected), 3)

        if reading > trigger:
            result = 1
        else:
            result = 0

    # sample data: 47.434;19.432;892;37.1;90;1;
    # format: reading;ambient;duration;trigger;accuracy;result;
    return f'{reading};{ambient};{duration};{trigger};{accuracy};{result};'


def start(sensor, client=None, batch=config.batch, publish=config.publish):
    print(f"Thread for {sensor} has started.")
    if len(config.queue[sensor]) > 0:
        try:
            print(f"clients: {list(config.queue.keys())} are currently connected")

            # set batch results as empty values
            config.results[sensor] = {"reading": [], "ambient": [], "duration": [], "accuracy": []}

            # process every single frame until 'batch' size is reached, or after 5 seconds:
            sleep = 0
            while len(config.results[sensor]["reading"]) < batch:
                if len(config.queue[sensor]) > 0:
                    # process the first frame in the sensor's queue
                    process(config.queue[sensor][0], sensor=sensor)
                    # remove the first frame from the sensor queue
                    config.queue[sensor].pop(0)
                    sleep = 0
                else:
                    # Force after 5 seconds:
                    if sleep > 5:
                        break
                    time.sleep(1)
                    sleep += 1

            result = parse(sensor)

            publish_topic = config.topic_publish_reply.format(sensor)
            if publish:
                client.publish(publish_topic, str(result))
                print(f"Published to: {publish_topic}, result: {result}")
            else:
                config.reply_list += [result]
                print(f"Testing: {publish_topic}, result: {result}")
                
        except Exception as e:
            print("Thread start(): " + str(e))
    print(f"Thread for {sensor} has stopped.")
