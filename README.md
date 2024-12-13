# Segmentation Agriculture Sentinel 2 Dataset using Segment Anything Model (SAM)

## Description
This project utilizes the Segment Anything Model (SAM) for segmentation on the Agriculture Sentinel-2 dataset. The application is built using Flask and provides a web-based interface for segmentation tasks.

## Requirements
- Python 3.9
- Conda (optional)
- Docker (optional)

## How to Run the Project

### Using Conda
1. Create a new Conda environment:
   ```bash
   conda create --name my_python_env python=3.9
   ```

2. Activate the environment:
   ```bash
   conda activate my_python_env
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application in your browser at:
   ```
   http://localhost:5000
   ```

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t flask_website .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 --name flask_app flask_website
   ```

3. Access the application in your browser at:
   ```
   http://localhost:5000
   ```

## Project Structure After Running Conda or using Docker
```
flask_website/
├── models/
│   └── sam_vit_b_01ec64.pth
├── model/
│   └── sam_model.py
├── static/
│   ├── css/
│   ├── images/
│   ├── png/
│   └── results/
├── templates/
│   ├── about-us.html
│   ├── index.html
│   ├── segmentation.html
│   ├── segmentation_results.html
│   ├── sign-in.html
│   └── sign-up.html
├── app.py
├── Dockerfile
├── README.md
└── requirements.txt
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
- [Segment Anything Model (SAM)](https://segment-anything.com/)

