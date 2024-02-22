from PIL import Image
import os

def crop_image(img, coordinate):
    coordinates = list(map(int, coordinate.strip().split(',')))
    x1, y1, x2, y2 = coordinates

    cropped_img = img.crop((x1, y1, x2, y2))
    return cropped_img

def crop_and_save_image(opt,frame_count):
    img_path = opt.input_folder_image + f"{frame_count}_img.png"
    with open(opt.input_coords, 'r') as f:
        coordinates_list = [line.strip() for line in f.readlines() if line.strip()]
    try:
        if opt.rgb:
            img = Image.open(img_path).convert('RGB')  # for color image
        else:
            img = Image.open(img_path).convert('L')

    except IOError:
        # make dummy image and dummy label for corrupted image.
        if opt.rgb:
            img = Image.new('RGB', (opt.imgW, opt.imgH))
        else:
            img = Image.new('L', (opt.imgW, opt.imgH))

    #img = Image.open(img_path)
    cropimg_list = []

    coor_len = len(coordinates_list)
    if(coor_len>4):
        filename = ["team1_name","team1_score","team2_name","team2_score","z_pitcher"]
    else:
        filename = ["team1_name","team1_score","team2_name","team2_score"]

    for idx, coordinate in enumerate(coordinates_list):
        tmp = crop_image(img,coordinate)
        cropimg_list.append(tmp)

        #Save the cropped image
        output_filename = f"{filename[idx]}.png"
        output_filepath = os.path.join(opt.cropimg_folder, output_filename)
        tmp.save(output_filepath)

    print("crop finish")
