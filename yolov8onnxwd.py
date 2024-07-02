try:
    import time
    from ultralytics import YOLO

    import cv2
    start_time = time.time()
    model = YOLO("hk2.onnx")
    results = model.predict(source="0",show=True)
    print(results)
except KeyboardInterrupt as e:
    #print(e,type(e))
    print("Halt")
    