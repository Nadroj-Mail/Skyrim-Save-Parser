"""
    Made by Nadroj
    https://github.com/Nadroj-Mail
"""
import struct
import json

def parse_skyrim_save_to_json(ess_file_path, json_file_path):
    with open(ess_file_path, 'rb') as save_file:
        # Read the header
        save_file.read(27)  # Skips the header (To the point needed)
        
        # Read the player name (String)
        player_name = b""

        while True:
            name = save_file.read(1)

            if name == b"\x00": # checks the name till 'unknown' value is present
                break
            
            player_name += name # Concatinates the char to itself

        save_file.seek(save_file.tell() - 1) # Goes back a byte to allow the level to be pared in the next section
        player_name = player_name[:-1] # removes the last byte from end of the string (needed to remove the byte from the level interfeering)

        player_name = player_name.decode('utf-8') # Decodes it to readable Characters


        # Read the player level (int)
        save_file.read(1)  # Skipping unknown bytes

        save_file.seek(save_file.tell() - 2) # Seek back 2 bytes

        level = save_file.read(4) # Read the UInt32 binary
        player_level = int.from_bytes(level, byteorder="little", signed=False) # gets the intiger value of the byte (this case 32bit)        

        #Player Location (String)
        save_file.read(2) #skips unknown bytes
        player_location = b""

        while True:
            location = save_file.read(1)
            if location == b"\x00":
                break
            player_location += location
        player_location = player_location.decode("utf-8")

        if "\t" in player_location:
            player_location = player_location.replace("\t", "")

        # Save time (Int by nature, but String because, it's the same fecking thing in this context)
        file_save_time = b""

        while True:
            stime = save_file.read(1) # stime = save time
            if stime == b"\x00":
                break
            file_save_time += stime
        file_save_time = file_save_time.decode('utf-8')

        if "\u000b" in file_save_time:
            file_save_time = file_save_time.replace("\u000b", "") #clean up

        # Player Race (String)
        player_race = b""

        while True:
            race = save_file.read(1)
            if race == b"\x52": # Stops for uneeded Bytes
                break
            player_race += race
        player_race = player_race.decode("utf-8")

        # Player Sex (0 = Male, 1 = Female)
        save_file.read(3)

        sex = save_file.read(2)
        player_sex_int = int.from_bytes(sex, byteorder="little", signed=False)

        if player_sex_int == 0:
            player_sex = "Male" # sets it for male
        elif player_sex_int == 1:
            player_sex = "Female" # sets it for female

        # Required PlayerEXP needed to level up
        save_file.read(4)
        
        exp = save_file.read(4)
        print(exp)
        needed_exp = struct.unpack('<f', exp)[0]
        print(needed_exp)
        
        # Read the player gold (int)
        save_file.read(12)  # Skipping unknown bytes
        gold = struct.unpack('<f', save_file.read(4))[0]
        
        
        # Dictionary with the extracted data
        skyrim_data = {
            "general_player_stats": [
                {"player_name": player_name},
                {"player_race": player_race},
                {"player_level": player_level},
                {"player_sex": player_sex} # 0 = Male; 1 = Female
            ],
            "file_save_time": file_save_time, # Format Hours; Minutes; Seconds
            "player_location": player_location, # name of location
            "needed_exp": needed_exp,
            #"gold": gold
        }
        
        # Write the data to a JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(skyrim_data, json_file, indent=4)
        
        print(f"Skyrim save data parsed and saved to: {json_file_path}")

# File Paths
skyrim_ess_file = "PATH_TO_ESS_SAVE_FILE"
json_output_file = "SkyrimParseJson.json"

parse_skyrim_save_to_json(skyrim_ess_file, json_output_file)