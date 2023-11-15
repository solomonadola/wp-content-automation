# Assuming 'template_data' is the variable containing the JSON data
# You need to navigate through the JSON structure to locate 'sc_option_list'

try:
    # Navigate to the relevant structure
    sc_option_list = (
        template_data["content"][0]["elements"][0]["elements"][0]["settings"]["sc_option_list"]
    )

    # Print or inspect 'sc_option_list'
    print(sc_option_list)

except KeyError:
    print("The structure of the JSON does not contain 'sc_option_list'.")
