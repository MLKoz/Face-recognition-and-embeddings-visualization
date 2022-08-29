import cv2
from dialogs import AIModule


def getFacesFromVideoWithMtcnn(video_path, divider, confidence_arg, face_size):
    detector = AIModule.detector
    lista_twarzy = list()
    lista_prob = list()
    vid = cv2.VideoCapture(video_path)
    frames_number = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    fps_number = vid.get(cv2.CAP_PROP_FPS)
    if divider == 0:
        while True:
            ret, frame = vid.read()
            if not ret:
                break
            general_width = frame.shape[1]
            general_height = frame.shape[0]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detector.detect_faces(frame)
            if len(results) != 0:
                for x in range(len(results)):
                    if results[x]['confidence'] > float(confidence_arg)/100:
                        def getFaceFromImage(frame, results, position):
                            x1, y1, width, height = results[position]['box']
                            if x1 < 0:
                                x1 = 0
                            if y1 < 0:
                                y1 = 0
                            x2, y2 = x1 + width, y1 + height
                            face = frame[y1:y2, x1:x2]
                            return face
                        face = getFaceFromImage(frame, results, x)
                        if face.shape[1] > general_width * (face_size / 100) and\
                                face.shape[0] > general_height * (face_size / 100):
                            lista_twarzy.append(face)
                            lista_prob.append(int(results[x]['confidence'] * 100))
                            return lista_twarzy, lista_prob
    elif divider == 1:
        aktualna_klatka = 0
        skok = int(frames_number/fps_number)
        while True:
            ret, frame = vid.read()
            if not ret:
                break
            general_width = frame.shape[1]
            general_height = frame.shape[0]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detector.detect_faces(frame)
            if len(results) != 0:
                for x in range(len(results)):
                    if results[x]['confidence'] > float(confidence_arg)/100:
                        x1, y1, width, height = results[x]['box']
                        x1, y1 = abs(x1), abs(y1)
                        x2, y2 = x1 + width, y1 + height
                        face = frame[y1:y2, x1:x2]
                        if face.shape[1] > general_width*(face_size/100) and face.shape[0] > general_height*(face_size/100):
                            #print(face.shape)
                            lista_twarzy.append(face)
                            lista_prob.append(int(results[x]['confidence'] * 100))
            aktualna_klatka+=skok
            vid.set(1, aktualna_klatka)
    elif divider == 2:
        # opcja z 1 klatka = 1 sekunda
        aktualna_klatka = 0
        skok = int(frames_number / fps_number) / 5
        while True:
            ret, frame = vid.read()
            if not ret:
                break
            general_width = frame.shape[1]
            general_height = frame.shape[0]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = detector.detect_faces(frame)
            if len(results) != 0:
                for x in range(len(results)):
                    if results[x]['confidence'] > float(confidence_arg)/100:
                        x1, y1, width, height = results[x]['box']
                        x1, y1 = abs(x1), abs(y1)
                        x2, y2 = x1 + width, y1 + height
                        face = frame[y1:y2, x1:x2]
                        if face.shape[1] > general_width * (face_size / 100) and face.shape[0] > general_height * (
                                face_size / 100):
                            lista_twarzy.append(face)
                            lista_prob.append(int(results[x]['confidence'] * 100))
            aktualna_klatka += skok
            vid.set(1, aktualna_klatka)
    return lista_twarzy, lista_prob
