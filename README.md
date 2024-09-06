# HR Base

**HR Base** is a job recruitment platform that connects job seekers and employers. Employers can post job vacancies, while job seekers can apply for these positions seamlessly. The application aims to streamline the hiring process and provide an efficient platform for both companies and candidates.

## Features

### For Job Seekers
- **Browse Jobs**: View and search through a wide range of job postings from various companies.
- **Apply for Jobs**: Apply directly to job vacancies with your profile and resume.
- **Manage Applications**: Track the status of your applications in one place.
- **Profile Creation**: Build a detailed profile with skills and experience for better job matches.

### For Employers
- **Post Vacancies**: Create and manage job postings, including job descriptions, requirements, and deadlines.
- **Manage Applications**: Review and manage job applications from job seekers.
- **Company Profile**: Create a company profile to attract potential candidates.
- **Collaborate**: Invite colleagues or HR team members to manage job postings and applications.

## Technology Stack
- **Database**: PostgreSQL
- **API**: Django REST Framework (DRF)

## Setup and Installation

### Prerequisites
- Python 3.x
- PostgreSQL 13.x
- Django 4.x
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AlphaCodz/hrbase.git
   cd hrbas
   cd project
   ```

2. **Create a Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up PostgreSQL**
   - Create a PostgreSQL database for the project.
   - Update the `DATABASES` settings in the `settings.py` file with your PostgreSQL credentials.

5. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create a Superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

8. **Access the Application**
   - Open a browser and navigate to `http://localhost:8000/` to view the HR Base platform.
   - Admin dashboard: `http://localhost:8000/admin/`

## API Endpoints

HR Base offers a RESTful API for integrating with third-party services.

### Sample Endpoints:
- **GET** `/api/jobs/` - Retrieve all job listings
- **POST** `/base_url/api/jobs/{job_id}/apply` - Apply for a job
- **GET** `/api/companies/` - Retrieve list of companies

For more information, refer to the detailed [API documentation](link_to_docs).

## Contribution Guide

We welcome contributions from the community to improve HR Base. Here's how you can contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## License

HR Base is licensed under the MIT License. See [LICENSE](./LICENSE) for more details.
