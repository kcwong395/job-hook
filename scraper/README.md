## Maintenance

### install required package

pip install -r scraper/requirements.txt

### run all test cases

python -m unittest discover -s scraper/tests -p "test_*.py" -v

### Update requirements.txt

pip3 freeze > backend/requirements.txt

### Build docker image with dockerfile

sudo docker build -t jh-scraper:v1.0 .