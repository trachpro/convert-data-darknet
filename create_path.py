import os
import cv2

def create_text_path(path_to_folder, isTrain=True):
    folders = [os.path.join(path_to_folder, folder) for folder in os.listdir(path_to_folder)]

    name_file = "train.txt"
    if not isTrain:
        name_file = "val.txt"

    f = open(os.path.join('data', name_file), 'w+')

    for folder in folders:

        image_paths = [os.path.join(folder, image) for image in os.listdir(folder) ]
        for path in image_paths:
            f.write(path + '\n')
    
    f.close()

def create_data(path_to_file, data_type='train'):
    prefix = './WIDER_' + data_type + '/images'
    text_f = open(path_to_file, 'r')

    lines = text_f.readlines()

    i = 0

    while(i!=len(lines)):
        line = lines[i].replace('\n', '')
        folder_name = line.split('/')[0]
        os.makedirs(os.path.join(prefix.replace('/images','/labels'), folder_name), exist_ok=True)
        path_image = os.path.join(prefix, line)
        # print(path_image)
        image = cv2.imread(path_image, cv2.IMREAD_COLOR)
        h,w,_ = image.shape

        text_path = path_image.replace('.jpg','.txt')
        text_path = text_path.replace('/images', '/labels')
        data_f = open(text_path, 'w+')

        i += 1
        length = int(lines[i])
        if length == 0:
            length = 1

        for j in range(0,length):
            i += 1
            line = lines[i].strip()

            data_array = line.split(' ')
            # print(data_array)
            data_int = list(map(int, data_array))
            x = data_int[0]
            y = data_int[1]
            iw = data_int[2]
            ih = data_int[3]

            if x != 0 and y != 0:
                data_f.write('0 {} {} {} {}\n'.format(str(float(x)/w), str(float(y)/h), str(float(iw)/w), str(float(ih)/h)))
            else:
                print(line)
        
        data_f.close()
        i += 1


if __name__ == "__main__":
    # create_text_path('/home/tupm/data/wider_face/WIDER_val/images', False)
    create_data('./wider_face_split/wider_face_train_bbx_gt.txt', 'train')
    create_data('./wider_face_split/wider_face_val_bbx_gt.txt', 'val')
    # img = cv2.imread('./WIDER_train/images/0--Parade/0_Parade_marchingband_1_849.jpg')
    # print(img)
