**README.md - Titan Patient Management System (Python Django)**

## Titan Patient Management System

Titan is a powerful Patient Management System developed using the Django framework in Python. This system efficiently stores, manages, and analyzes patient data, providing a seamless user experience. It includes features for patient data storage, display, statistical analysis, Google Sync automation for data synchronization with Google Sheets, and a comprehensive activity log that tracks recent activities, including field edits.

### Features:

1. **Patient Data Storage:**
   - Easily manage patient records with Django's robust database backend.
   - Capture comprehensive patient information, including personal details, medical history, and contact information.

2. **Patient Data Display:**
   - Utilize Django templates and views to create a user-friendly interface for viewing and searching patient records.
   - Retrieve and display patient information effortlessly.

3. **Patient Data Stats:**
   - Leverage Django's ORM for generating statistical insights and reports based on patient data readings.
   - Track trends and analyze key metrics to support informed decision-making.

4. **Google Sync Automation:**
   - Integrate seamlessly with Google Sheets using Django commands for efficient data synchronization.
   - Automate the syncing process to keep patient data up-to-date between Titan and Google Sheets.

5. **Activity Log:**
   - Maintain a detailed activity log that records recent interactions and updates for each patient.
   - Track changes, including who edited which patient field, ensuring transparency and accountability.

### Getting Started:

Follow these steps to set up and deploy Titan Patient Management System:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/Titan.git
   ```

2. **Install Dependencies:**
   ```bash
   cd titan
   pip install -r requirements.txt
   ```

3. **Configure Google Sync:**
   - Obtain Google Sheets API credentials and configure them in the Django project.
   - Set up the necessary permissions for Google Sync automation.

4. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

### Usage:

- **Adding Patient Data:**
  - Access the Django admin interface or implement custom forms to add new patient records.

- **Viewing Patient Data:**
  - Utilize Django views and templates to create an intuitive interface for viewing and searching patient records.

- **Analyzing Patient Data Stats:**
  - Leverage Django's ORM and custom queries to analyze trends and metrics based on patient data readings.

- **Activity Log:**
  - Explore the activity log to track recent activities, including field edits, providing transparency and accountability.

- **Google Sync Automation:**
  - Execute the Django management command to automate the synchronization of patient data with Google Sheets.
