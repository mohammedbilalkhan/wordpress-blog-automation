# Wordpress Blog Comment Automation

Automate the process of posting comments on WordPress blogs with this script. The script is designed to follow a specific flow for commenting on articles from various WordPress blogs. 

## Features

- **Input Fields**: The script requires four input fields for each comment: name, email, website, and comment. Make sure to fill in all the fields correctly to personalize your comments.
  
- **Dynamic Commenting**: Specify the number of pages you want to comment on for each website. The script will navigate through the specified number of pages and post comments.

- **CSV Configuration**: Manage your target WordPress blogs through a 'sites.csv' file. Add the homepage links of the websites you want to comment on. The script will follow the same flow for all specified websites.

- **User Interface**: The script provides a simple user interface with a "Run" button to start the commenting process. You can also use the "Clear" button to reset all the input fields.

- **Browser Automation**: The script uses the undetected_chromebrowser library to run a Chrome browser. This is necessary as some WordPress blogs have reCAPTCHA on their pages. 

- **Profile Configuration**: You have the option to use your default Chrome profile. Uncomment the line under 'uc chrome options' and add the profile path. To find your profile path, open 'chrome://version' in your browser, copy the profile path, and paste it in the script's argument.

## Usage

1. **Input Configuration**: Fill in the name, email, website, and comment fields with the desired values.

2. **CSV Configuration**: Add the homepage links of the WordPress blogs you want to target in the 'sites.csv' file.

3. **Run Process**: Click the "Run" button to start the commenting process. The script will navigate through the specified pages of each website and post comments.

4. **Clear Fields**: Use the "Clear" button to reset all input fields for the next set of comments.

5. **Stop Process**: To stop the process, simply close the opened Chrome browser window.

## Notes

- Make sure to handle the commenting responsibly and within the guidelines of the targeted websites to avoid any issues.

- Keep an eye on the process and adjust the settings accordingly for a seamless commenting experience.

Thank you for using WordPress Blogs Comment Automation! Happy commenting!
