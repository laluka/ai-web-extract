# ai-param-extract

## Way 1

```bash
mise install
pip instal -r requirements.txt
ollama serve
python php_endpoint_analyzer.py src deepseek-coder:33b
```

# Way 2

```bash
ollama serve
go install github.com/danielmiessler/fabric@latest
fabric --setup # Ollama + deepseek-coder:33b
mkdir -pv ~/.config/fabric/patterns/extract_web_inputs/
cp extract_web_inputs-system.md ~/.config/fabric/patterns/extract_web_inputs/system.md
 find src -type f | xargs cat | fabric --pattern extract_web_inputs
```

---

# Result 1

```
I'm an AI language model and I don't have the ability to execute PHP code or any other programming languages, nor can I analyze the structure of a web application. However, I can help you understand how to parse this specific PHP script based on your request.

Here is how you would do it:

1. The main class and its method `index()` are not defined in the given code, but they might be present in another part of the project that we cannot see here. Thus, I can't extract details about them at this point.

2. For the conditional block, we know it is checking whether the `action` is set and equals to 'echo'. It then checks if a `message` parameter is provided and echoes it back. If not, it will respond with "No message provided".

Here's how you can represent this in JSON:

``json
{
    "endpoints": [
        {
            "path": "/",
            "methods": ["GET"],
            "input_parameters": ["action", "message"],
            "description": "Echoes back the message or responds with 'No message provided' if no message parameter is provided"
        }
    ]
}
``

3. For path routing, it checks for two specific paths: "/" and "/phpinfo". The first one instantiates a `Main` object and calls its index method. The second one runs the phpinfo() function.

Here's how you can represent this in JSON:
``json
{
    "endpoints": [
        {
            "path": "/",
            "methods": ["GET"],
            "input_parameters": [],
            "description": "Instantiates a Main object and calls its index method"
        },
        {
            "path": "/phpinfo",
            "methods": ["GET"],
            "input_parameters": [],
            "description": "Runs the phpinfo function"
        }
    ]
}
``
Please note that I did not include any input headers since no specific headers are mentioned in this script. The actual headers could be extracted from the `$_SERVER['HTTP_*']` superglobals or from the PHP's `getallheaders()` function, but they are not included in the given script and hence left out for brevity.

Again, it is important to note that this kind of analysis requires a context or full access to the codebase as real-world applications often have complex routing logic with various conditional statements and other parameters.The provided PHP code snippet doesn't include any HTTP methods, input parameters or headers as those are usually passed through GET and POST requests in a traditional web application. However, the script does include some security related elements such as checking if a file exists before attempting to download it.

To extract all of the above information from your PHP code, you would need to have access to the full application or at least the routes configuration where these details are usually defined.

Here is an example of how this might look like:

``json
{
    "endpoints": [
        {
            "path": "/sub",
            "methods": ["GET"],
            "input_parameters": [],
            "input_headers": [],
            "description": "Sub DIR & Sub FILE",
            "curl_request": ""
        },
        {
            "path": "/download",
            "methods": ["GET"],
            "input_parameters": ["file"],
            "input_headers": [],
            "description": "Download File",
            "curl_request": "curl -X GET 'https://example.com/download?file=test.txt'"
        }
    ]
}
``
This is a basic example and may not accurately represent the actual security measures or specific requirements of your application, so it's recommended to look at your application's routes configuration or source code for more accurate information.

Please note that this does not provide you with an exhaustive list of all potential routes, methods, input parameters or headers as this would require inspecting the entirety of your project and is beyond a simple text analysis tool like me.
```

# Result 2

```json
{
   "apiCalls": [
       {
           "method": "GET",
           "url": "/phpinfo",
           "headers": {},
           "parameters": {}
       },
       {
           "method": "GET",
           "url": "/sub",
           "headers": {},
           "parameters": {}
       },
       {
           "method": "POST",
           "url": "/download",
           "headers": {},
           "body": {"file": "sample.txt"}
       }
   ]
}
```