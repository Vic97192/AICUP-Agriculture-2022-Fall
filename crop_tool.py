# Author: Lee Hsuan-Yi
from PIL import Image 
import csv,os,random

img_size = []

# Define the root directory where training images are stored
save_path = "C:\\AICUP"

# Define the root directory where training images are stored
train_root = "D:\\AI CUP\\train"

# Define the CSV file name that contains image annotations.
csvfile_name = 'tag_locCoor.csv'

log_name = 'log.txt'
img_path_list = os.listdir(train_root)
log = open(log_name,'w')

for individual_path in img_path_list:
    img_root = train_root+'\\'+ individual_path
    with open(csvfile_name, newline='') as csvfile: 
        rows = csv.reader(csvfile)
        next(rows,None)
        for row in rows:
            try:
                    img = Image.open(img_root+"\\"+row[1])           
                    width, height = img.size   # Size of the image in pixels (size of original image) 
                    img_size.append(int(width))
                    img_size.append(int(height))
                    img_size.sort()

                    # Define crop size as 35% of the smaller dimension
                    crop_size = img_size[0] * 0.35 
                    
                    x , y = width/2 + int(row[2]) , height/2 + int(row[3])    # Calculate crop center based on given annotation offsets
                    new_img = img.crop((x-crop_size, y-crop_size, x+crop_size, y+crop_size))

                    # Resize the cropped image to 480x480 pixels using high-quality LANCZOS resampling
                    new_img.resize((480,480),Image.LANCZOS)

                    # Randomly assign the image to either the training or validation set (90% train, 10% val)
                    key = random.randint(1, 100)
                    if key < 10:
                            save_root = save_path + "\\val" + "\\" + individual_path
                    else:
                            save_root = save_path + "\\train" + "\\" + individual_path

                    if os.path.isdir(save_root) == False:
                            os.mkdir(save_root)
                    
                    print("Saving: " + save_root + "\\" + row[1] + " from "+ img_root + "\\" + row[1])
                    log.write("Saving: " + save_root + "\\" + row[1] + " from "+ img_root + "\\" + row[1] + "\n")
                    log.flush()
                    new_img.save(save_root +"\\"+ row[1], quality = 95)

            except KeyboardInterrupt:
                print("Keyboard Interrupt Dectected.")
                exit()
            except FileNotFoundError:
                print(row[1] + " Not Found in: " + individual_path)
                log.write(row[1] + " Not Found in: " + individual_path + "\n")
                log.flush()

log.close()