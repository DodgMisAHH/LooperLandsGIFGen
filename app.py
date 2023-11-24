import sys
import os
import re
from PIL import Image
from multiprocessing import Pool
import time

# Asks user to input the paths and returns them
def get_user_input():
    while True:
        print('Welcome to the LooperLands GIF Generator!')
        print()
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

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

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

def create_gif_with_background(frames, bg_file, output_filename, frame_duration=100):
    # Load background image
    bg = Image.open(bg_file)

    # The order in which to use the frames based on specific actions
    order = ['side attack'] * 2 + ['side walk'] * 2 + ['side idle'] * 3 + \
            ['upward attack'] * 2 + ['upward walk'] * 2 + ['upward idle'] * 3 + \
            ['downward attack'] * 2 + ['downward walk'] * 2 + ['downward idle'] * 3
    
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
            ordered_frames.extend(frames[30:35])
        elif action == 'downward walk':
            ordered_frames.extend(frames[35:39])
        elif action == 'downward idle':
            ordered_frames.extend(frames[40:42])

    # Combine frames with the background image
    composite_frames = []
    for frame in ordered_frames:
        composite = Image.new('RGBA', bg.size)
        composite.paste(bg, (0, 0))
        x = (bg.width - frame.width) // 2
        y = (bg.height - frame.height) // 2
        composite.paste(frame, (x, y), frame)
        composite_frames.append(composite)

    # Save the ordered frames as a GIF
    output_path = os.path.join('output', f'{output_filename}.gif')
    composite_frames[0].save(
        output_path,
        save_all=True,
        append_images=composite_frames[1:],
        loop=0,
        duration=frame_duration
    )
    print(output_filename, 'finished!')


def process_sprite_sheet(sprite_file, sprite_sheet_folder):
    root, ext = os.path.splitext(sprite_file)
    if ext.lower() not in ['.png', '.jpg', '.jpeg']:
        print(f"File {sprite_file} has unsupported extension and will be skipped.")
        return None, None  # Updated this line to return a tuple
    gif_filename = root
    full_path = os.path.join(sprite_sheet_folder, sprite_file)
    frames = divide_sprite_sheet(full_path)
    frames = upscale_frames(frames)
    # Skipping the add background step, will be done later when creating the GIF
    return frames, gif_filename

if __name__ == '__main__':
    isExist = os.path.exists('output')
    if not isExist:
        os.makedirs('output')
    bg_file, sprite_sheet_folder = get_user_input()
    sprite_sheet_files = sorted(os.listdir(sprite_sheet_folder), key=natural_sort_key)

    # Start the timer
    time_start = time.time()

    # Create a pool of processes
    pool = Pool()

    # Use the pool to process the sprite sheet files in parallel
    results = pool.starmap(process_sprite_sheet, [(sprite_file, sprite_sheet_folder) for sprite_file in sprite_sheet_files]) 
    pool.close() 
    pool.join() 

    # Generate the GIFs with the background for processed frames
    for frames, gif_filename in results:
        if frames and gif_filename:  # Updated the condition to check for both values
            create_gif_with_background(frames, bg_file, gif_filename)

    # End the timer
    time_end = time.time() 

    # Calculate the elapsed time
    elapsed_time = time_end - time_start 
    processed_files_count = len([result for result in results if result[0]])
    average = elapsed_time / processed_files_count if processed_files_count else 0
    print()
    print(f'All sprites processed, please check your output folder!')
    if elapsed_time < 60:
        print(f'It took {int(elapsed_time)} seconds to process {processed_files_count} sprite sheets (avg. {average:.2f} each).')
    else:
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        print(f'It took {int(minutes)} minutes and {int(seconds)} seconds to process {processed_files_count} sprite sheets (avg. {average:.2f}s each).')