# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request, render_template_string, jsonify
from openai import OpenAI

app = Flask(__name__)
"""
用户只需要自行修改call_with_messages即可
"""


def call_with_messages(query):
    # example
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="your_api_key"
    )
    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[{"role": "user", "content": '你必须用简体中文回复我！' + query}],
        temperature=0.7,
        top_p=1,
        max_tokens=1024,
        stream=True
    )
    result = 'llama-3:'
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content
    return result


"""
以下函数不需要修改
"""
# 将前端HTML代码作为模板字符串
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini</title>
</head>
<style>
    /* ... (rest of the CSS remains the same) */
            body {
        background-color: #2b2b2b;
        color: #fff;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex; /* add this to make the body a flex container */
        flex-direction: column; /* add this to make the body a column layout */
        height: 100vh; /* add this to make the body take up the full height of the viewport */
    }

    h1 {
        text-align: center;
        margin-top: 50px;
    }

    .input-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: auto; /* add this to push the input container to the bottom */
        margin-bottom: 20px; /* add this to create some space between the input container and the bottom bar */
    }

    input[type="text"] {
        width: 400px;
        height: 40px;
        border: none;
        border-radius: 5px;
        padding: 0 10px;
        font-size: 16px;
        background-color: #464646;
        color: #cccccc;
        transition: box-shadow 0.3s ease;
    }

    input[type="text"]:focus {
        box-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
    }

    button {
        width: 100px;
        height: 40px;
        border: none;
        border-radius: 5px;
        margin-left: 10px;
        font-size: 16px;
        color: #fff;
        background-color: #4c4c4c;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        transition: background-color 0.3s ease, transform 0.3s ease;
        cursor: pointer;
    }

    button:hover {
        background-color: #666;
        transform: translateY(-2px);
    }

    .bottom-bar {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: 20px; /* add this to create some space between the bottom bar and the end of the page */
    }

    .bottom-bar p {
        margin: 0;
        font-size: 14px;
        color: #999;
    }

    @media (max-width: 600px) {
        .input-container {
            flex-direction: column;
            align-items: stretch;
        }

        input[type="text"] {
            width: 80%;
            margin-bottom: 10px;
        }

        button {
            width: 40%;
            margin-left: 0;
            margin-top: 10px;
        }
    }
    #searchBtn {
        position: relative; /* add this to make the button a positioning context */
    }

    #searchBtn img {
        position: absolute; /* add this to position the image on top of the button */
        top: -55px; /* adjust the top position to 5px above the button */
        left: 50%; /* center the image horizontally */
        transform: translateX(-50%); /* center the image horizontally */
        width: 50px;
        height: 50px;
        border-radius: 5px;
        object-fit: cover; /* add this to scale the image while maintaining aspect ratio */
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3); /* add a subtle shadow effect */
        transition: transform 0.3s ease; /* add a transition effect for the floating effect */
    }

    #search-display, #result-display {
    margin-left: 20%;
    padding-left: 20px;
    margin-top: 1.25rem;
}
</style>
<body>
    <h1>EartAgent WebUI</h1>
    <div id="search-display"></div>
    <div id="result-display"></div>
    <div class="input-container">
        <input type="text" id="searchInput" placeholder="在这里输入你的问题" onkeydown="handleKeydown(event)">
        <input type="file" id="imageInput" accept="image/*" style="display: none;">
        <button id="searchBtn" style="background-image: none; background-color: #4c4c4c;">Load</button>
        <button id="voiceBtn">语音输入</button>
    </div>
    <div class="bottom-bar">
        <p>Copyright &copy; 2024 EartAgent WebUI. All rights reserved.</p>
    </div>

    <script>
        const searchInput = document.getElementById('searchInput');
        const searchDisplay = document.getElementById('search-display');
        const resultDisplay = document.getElementById('result-display');
        const searchBtn = document.getElementById('searchBtn');
        const imageInput = document.getElementById('imageInput');
        const voiceBtn = document.getElementById('voiceBtn');

        // Update the search display only when the user presses Enter
        function handleKeydown(event) {
            if (event.key === 'Enter') {
                const query = searchInput.value.trim();
                searchDisplay.innerText = `You typed: ${query}`;
                performSearch(query);
                searchInput.value = ''; // 清空 searchInput 的内容
            }
        }       

        imageInput.addEventListener('change', (e) => {
            const file = imageInput.files[0];
            const reader = new FileReader();
            reader.onload = (event) => {
                const imageData = event.target.result;
                const img = document.createElement('img');
                img.src = imageData;
                searchBtn.innerHTML = '';
                searchBtn.appendChild(img);
            };
            reader.readAsDataURL(file);
        });

        searchBtn.addEventListener('click', () => {
            const query = searchInput.value.trim();
            if (query) {
                searchDisplay.innerText = `You typed: ${query}`;
                performSearch(query);
            }
        });

        voiceBtn.addEventListener('click', () => {
            console.log('开始语音输入');
        });

        searchBtn.addEventListener('click', () => {
            imageInput.click();
        });

        function performSearch(query) {
            fetch('http://127.0.0.1:5000/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: query })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultDisplay.innerText = data.error;
                } else {
                    resultDisplay.innerText = data.result;
                }
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
'''


# 路由处理函数
@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)


# 处理查询的路由
@app.route('/query', methods=['POST'])
def query():
    try:
        user_input = request.json.get('query')
        print(user_input)
        if user_input:
            result = call_with_messages(user_input)
            print(result)
            return jsonify({'result': result})
        else:
            return jsonify({'error': 'No query provided'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
