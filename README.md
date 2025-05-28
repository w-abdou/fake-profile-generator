
# Fake Profile Generator

**Fake Profile Generator** is a Python-based tool designed to create synthetic user profiles for testing, development, and educational purposes. It generates realistic personal data, including names, addresses, contact information, and more, without compromising real user privacy.

## 📦 Features

* **Realistic Data Generation**: Produces plausible user information such as names, emails, phone numbers, and addresses.
* **Customizable Output**: Allows users to specify the number of profiles to generate.
* **Data Export**: Supports exporting generated profiles to formats like CSV or JSON for easy integration.
* **Modular Design**: Structured codebase for easy maintenance and extension.

## 🛠️ Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/w-abdou/fake-profile-generator.git
   cd fake-profile-generator
   ```

2. **Install Dependencies**:

   Ensure you have Python 3 installed. Then, install required packages:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: If `requirements.txt` is not present, manually install necessary packages such as `Faker`:*

   ```bash
   pip install Faker
   ```

## 🚀 Usage

Run the `fake_profile.py` script to generate fake profiles:

```bash
python fake_profile.py
```

By default, the script may generate a predefined number of profiles. To customize:

```bash
python fake_profile.py --count 10 --output profiles.csv
```

**Arguments**:

* `--count`: Number of profiles to generate (default: 1).
* `--output`: Filename to save the generated profiles (supports `.csv` and `.json`).

## 📁 Project Structure

```
fake-profile-generator/
├── fake_profile.py              # Main script to generate profiles
├── requirements.txt             # Python dependencies
├── Fake-Profile-Generator-Presentation.pdf  # Project presentation
├── Fake_Profile_Report.pdf      # Detailed project report
└── README.md                    # Project documentation
```

## 📄 Sample Output

An example of a generated profile:

```json
{
  "name": "John Doe",
  "email": "johndoe@example.com",
  "phone": "+1-202-555-0173",
  "address": "123 Main St, Anytown, USA"
}
```

## 🎓 Educational Resources

The repository includes a presentation and a detailed report:

* [Fake-Profile-Generator-Presentation.pdf](Fake-Profile-Generator-Presentation.pdf)
* [Fake\_Profile\_Report.pdf](Fake_Profile_Report.pdf)

These documents provide insights into the project's objectives, design decisions, and potential applications.

