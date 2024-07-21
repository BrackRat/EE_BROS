import cv2


def get_line_position_from_img(img, draw_img=False, debug=False):
    """
    对二值化后的图片中间部分，上下20像素，寻找黑色色块的中心点，返回中心点坐标相对图片中心的偏移量，正数为右，负数为左。
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    if debug:
        cv2.imshow("binary", binary)
    # 提取图像中间部分
    middle_slice = binary[img.shape[0] // 2 - 20: img.shape[0] // 2 + 20, :]
    # 反色以提取黑色色块
    binary = cv2.bitwise_not(middle_slice)

    # 先侵蚀再膨胀，以去除噪点
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    binary = cv2.erode(binary, kernel, iterations=3)
    if debug:
        cv2.imshow("erode", binary)
    binary = cv2.dilate(binary, kernel, iterations=3)
    if debug:
        cv2.imshow("dilate", binary)



    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        if draw_img:
            return 0, img
        else:
            return 0

    center_points = []
    for contour in contours:
        M = cv2.moments(contour)
        if M["m00"] == 0:
            continue
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"]) + img.shape[0] // 2 - 20  # 调整Y坐标的偏移
        center_points.append((cX, cY))

    center_x = img.shape[1] // 2
    if not center_points:  # No valid center points found
        if draw_img:
            return 0, img
        else:
            return 0
    offset = center_points[0][0] - center_x

    if draw_img:
        # 画出检测区域框
        cv2.rectangle(img, (0, img.shape[0] // 2 - 20), (img.shape[1], img.shape[0] // 2 + 20), (0, 255, 0), 2)
        # 修正并画出黑色色块和中心点
        for contour in contours:
            contour[:, :, 1] += img.shape[0] // 2 - 20  # 对Y坐标进行全局偏移
        cv2.drawContours(img, contours, -1, (0, 0, 255), 2)
        cv2.circle(img, center_points[0], 3, (0, 255, 255), -1)
        # 写出偏移量，确保文本不会被绘制在图像外
        text_x = max(0, min(center_points[0][0] + 30, img.shape[1] - 100))
        text_y = max(30, min(center_points[0][1], img.shape[0] - 10))
        cv2.putText(img, f"Offset: {offset}", (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        return offset, img
    else:
        return offset



if __name__ == "__main__":
    # from logger_br import logger

    img = cv2.imread("assets/camera_low/ (12).jpg")
    # scale img to max 640
    if img.shape[1] > 640:
        img = cv2.resize(img, (640, int(640 / img.shape[1] * img.shape[0])))

    result, img = get_line_position_from_img(img, draw_img=True, debug=True)
    print(result)
    cv2.imshow("result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
