import itertools
import random
import os
from collections import defaultdict
def get_users(filenames):
    """
    This function takes the filenames and creates a dictionary of users and eyes 
    (left or right) of filenames, which makes it easier to create pairs
    """

    structured_data = defaultdict(lambda: defaultdict(list))
    print(f"Organizaing users for {len(filenames)} files")

    for file_path in filenames:
        user_id = os.path.basename(os.path.dirname(file_path))
        filename = os.path.basename(file_path)

        try:
            eye = filename.split('_')[1].split('.')[0]
            if eye in ['L', 'R']:
                structured_data[user_id][eye].append(file_path)

        except IndexError:
            continue
    return structured_data

def generate_genuine_pairs(structured_data):
    genuine_pairs = []
    for user_id, eyes in structured_data.items():
        for eye, images in eyes.items():
            if len(images) > 1:
                pairs = list(itertools.combinations(images, 2))
                genuine_pairs.extend(pairs)
    print(f"Generated - {len(genuine_pairs)} genuine pairs")
    return genuine_pairs

def generate_impostor_pairs(structured_data, num_impostor_pairs):
    impostor_pairs_set = set()
    user_ids = list(structured_data.keys())
    
    if len(user_ids)<2:
        print("Warning: Cannot create impostor pairs. Requires at least two users.")
        return []

    print(f"Generating {num_impostor_pairs} impostor pairs...")
    while len(impostor_pairs_set) < num_impostor_pairs:
        user1, user2 = random.sample(user_ids, 2)
        
        all_images_user1 = [img for eye, images in structured_data[user1].items() for img in images]
        all_images_user2 = [img for eye, images in structured_data[user2].items() for img in images]

        if all_images_user1 and all_images_user2:
            img1 = random.choice(all_images_user1)
            img2 = random.choice(all_images_user2)
            
            impostor_pairs_set.add(tuple(sorted((img1, img2))))
            
    return list(impostor_pairs_set)

def generate_pairs(structured_data, num = 2000):
    genuine_pairs = generate_genuine_pairs(structured_data)
    impostor_pairs = generate_impostor_pairs(structured_data, num)

    return genuine_pairs, impostor_pairs


def get_filenames(directory = '../datasets/IITD/'):
    # Return if root dir does not exist
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return []
    all_filenames = []

    for dirpath, dirnames, filenames in os.walk(directory):
        parent_dir_name = os.path.basename(os.path.dirname(dirpath))
        current_dir_name = os.path.basename(dirpath)

        if parent_dir_name == 'IITD' and current_dir_name.isdigit() and len(current_dir_name)== 3:
            for filename in filenames:
                if filename.endswith('.bmp'):
                    full_path = os.path.join(dirpath, filename)
                    all_filenames.append(full_path)
    
    return all_filenames



