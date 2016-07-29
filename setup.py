from setuptools import setup

setup(
  name='navernews',
  packages=['navernews'],
  version='0.0.1',
  description='A simple Python module to crawl Naver News. See https://github.com/q1c/navernews for more information.',
  author='Kyuwon Choi',
  author_email='kyuwon.choi11@gmail.com',
  url='https://github.com/q1c/navernews',
  keywords=['naver', 'news', 'scraping'],
  install_requires=['requests', 'lxml']
  # install_requires=['Js2Py==0.37', 'requests >= 2.0.0']
)
