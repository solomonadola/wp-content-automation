import os
import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def modify_json(template_json, name, about_title2, content, username, service_lines):
    modified_json = template_json.copy()

    # Update the values in the JSON
    modified_json["content"][0]["elements"][0]["elements"][0]["settings"]["name"] = name
    modified_json["content"][0]["elements"][0]["elements"][0]["settings"]["about_title2"] = about_title2
    modified_json["content"][0]["elements"][0]["elements"][0]["settings"]["content"] = content

    # Extract the part after the colon in the username line
    username_line = username.strip().split(":")
    print(username_line)
    if len(username_line) > 1:
        linkedin_username = username_line[1].strip()
        print(f"LinkedIn Username: {linkedin_username}")
        
        # Update the LinkedIn URL in the sc_option_list
        linkedin_url = f"https://www.linkedin.com/in/{linkedin_username}/"
        print(f"LinkedIn URL to be updated: {linkedin_url}")
        modified_json["content"][11]["elements"][0]["elements"][1]["elements"][0]["elements"][0]["settings"]["title"] = f"{name}"
        modified_json["content"][11]["elements"][0]["elements"][1]["elements"][0]["elements"][0]["settings"]["sub_title"] = f"{about_title2}"
        modified_json["content"][11]["elements"][0]["elements"][1]["elements"][0]["elements"][0]["settings"]["sc_option_list"][-1]["url"]["url"] = linkedin_url
        modified_json["content"][0]["elements"][0]["elements"][1]["elements"][0]["elements"][0]["settings"]["sc_option_list"][-1]["url"]["url"] = linkedin_url
    else:
        print("No valid username found. Skipping LinkedIn URL update.")

    # Update services_list with values from service_lines
    for i, line in enumerate(service_lines):
        parts = line.strip().split(":")
        if len(parts) >= 2:
            title = parts[0].strip()
            sub_title = parts[1].strip()
            modified_json["content"][2]["elements"][0]["elements"][1]["settings"]["services_list"][i]["title"] = title
            modified_json["content"][2]["elements"][0]["elements"][1]["settings"]["services_list"][i]["sub_title"] = sub_title

    return modified_json

def main():
    template_path = 'template.json'
    output_folder = 'outputs'
    data_folder = 'data'

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Load the template JSON
    template_json = load_json(template_path)

    # Process each text file in the data folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(data_folder, filename)

            # Read the content from the text file
            with open(file_path, 'r') as txt_file:
                lines = txt_file.readlines()
                name = lines[0].strip()
                about_title2 = lines[1].strip()
                content_start = lines.index('About Me:\n') + 1
                content_end = lines.index('What I Do:\n') if 'What I Do:\n' in lines else len(lines)
                content = ''.join(lines[content_start:content_end]).strip()
                username = lines[-1].strip()

                # Extract lines after "What I Do:" for services_list
                service_lines = lines[content_end + 1:-2]
                print(service_lines)

            # Modify the JSON
            modified_json = modify_json(template_json, name, about_title2, content, username, service_lines)

            # Save the modified JSON to the output folder
            output_filename = f"{name.replace(' ', '_')}.json"
            output_path = os.path.join(output_folder, output_filename)
            save_json(output_path, modified_json)

if __name__ == "__main__":
    main()
