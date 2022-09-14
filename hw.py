from email.mime import image
import cv2
import numpy as np
import easyocr

# predict text from image
def predict_text(img):
    reader = easyocr.Reader(['en'], gpu=False)
    result = reader.readtext(img)
    return result

# draw bounding box on image
def draw_box(img, result):
    for detection in result:
        top_left = tuple([int(val) for val in detection[0][0]])
        bottom_right = tuple([int(val) for val in detection[0][2]])
        text = detection[1]
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = cv2.rectangle(img, top_left, bottom_right,
                            color=(0, 255, 0), thickness=5)
        img = cv2.putText(img, text, top_left, font,
                          1, (0, 0, 0), 2, cv2.LINE_AA)
        # add percentage of confidence
        img = cv2.putText(img, '{:.2f}'.format(
            detection[2]*100) + '%', bottom_right, font, 1, (0, 0, 0), 2, cv2.LINE_AA)
        # show image where not white
        img = cv2.bitwise_not(img)
    return img

# render image with bounding box on image
def render_result(img, result):
    img = draw_box(img, result)
    # return image
    return img

if __name__ == "__main__":
    # hide warnings
    import warnings
    warnings.filterwarnings("ignore")

    image = cv2.imread('./samples/download.png', cv2.IMREAD_UNCHANGED)
    # make mask of where the transparent bits are
    trans_mask = image[:, :, 3] == 0
    # replace areas of transparency with white and not transparent
    image[trans_mask] = [255, 255, 255, 255]
    # new image without alpha channel...
    new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    result = predict_text(new_img)
    render_result(new_img, result)