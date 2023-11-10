from flask import Flask, render_template_string, request
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)

def crawl_and_get_tables(id, pw):
    webdriver_options = webdriver.ChromeOptions()
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--disable-dev-shm-usage')
    webdriver_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36')

    driver = webdriver.Chrome(options=webdriver_options)
    driver.implicitly_wait(1)

    # 로그인 페이지에서 로그인하기
    login_url = 'https://account.everytime.kr/login'
    driver.get(login_url)
    driver.find_element(By.NAME, 'id').send_keys(id)  # ID 입력
    driver.find_element(By.NAME, 'password').send_keys(pw)  # PW 입력
    driver.find_element(By.XPATH, '//input[@value="에브리타임 로그인"]').click()

    driver.implicitly_wait(10)
    driver.get('https://everytime.kr/')
    driver.get_screenshot_as_file('capture1.png')

    # Assuming the timetable is on a new page, navigate to that page
    timetable_url = 'https://everytime.kr/timetable'
    driver.get(timetable_url)
    driver.implicitly_wait(5)
    driver.get_screenshot_as_file('capture2.png')  # capture 2를 통해 시간표 확인 가능
    table_elements = driver.find_elements(By.TAG_NAME, 'table')

    table_html_list = [table.get_attribute('outerHTML') for table in table_elements]  # 테이블의 각 값을 list에 저장
    driver.quit()

    return table_html_list

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # If the form is submitted, get the ID and password from the form
        id = request.form['id']
        pw = request.form['password']
        
        # Get the HTML codes of tables using the provided ID and password
        table_html_list = crawl_and_get_tables(id, pw)
    else:
        # If it's a GET request, initialize the HTML list with an empty list
        table_html_list = []

    all_tables_html = "\n".join(table_html_list)  # 하나의 문자열로 연결

    # HTML template to display the tables
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crawled Tables</title>
    </head>
    <body>
        <form method="post" action="/">
            <label for="id">ID:</label>
            <input type="text" id="id" name="id" required>
            <br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <br>
            <input type="submit" value="Submit">
        </form>
        {{ tables_html|safe }}
    </body> 
    </html>
    """

    return render_template_string(html_template, tables_html=all_tables_html)

if __name__ == '__main__':
    # Run the Flask app
    app.run(debug=True)
