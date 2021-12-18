# SI 650 Project Frontend Deployment Tips

I've tried 2 deployment method, and successfully deployed on pythonanywhere: https://tcy1999.pythonanywhere.com/.

## Deployment on pythonanywhere

1. The space is limited, so it's better to install a cpu-only version of pytorch if possible (See: https://stackoverflow.com/questions/51730880/where-do-i-get-a-cpu-only-version-of-pytorch)
2. As I'm using a free account, it seems that when using sentence-transformers, the host is not [whitelisted](https://www.pythonanywhere.com/whitelist/) for pythonanywhere, so I have to save the pretrained model locally on my laptop, and upload to pythonanywhere.

## Deployment on heroku

1. The space is again limited, and I tried to install cpu-only version of pytorch again. However, this time the website is deployed, but run into memory problem during running time.
2. Heroku also have time limit on a request, where a request must receive a response within 30 seconds. This issue could be solved by using websocket.
3. Remember to include the `requirements.txt`, `Procfile` and `runtime.txt`, and you could choose to deploy from a Github repo.