import os
import cv2
import glob
import shutil


class DatasetManager:
    def __init__(self, path):
        self.path = path

    def get_images_from_directories(self):
        images = []
        for name in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, name)):
                images.extend(glob.glob(os.path.join(self.path, name, '*.[jJ][pP][gG]')))
                images.extend(glob.glob(os.path.join(self.path, name, '*.[pP][nN][gG]')))
        return images


class ImageFilter:
    def __init__(self, images):
        self.images = images
        self.index = self.load_index()

    def load_index(self):
        if os.path.exists('index.txt'):
            with open('index.txt', 'r') as f:
                return int(f.read())
        else:
            return 0

    def save_index(self):
        with open('index.txt', 'w') as f:
            f.write(str(self.index))

    def show_image(self):
        if self.index < len(self.images):
            img = cv2.imread(self.images[self.index])
            cv2.imshow('Image', img)


    def delete_image(self):
        if self.index < len(self.images):
            target_dir = 'deleted_images'
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            # 获取原始文件名
            original_filename = os.path.basename(self.images[self.index])
            # 获取所在的文件夹名
            directory_name = os.path.basename(os.path.dirname(self.images[self.index]))
            # 创建新的文件名
            new_filename = directory_name + '_' + original_filename
            # 创建目标路径
            target_path = os.path.join(target_dir, new_filename)
            # 移动文件
            shutil.move(self.images[self.index], target_path)
            del self.images[self.index]
            self.show_image()

    def start(self):
        self.show_image()
        while True:
            key = cv2.waitKey(0)
            if key == ord('d'):
                self.index += 1
                self.show_image()
            elif key == ord('a'):
                self.index -= 1
                self.show_image()
            elif key == ord('r'):
                self.delete_image()
            elif key == ord('q'):
                self.save_index()
                print(f"Current directory: {os.path.dirname(self.images[self.index])}")
                break
        cv2.destroyAllWindows()


def main():
    # 使用方法
    manager = DatasetManager('dataset')
    images = manager.get_images_from_directories()
    image_filter = ImageFilter(images)
    image_filter.start()


if __name__ == '__main__':
    main()
