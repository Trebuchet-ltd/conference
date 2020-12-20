import cv2

cap = cv2.VideoCapture('test.mp4')

OUTPUT_SIZE = (640, 480)

VIDEO_FORMAT_CODEC = {
    'mp4': 'mp4v',
    'avi': 'XVID'
}

OUTPUT_FORMAT = 'mp4'

fourcc = cv2.VideoWriter_fourcc(*VIDEO_FORMAT_CODEC[OUTPUT_FORMAT])
out = cv2.VideoWriter(f'output.{OUTPUT_FORMAT}', fourcc, 60, OUTPUT_SIZE)

# dims = []
# if cap.isOpened():
#     width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
#     height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
#     dims.append((width, height))
#
# print(dims)
while True:
    ret, frame = cap.read()
    if ret:
        b = cv2.resize(frame, OUTPUT_SIZE, fx=0, fy=0, interpolation=cv2.INTER_CUBIC)
        out.write(b)
    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
