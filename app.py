from flask import Flask, render_template, request
from selenium import webdriver
from urllib.parse import urlparse
app = Flask(__name__)

@app.route('/')
def challenge():
    return render_template('challenge.html')

def is_valid_url(url):
    try:
        parsed_url = urlparse(url)
        # Ensure URL has a valid scheme (http, https) and a network location (domain).
        return all([parsed_url.scheme in ['http', 'https'], parsed_url.netloc])
    except ValueError:
        return False  # ValueError is raised if the URL is malformed.

@app.route('/admin-bot/', methods=['POST', 'GET'])
def admin():
    url = request.form.get('url', None)
    if not url:
        return render_template('bot.html')
    elif not is_valid_url(url):
        return render_template('bot.html', error="Invalid URL")

    # get the domain of this hosted instance
    host_domain = urlparse(request.host_url).hostname
    # to prevent a domain mismatch exception from lovely selenium
    domain = urlparse(url).hostname

    # check if the provided URL's domain matches the server's domain
    if domain != host_domain:
        return render_template('bot.html', error="I'm sorry, you can only ask the Admin bot to submit requests to the fanpage.")

    cookie = { 'name': 'flag', 'value': 'EKO{XXXXXXXXXXYYYYY}', 'domain': domain }

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)
    # There needs to be an inital request for the domain we're trying to set a cookie for
    driver.get(url)
    driver.add_cookie(cookie)
    # And finally now that we have the cookie set, re-request this.
    driver.get(url)

    # Give selenium time to process the page and execute any outgoing requests via JavaScript
    time.sleep(5)

    # Let's be clean and quit the driver ourselves.
    driver.quit()
    return render_template('bot.html', url=url)

if __name__ == "__main__":
    app.run()
    #app.run(debug=True)
