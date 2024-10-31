import os


def generate_folder_structure(folder_path, indent=""):
    folder_structure = ""
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isdir(item_path):
            # 表示文件夹
            folder_structure += f"{indent}📁 {item}\n"
            folder_structure += generate_folder_structure(item_path, indent + "    ")
        else:
            # 表示文件
            folder_structure += f"{indent}📄 {item}\n"
    return folder_structure


# 使用示例
folder_path = r"E:\SEproject\Program\Frontend_total\SoftwareEngineer"  # 替换为你要扫描的文件夹路径
structure = generate_folder_structure(folder_path)
print(structure)
