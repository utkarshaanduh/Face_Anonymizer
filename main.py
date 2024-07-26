import os.path
import argparse
import cv2
import mediapipe as mp


# Making Output Directory for Saving the Anonymous Image
output_dir = './output'
if not os.path.exists(output_dir):
 os.makedirs(output_dir)


def process_img(img, face_detection):
 H, W, _ = img.shape
 img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
 out = face_detection.process(img_rgb)

 if out.detections is not None:
  for detections in out.detections:
   location_data = detections.location_data
   bbox = location_data.relative_bounding_box
   x1, y1, w, h = bbox.xmin, bbox.ymin, bbox.width, bbox.height

   x1 = int(x1 * W)
   y1 = int(y1 * H)
   w = int(w * W)
   h = int(h * H)

   img[y1:y1+h, x1:x1+w,:] = cv2.blur(img[y1:y1+h, x1:x1+w,:],(55,50))
 return img


args = argparse.ArgumentParser()
args.add_argument("--mode", default = 'image')   # replace it's value for photo/video
args.add_argument("--filePath", default = "D:\Python folder\Face Anonymizer\Image\My Image.png")

args = args.parse_args()

# read image
img = cv2.imread("D:\Python folder\Face Anonymizer\Image\My Image.png")

# detect faces
mp_face_detection = mp.solutions.face_detection

with mp_face_detection.FaceDetection(min_detection_confidence=0.5, model_selection=0) as face_detection:

 if args.mode in ["image"]:
  img = cv2.imread(args.filePath)

  img = process_img(img, face_detection)

#saving image

  cv2.imwrite(os.path.join(output_dir, 'output.png'), img)

 elif args.mode in ['video']:

  cv2.VideoCapture(args.filePath)
  ret, farme = cap.read()

  output_video = cv2.VideoWriter(os.path.join(output_dir, 'output.mp4'), cv2.VideoWriter_fourcc(*'MPV4'),
                                 50,
                                 (frame.shape[1],
                                 frame.shape[0]))

  while ret:
   frame = process_img(frame, face_detection)

   output_video.write(frame)

   ret, frame = cap.read(0)

  cap.release()
  output_video.release()




