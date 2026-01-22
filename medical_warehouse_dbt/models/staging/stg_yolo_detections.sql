SELECT *
FROM {{ source('raw', 'yolo_detections') }}
