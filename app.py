import sys
import os
from PIL import Image
from multiprocessing import Pool

# Asks user to input the paths and returns them
def get_user_input():
    while True:
        bg_file = input('Please enter the path to the background file: ')
        if not os.path.exists(bg_file):
            print("This path does not exist")
        else:
            break
    while True:
        sprite_sheet_folder = input('Please enter the path to the folder containing sprite sheet files: ')
        if not os.path.exists(sprite_sheet_folder):
            print("This path does not exist")
        else:
            break
    print('Processing your sprites, please wait...')
    return bg_file, sprite_sheet_folder

# Define a new function that takes a sprite sheet file as input                                                    
# and performs the frame division, upscaling, background addition, and GIF creation.                               
def process_sprite_sheet(sprite_file):                                                                             
    root, ext = os.path.splitext(sprite_file)                                                                      
    if ext.lower() not in ['.png', '.jpg', '.jpeg']:  # add or remove file types as needed                         
        return                                                                                                     
    gif_filename = root                                                                                            
    print(gif_filename,'processing...')                                                                            
    full_path = os.path.join(sprite_sheet_folder, sprite_file)                                                     
    frames = divide_sprite_sheet(full_path)                                                                        
    frames = upscale_frames(frames)                                                                                
    frames = add_background(frames, bg_file)                                                                          
    combine_frames(frames, gif_filename)                                                                           
    print(gif_filename,'finished!')  

def divide_sprite_sheet(sprite_sheet_file):
    sprite_sheet = Image.open(sprite_sheet_file)
    width, height = sprite_sheet.size                                       
    frame_width = width // 5                                                
    frame_height = height // 9                                              
    frames = []                                                             
    for i in range(height // frame_height):                                 
        for j in range(width // frame_width):                               
            left = j * frame_width                                          
            top = i * frame_height                                          
            right = (j + 1) * frame_width                                   
            bottom = (i + 1) * frame_height                                 
            frame = sprite_sheet.crop((left, top, right, bottom))           
            frames.append(frame)
    return frames 

def upscale_frames(frames):
    upscaled_frames = []
    for frame in frames:
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')   # ensure frame is in the right format
        upscaled_frame = frame.resize((512, 512), Image.NEAREST)
        upscaled_frames.append(upscaled_frame)
    return upscaled_frames

def add_background(frames, bg_file):
    bg = Image.open(bg_file)
    frames_with_bg = []
    for frame in frames:
        new_image = Image.new('RGBA', bg.size)
        new_image.paste(bg, (0, 0))
        x = (bg.width - frame.width) // 2
        y = (bg.height - frame.height) // 2
        new_image.paste(frame, (x, y), frame)
        frames_with_bg.append(new_image)
    return frames_with_bg

def combine_frames(frames, output_filename):
    order = ['side attack'] * 2 + ['side walk'] * 2 + ['side idle'] * 3 + ['upward attack'] * 2 + ['upward walk'] * 2 + ['upward idle'] * 3 + ['downward attack'] * 2 + ['downward walk'] * 2 + ['downward idle'] * 3
    ordered_frames = []
    for action in order:
        if action == 'side attack':
            ordered_frames.extend(frames[0:5])
        elif action == 'side walk':
            ordered_frames.extend(frames[5:9])
        elif action == 'side idle':
            ordered_frames.extend(frames[10:12])
        elif action == 'upward attack':
            ordered_frames.extend(frames[15:20])
        elif action == 'upward walk':
            ordered_frames.extend(frames[20:24])
        elif action == 'upward idle':
            ordered_frames.extend(frames[25:27])
        elif action == 'downward attack':
            ordered_frames.extend(frames[30:36])
        elif action == 'downward walk':
            ordered_frames.extend(frames[35:39])
        elif action == 'downward idle':
            ordered_frames.extend(frames[40:42])

        ordered_frames[0].save(os.path.join('output',f'{output_filename}.gif'), save_all=True, append_images=ordered_frames[0:], loop=0)


import os
from multiprocessing import Pool

def process_sprite_sheet(sprite_file):
    root, ext = os.path.splitext(sprite_file)
    if ext.lower() not in ['.png', '.jpg', '.jpeg']:
        return
    gif_filename = root
    print(gif_filename, 'processing...')
    full_path = os.path.join(sprite_sheet_folder, sprite_file)
    frames = divide_sprite_sheet(full_path)
    frames = upscale_frames(frames)
    frames = add_background(frames, bg_file)
    combine_frames(frames, gif_filename)
    print(gif_filename, 'finished!')


import os
from multiprocessing import Pool

def process_sprite_sheet(sprite_file, sprite_sheet_folder):
    root, ext = os.path.splitext(sprite_file)
    if ext.lower() not in ['.png', '.jpg', '.jpeg']:
        return
    gif_filename = root
    print(gif_filename, 'processing...')
    full_path = os.path.join(sprite_sheet_folder, sprite_file)
    frames = divide_sprite_sheet(full_path)
    frames = upscale_frames(frames)
    frames = add_background(frames, bg_file)
    combine_frames(frames, gif_filename)
    print(gif_filename, 'finished!')


import os
from multiprocessing import Pool

def process_sprite_sheet(sprite_file, sprite_sheet_folder, bg_file):
    root, ext = os.path.splitext(sprite_file)
    if ext.lower() not in ['.png', '.jpg', '.jpeg']:
        return
    gif_filename = root
    print(gif_filename, 'processing...')
    full_path = os.path.join(sprite_sheet_folder, sprite_file)
    frames = divide_sprite_sheet(full_path)
    frames = upscale_frames(frames)
    frames = add_background(frames, bg_file)
    combine_frames(frames, gif_filename)
    print(gif_filename, 'finished!')


import os
from multiprocessing import Pool

def process_sprite_sheet(sprite_file, sprite_sheet_folder, bg_file):
    root, ext = os.path.splitext(sprite_file)
    if ext.lower() not in ['.png', '.jpg', '.jpeg']:
        return
    gif_filename = root
    print(gif_filename, 'processing...')
    full_path = os.path.join(sprite_sheet_folder, sprite_file)
    frames = divide_sprite_sheet(full_path)
    frames = upscale_frames(frames)
    frames = add_background(frames, bg_file)
    combine_frames(frames, gif_filename)
    print(gif_filename, 'finished!')

if __name__ == '__main__':
    isExist = os.path.exists('output')
    if not isExist:
        os.makedirs('output')
    bg_file, sprite_sheet_folder = get_user_input()
    sprite_sheet_files = sorted(os.listdir(sprite_sheet_folder))

    # Create a pool of processes
    pool = Pool()

    # Use the pool to process the sprite sheet files in parallel
    pool.starmap(process_sprite_sheet, [(sprite_file, sprite_sheet_folder, bg_file) for sprite_file in sprite_sheet_files])

    print('All sprites processed, please check your output folder!')

    isExist = os.path.exists('output')
    if not isExist:
        os.makedirs('output')
    bg_file, sprite_sheet_folder = get_user_input()
    sprite_sheet_files = sorted(os.listdir(sprite_sheet_folder))

    # Create a pool of processes
    pool = Pool()

    # Use the pool to process the sprite sheet files in parallel
    pool.starmap(process_sprite_sheet, [(sprite_file, sprite_sheet_folder, bg_file) for sprite_file in sprite_sheet_files])

    print('All sprites processed, please check your output folder!')

    isExist = os.path.exists('output')
    if not isExist:
        os.makedirs('output')
    bg_file, sprite_sheet_folder = get_user_input()
    sprite_sheet_files = sorted(os.listdir(sprite_sheet_folder))

    # Create a pool of processes
    pool = Pool()

    # Use the pool to process the sprite sheet files in parallel
    pool.starmap(process_sprite_sheet, [(sprite_file, sprite_sheet_folder,bg_file) for sprite_file in sprite_sheet_files])

    print('All sprites processed, please check your output folder!')

    isExist = os.path.exists('output')
    if not isExist:
        os.makedirs('output')
    bg_file, sprite_sheet_folder = get_user_input()
    sprite_sheet_files = sorted(os.listdir(sprite_sheet_folder))

    # Create a pool of processes
    pool = Pool()

    # Use the pool to process the sprite sheet files in parallel
    pool.map(process_sprite_sheet, sprite_sheet_files)

    print('All sprites processed, please check your output folder!')
                                                                                         
    isExist = os.path.exists('output')                                                                             
    if not isExist:                                                                                                
        os.makedirs('output')                                                                                                                                                                                            
    bg_file, sprite_sheet_folder = get_user_input()                                                                                                                                                         
    sprite_sheet_files = sorted(os.listdir(sprite_sheet_folder))                                                           
                                                                                                                    
    # Create a pool of processes                                                                                   
    pool = Pool()                                                                                  
                                                                                                                    
    # Use the pool to process the sprite sheet files in parallel                                                   
    pool.map(process_sprite_sheet, sprite_sheet_files)                                                             
                                                                                                                    
    print('All sprites processed, please check your output folder!') 
