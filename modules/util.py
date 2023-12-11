import subprocess
import platform
import re

# depending on what OS you are using,
# the operation for force opening a file (used for force opening the TOS file)
# is a bit different for each platform. Therefor this function will handle those differences to achieve the same result.
# Note: This application is not supported on MacOS by nature as I did not install macos and linux equivilant binaries. 
# If you want you can install those binaries and change the existing ones to get support on your preferred OS.
def open_file(file_path):
    if platform.system() == 'Darwin':  # macOS
        subprocess.run(['open', file_path])
    elif platform.system() == 'Windows':
        subprocess.run(['start', '', file_path], shell=True)
    elif platform.system() == 'Linux':
        subprocess.run(['xdg-open', file_path])

# the auction site titles are very long and messy
# it can be useful to have a stronger search pattern to find more specific content
# this function will scan the entire product tilte for specific keywords
def find_matches_in_text(text, *patterns):
    # escape special characters in each pattern
    escaped_patterns = [re.escape(pattern.lower()) for pattern in patterns]

    # create a regex pattern by joining the escaped patterns with '|'
    regex_pattern = '|'.join(escaped_patterns)

    # search for matches in the product title
    matches = re.findall(regex_pattern, text.lower(), flags=re.IGNORECASE)

    return matches

# builds a pretty dialog message to be used for dialog choice
def build_dialog_choice_str(title: str, options: [str]):
    message = title + "\n\n"
    for i in range(len(options)):
        message += f"{i + 1}. {options[i]}\n"
    message += "\nResponse: "
    return message