# Cloudflare DNS Wizard

![Cloudflare Logo](https://www.cloudflare.com/img/logo-cloudflare-dark.svg)

The **Cloudflare DNS Wizard** is a Python script that empowers you to interact with Cloudflare's DNS service using their powerful API. With this tool, you can effortlessly manage DNS records, view zone information, and access account details.

## Features

- **Fetch DNS Records:** Retrieve DNS records for your Cloudflare zone.
- **Display Zone Information:** Get insights into your Cloudflare zone.
- **Display Account Information:** View your Cloudflare account details.
- **Update DNS Records:** Modify DNS records of a specific type with new content.

## Prerequisites

Before you get started, make sure you have the following prerequisites:

- **Python 3.x:** You need Python 3.x installed on your machine. You can download it from [Python's official website](https://www.python.org/downloads/).

- **Required Python Packages:** Install the required Python packages listed in `requirements.txt` using the following command:

    ```bash
    pip install -r requirements.txt
    ```

- **Python Virtual Environment (venv):** We recommend setting up a virtual environment to keep your project dependencies isolated. You can create and activate a virtual environment using the following commands:

    ```bash
    # Create a virtual environment (replace 'venv' with your preferred name)
    python -m venv venv

    # Activate the virtual environment (Windows)
    .\venv\Scripts\activate

    # Activate the virtual environment (macOS and Linux)
    source venv/bin/activate
    ```

    Once activated, your terminal prompt will change to indicate that you are now working within the virtual environment.

## Usage

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/cloudflare-dns-wizard.git
    ```

2. **Configure Your Cloudflare API Details:**

    - Create a `config.txt` file and input your Cloudflare email, API token, Zone ID, and Account ID as specified in the script.

3. **Run the Script:**

    ```bash
    python cloudflare_dns_wizard.py
    ```

4. **Follow the On-Screen Instructions:**

    The script will guide you through various actions to manage your DNS records and Cloudflare account.

## Configuration

You have the flexibility to customize the script by modifying the code to suit your specific needs. For instance, you can adjust API endpoint URLs or expand the script's functionality to include additional features.

## License

This project is licensed under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file.

## Acknowledgments

- Special thanks to Cloudflare for providing a robust API that powers this tool.

![Cloudflare API Logo](https://www.cloudflare.com/img/logo-api-gray.svg)

---

This Cloudflare DNS Wizard simplifies the management of your DNS records and empowers you to harness the full potential of Cloudflare's DNS service. It's a valuable tool for professionals in the cybersecurity field and anyone looking to optimize their DNS management.

For inquiries and support, feel free to reach out to me on GitHub: [VSM97 GitHub Profile](https://github.com/VSM97)

Thank you for considering this tool, and I look forward to your contributions and feedback.
