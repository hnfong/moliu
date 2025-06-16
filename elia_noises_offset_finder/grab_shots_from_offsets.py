import numpy as np
import moviepy
import PIL
import json
from ocrmac import ocrmac

# loading video gfg
clip = moviepy.VideoFileClip("video.mp4")

CROP_X = 236
CROP_Y = 668
CROP_W = 346
CROP_H = 78

with open("annotations.txt", "w") as out_file:
  with open("offsets.txt") as f:
    for line in f:
        t, t_human, _ = json.loads(line)

        # Video clips are the building blocks of longer videos. Technically, they are
        # clips with a clip.get_frame(t) method which outputs a HxWx3 numpy array
        # representing the frame of the clip at time t.
        frame_data_a = clip.get_frame(t + 5)
        frame_data_b = clip.get_frame(t + 10)
        frame_data_c = clip.get_frame(t + 15)

        # Use PIL to export a PNG. The timings are not always correct (probably
        # can be sped up by Elia pressing a button), so we have to sample a
        # couple different places.
        img_a = PIL.Image.fromarray(frame_data_a).crop((CROP_X, CROP_Y, CROP_X + CROP_W, CROP_Y + CROP_H))
        frame_png_a = f"frame-{t_human}a.png"
        img_a.save(frame_png_a)

        frame_png_b = f"frame-{t_human}b.png"
        img_b = PIL.Image.fromarray(frame_data_b).crop((CROP_X, CROP_Y, CROP_X + CROP_W, CROP_Y + CROP_H))
        img_b.save(frame_png_b)

        frame_png_c = f"frame-{t_human}c.png"
        img_c = PIL.Image.fromarray(frame_data_c).crop((CROP_X, CROP_Y, CROP_X + CROP_W, CROP_Y + CROP_H))
        img_c.save(frame_png_c)
        print(f"Saved to {frame_png_a}")

        image_paths = [frame_png_a, frame_png_b, frame_png_c]

        ocr_result = []
        for image_path in image_paths:
            annotations = ocrmac.OCR(image_path, recognition_level='accurate', language_preference=["en-US",]).recognize()
            print(annotations)
            if len(annotations) > 0:
                what = annotations[0][0]
                if what != "" and (len(ocr_result) == 0 or what != ocr_result[-1]):
                    ocr_result.append(what)

        out_file.write(f"{t_human} - {"/".join(ocr_result)}\n")
