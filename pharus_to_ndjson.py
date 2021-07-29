#!/bin/env python3

import json
import sys
import math

if len(sys.argv) != 2:
    print(f"Usage {sys.argv[0]} [input-file]")
    print("Hint: input-file is most likely something like recording3995161125.trk")
    sys.exit(1)

inputLines = ''
inputData = []

with open(sys.argv[1]) as f:
    inputLines = f.readlines()

previousTimestamp = 0
frame = -1
for line in inputLines:
    timestamp,pedestrian,x,y = line.split('|')
    timestamp = int(timestamp)
    pedestrian = int(pedestrian)
    x = float(x)
    y = float(y)
    if previousTimestamp != timestamp:
        previousTimestamp = timestamp
        frame +=1
    inputData.append([frame, timestamp, pedestrian, x, y])

# pedestrians = { row[1] for row in inputData }

pedestrians = {}

firstTimestamp = inputData[0][1]
lastTimestamp = inputData[len(inputData)-1][1]
fps = math.floor(frame / (lastTimestamp - firstTimestamp) * 1000) + 1

for row in inputData:
    if row[2] not in pedestrians:
        pedestrians[row[2]] = {
                'first': row[0],
                'last': row[0],
                'calc_end': 0,
                }
    else:
        pedestrians[row[2]]['last'] = row[0]
        pedestrians[row[2]]['duration'] = pedestrians[row[2]]['last'] - pedestrians[row[2]]['first']

chunkSize = min([pedestrian['duration'] for pedestrianId, pedestrian in pedestrians.items()])
chunkSize = 100
sceneId = 0

for pedestrianId, pedestrian in pedestrians.items():
    for x in range(pedestrian['first'], pedestrian['last'], chunkSize):
        if  x + chunkSize > pedestrian['last']:
            continue
        print(json.dumps({'scene': {
            'id': sceneId,
            'p': pedestrianId,
            's': x,
            'e': x + chunkSize,
            'real_end': pedestrian['last'] ,
            'real_first': pedestrian['first'],
            'fps': fps,
            'tag': [3, []],
            }}))
        sceneId += 1
        pedestrian['calc_end'] = x + chunkSize

for row in inputData:
    if row[0] > pedestrians[row[2]]['calc_end']:
        continue
    print(json.dumps({'track': {
        'f': row[0],
        'p': row[2],
        'x': row[3],
        'y': row[4],
        }}))
