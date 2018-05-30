### 程序分三部分
####  一、
```python
python api/crawl_proxy.py
```
抓取代理网站的ip，并将ip过滤后存入redis,保存的形式key为'host|port',比如"101.251.232.221|3128",value为整数4

---
####  二、
```python
python api/timing_validate.py
```
将过滤后的ip进行随机定期验证，删除失效的ip

---
####  三、
```python
python manage.py
```
flask服务，通过post请求，可以获取redis中的ip