# Vehicle Data Pipeline Project

## 📌 Project Overview
This project aims to build a fully automated data pipeline using MongoDB, Python, and AWS services. It includes data ingestion, validation, transformation, model training, and deployment using CI/CD on AWS EC2.

---

## 🚀 Project Setup
### 1️⃣ Create Project Template
Run the following command to initialize the project structure:
```bash
python template.py
```

### 2️⃣ Configure Local Package Imports
- Modify `setup.py` and `pyproject.toml` to enable local package imports.
- More details are available in `crashcourse.txt`.

### 3️⃣ Set Up Virtual Environment
```bash
conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt
```
Verify installation:
```bash
pip list
```

---

## 🗄️ MongoDB Setup
### 4️⃣ Set Up MongoDB Atlas
1. Sign up on [MongoDB Atlas](https://www.mongodb.com/atlas) and create a new project.
2. Click on **Create a Cluster** → Choose **M0 Free Tier** → Deploy.
3. Create a **Database User** with a username and password.
4. In **Network Access**, add IP address `0.0.0.0/0` for global access.
5. Get the **MongoDB Connection String** (Driver: Python 3.6+).
6. Save the connection string (replace `<password>` with your actual password).

### 5️⃣ Push Data to MongoDB
1. Create a `notebook` folder and add `mongoDB_demo.ipynb`.
2. Load the dataset and push it to MongoDB.
3. Verify data in **MongoDB Atlas** → Database → Browse Collection.

---

## 📝 Logging, Exception Handling & Notebooks
### 6️⃣ Implement Logging & Exception Handling
- Create `logger.py` and `exception.py`, test them in `demo.py`.
- Add **EDA & Feature Engineering** notebooks.

---

## 📥 Data Ingestion
### 7️⃣ Implement Data Ingestion
- Define constants in `constants/__init__.py`.
- Implement MongoDB connection in `configuration/mongo_db_connections.py`.
- Add data retrieval logic in `data_access/proj1_data.py`.
- Define entities in `entity/config_entity.py` and `entity/artifact_entity.py`.
- Implement `components/data_ingestion.py`.
- Run `demo.py` to test.

### 8️⃣ Configure MongoDB Connection URL
```bash
export MONGODB_URL="mongodb+srv://<username>:<password>@cluster.mongodb.net/"
echo $MONGODB_URL
```
(For Windows, set environment variables manually.)

---

## 🏗️ Data Validation, Transformation & Model Training
### 9️⃣ Data Validation
- Complete `utils/main_utils.py` and `config/schema.yaml`.
- Implement validation as done in **Data Ingestion**.

### 🔟 Data Transformation
- Implement transformation logic.
- Update `estimator.py` in `entity/`.

### 1️⃣1️⃣ Model Training
- Implement training logic in `estimator.py`.
- Train and evaluate the model.

---

## ☁️ AWS Setup
### 1️⃣2️⃣ AWS IAM & S3 Configuration
- Create an IAM user with `AdministratorAccess`.
- Generate access keys and set environment variables:
  ```bash
  export AWS_ACCESS_KEY_ID="<your-access-key>"
  export AWS_SECRET_ACCESS_KEY="<your-secret-key>"
  ```
- Create an S3 bucket `my-model-mlopsproj`.
- Implement `aws_connection.py` for S3 interaction.

---

## 📊 Model Evaluation & Deployment
### 1️⃣3️⃣ Model Evaluation & Pusher
- Implement Model Evaluation & Pusher components.

### 1️⃣4️⃣ Prediction Pipeline & Web App
- Implement `app.py`.
- Add `static` and `templates` directories.

---

## 🔄 CI/CD with Docker & GitHub Actions
### 1️⃣5️⃣ Docker Setup
- Create `Dockerfile` and `.dockerignore`.

### 1️⃣6️⃣ GitHub Actions for CI/CD
- Create `.github/workflows/aws.yaml`.
- Set up **GitHub Secrets**:
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `AWS_DEFAULT_REGION`
  - `ECR_REPO`

### 1️⃣7️⃣ Deploy to AWS EC2
- Launch an Ubuntu EC2 instance (T2 Medium, 30GB storage).
- Install Docker:
  ```bash
  curl -fsSL https://get.docker.com -o get-docker.sh
  sudo sh get-docker.sh
  ```
- Set up a **self-hosted runner** on GitHub.

### 1️⃣8️⃣ Expose EC2 Port for App
- Edit **Inbound Rules**:
  - Type: Custom TCP
  - Port: `5080`
  - Source: `0.0.0.0/0`
- Access the app at `http://<EC2-PUBLIC-IP>:5080`.

---

## ✅ Final Steps
- CI/CD pipeline triggers on `git push`.
- Web app is accessible at `/training` route for model training.
- Validate predictions via `app.py`.

---

## 🎯 Conclusion
This project provides an end-to-end data pipeline from data ingestion to model deployment using MongoDB, AWS, and CI/CD. 🚀

