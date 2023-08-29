import dxcam
import cv2
import easyocr
from load_dict import AnagramSolver
from PIL import Image

# INIT DXCAM
winname = "Test"
cam = dxcam.create(output_color="RGB")

# INIT ANAGRAM SOLVER
anagram_solver = AnagramSolver()
english_words = anagram_solver.load_words()

# INIT IMG
top_left_part_img = cv2.imread('assets/top_left_part.png')
top_right_part_img = cv2.imread('assets/top_right_part.png')

top_left_part_img_grey = cv2.cvtColor(top_left_part_img, cv2.COLOR_RGB2GRAY)
top_right_part_img_grey = cv2.cvtColor(top_right_part_img, cv2.COLOR_RGB2GRAY)

# INIT SIFT
sift = cv2.SIFT.create()

# INIT EASYOCR
reader = easyocr.Reader(['en'])

# FINDING KEYPOINTS AND DESCRIPTORS
kp_top_left, des_top_left = sift.detectAndCompute(top_left_part_img_grey, None)
kp_top_right, des_top_right = sift.detectAndCompute(top_right_part_img_grey, None)

# INIT FLANN
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)


# APPEND TO GOOD MATCHES IF M1 DISTANCE LESS THAN 20% OF MATCH2 DISTANCE
class CoreLogic:
    def find_best_matches(self, matches):
        good = []

        for match1, match2 in matches:
            if match1.distance < 0.75 * match2.distance:
                good.append(match1)

        return good

    # FINDING THE XY COORDINATE
    def find_xy(self, dmatch, kp_full):
        kp2_x, kp2_y = kp_full[dmatch.trainIdx].pt
        x, y = round(kp2_x), round(kp2_y)
        return x, y

    def main(self):
        available_words = set()
        cam.start(target_fps=30)

        full_img_grey = cv2.cvtColor(cam.get_latest_frame(), cv2.COLOR_RGB2GRAY)

        # FINDING KEYPOINTS AND DESCRIPTORS
        kp_full, des_full = sift.detectAndCompute(full_img_grey, None)

        # USING FLANN TO FIND MATCHES
        matches_top_left = flann.knnMatch(des_top_left, des_full, k=2)
        matches_top_right = flann.knnMatch(des_top_right, des_full, k=2)

        good_top_left = self.find_best_matches(matches_top_left)
        good_top_right = self.find_best_matches(matches_top_right)

        try:
            # FINDING XY COORD
            left, top = self.find_xy(good_top_left[-1], kp_full)
            top_right = self.find_xy(good_top_right[-1], kp_full)
            right, bottom = top_right[0], top_right[1] + (top_right[0] - left)

            # GRAB THE ROI
            result = cv2.cvtColor(cam.grab((left + 15, top + 15, right - 15, bottom - 15)), cv2.COLOR_RGB2GRAY)
            ret, result = cv2.threshold(result, 30, 255, cv2.THRESH_BINARY_INV)

            Image.fromarray(result).show()

            reader_result = reader.readtext(result, allowlist='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
            text = ''
            for arr in reader_result:
                text += arr[1]
            print(text)
            available_words = anagram_solver.solve_anagram(text.lower(), english_words=english_words)


        except:
            pass

        cam.stop()
        return available_words
