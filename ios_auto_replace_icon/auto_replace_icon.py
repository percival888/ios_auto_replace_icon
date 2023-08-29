# import argparse
import config
import sys
import shutil
import json
import os
from PIL import Image

# 判断是否是png格式
def is_png_file(file_name):
    if file_name.endswith(".png"):
        return True
    else:
        return False

# 获取图片尺寸
def check_image_size_1024(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width == 1024 and height == 1024
    except IOError:
        print(f"无法打开或读取图像文件: {image_path}")
        return False

def resize_and_save_image(input_path, output_path, target_size):
    try:
        with Image.open(input_path) as img:
            # 获取图像原始尺寸
            original_width, original_height = img.size

            # 计算目标尺寸的缩放比例
            ratio = min(target_size[0] / original_width, target_size[1] / original_height)

            # 计算调整后的尺寸
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            # 调整图像尺寸
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # 保存处理后的图像到指定路径
            resized_img.save(output_path)

            # print(f"图片已成功压缩并保存至 {output_path}")

            return True

    except IOError:
        print(f"无法打开或读取图像文件: {input_path}")
        return False
    except Exception as e:
        print(f"处理图像时出现错误: {e}")
        return False


# 获取项目icons存放路径
targetAppIconAssetsXcassetsPath = config.target_assets_path + 'Assets.xcassets'
if not os.path.exists(targetAppIconAssetsXcassetsPath):
    targetAppIconAssetsXcassetsPath = config.target_assets_path + 'Images.xcassets'
    if not os.path.exists(targetAppIconAssetsXcassetsPath):
        print("error:查询xcassets文件夹路径失败")
        sys.exit(1)
targetAppIconAssetsPath = os.path.join(targetAppIconAssetsXcassetsPath, 'AppIcon.appiconset')

# 获取源图片路径
user_input_path = input("请输入源图片路径: ")
source_image_path = user_input_path.strip('"\'').replace(" ", "")

if is_png_file(source_image_path) == False:
    print("error:图片格式需为png")
    sys.exit(1)


if check_image_size_1024(source_image_path) == False:
    print("error:图片尺寸需要为1024*1024,请重新选择合适的图片资源")
    sys.exit(1)

newImagesJsonInfo = []

# iphone图片处理
for imageSizeInfo in config.iphone_image_size_info:
    targetImageSize = imageSizeInfo[0] * imageSizeInfo[1]
    targetImageSuffix = ".png" if imageSizeInfo[1] == 1 else "@{0}x.png".format(imageSizeInfo[1])
    targetIconName = '{0}-iphone{1}'.format(imageSizeInfo[0],targetImageSuffix)
    targetIconPath =  os.path.join(targetAppIconAssetsPath, targetIconName)
    if resize_and_save_image(source_image_path, targetIconPath, (targetImageSize,targetImageSize)) == False:
        print("error:图片压缩处理失败")
        sys.exit(1)
    else:
        newImagesJsonInfo.append({
            "size" : '{0}x{1}'.format(imageSizeInfo[0],imageSizeInfo[0]),
            "idiom" : "iphone",
            "filename" : targetIconName,
            "scale" : "{}x".format(imageSizeInfo[1]),
            })

# ipad图片处理
for imageSizeInfo in config.ipad_image_size_info:
    targetImageSize = imageSizeInfo[0] * imageSizeInfo[1]
    targetImageSuffix = ".png" if imageSizeInfo[1] == 1 else "@{0}x.png".format(imageSizeInfo[1])
    targetIconName = '{0}-ipad{1}'.format(imageSizeInfo[0],targetImageSuffix)
    targetIconPath = os.path.join(targetAppIconAssetsPath, targetIconName)
    if resize_and_save_image(source_image_path, targetIconPath, (targetImageSize,targetImageSize)) == False:
        print("error:图片压缩处理失败")
        sys.exit(1)
    else:
        newImagesJsonInfo.append({
            "size" : '{0}x{1}'.format(imageSizeInfo[0],imageSizeInfo[0]),
            "idiom" : "ipad",
            "filename" : targetIconName,
            "scale" : "{}x".format(imageSizeInfo[1]),
            })

#AppStore图片处理
shutil.copy(source_image_path, os.path.join(targetAppIconAssetsPath, 'AppStoreIcon.png'))
newImagesJsonInfo.append({
            "size" : '1024x1024',
            "idiom" : "ios-marketing",
            "filename" : 'AppStoreIcon.png',
            "scale" : "1x",
            })

#json配置文件修改
targetAppIconAssetsJsonPath = os.path.join(targetAppIconAssetsPath, "Contents.json")
with open(targetAppIconAssetsJsonPath, "r+") as file:
    contents = file.read()
jsonData = json.loads(contents)
jsonData['images'] = newImagesJsonInfo
modified_content = json.dumps(jsonData, indent=2)
with open(targetAppIconAssetsJsonPath, "w") as file:
    file.write(modified_content)

print("图片配置已完成")



# parser = argparse.ArgumentParser(description='命令行中传入源图片路径')
# #type是要传入的参数的数据类型  help是该参数的提示信息
# parser.add_argument('path', type=str, help='传入的图片路径')

# args = parser.parse_args()

# print('图片路径为:%s'%(args.path))













