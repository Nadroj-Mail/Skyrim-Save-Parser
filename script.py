import json
#from ssfp import SkyrimSaveFile

def Parse_Skyrim_Save_To_Json(ess_file_path, json_file_path):
    #save = SkyrimSaveFile(ess_file_path)
    with open(ess_file_path, 'rb') as ess_file:
        save_data = ess_file.read()

    skyrim_Data = {
        "PlayerName": "Van Gaaito",
        "level": 56,
        "gold": 23958
    }

    with open(json_file_path, 'w') as json_file:
        json.dump(skyrim_Data, json_file, indent=4)

    print(f"skyrim save data parsed and saved to: {json_file_path}")

skyrim_ess_file = "PATH-TO-YOUR-SAVE"
json_output_file = "SkyrimParseJason.json"

Parse_Skyrim_Save_To_Json(skyrim_ess_file, json_output_file)