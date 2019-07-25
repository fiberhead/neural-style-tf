# Docker for API

You can build and run the docker using the following process:

Cloning
```console
git clone https://github.com/jqueguiner/neural-style-tf neural-style
```

Building Docker
```console
cd neural-style && docker build -t neural-style -f Dockerfile .
```

Running Docker
```console
echo "http://$(curl ifconfig.io):5000" && docker run -p 5000:5000 -d neural-style
```

Calling the API
```console
curl -X POST "http://MY_SUPER_API_IP:5000/process" -H "accept: image/*" -H "Content-Type: application/json" -d '{"url":"https://i.ibb.co/BGHyHjc/input.png"}' --output styled_image.png
```
