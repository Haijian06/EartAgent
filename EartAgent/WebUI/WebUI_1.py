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
import os
import dashscope
from openai import OpenAI
from dashscope import MultiModalConversation
from flask import Flask, request, render_template_string
dashscope.api_key = "api_key"
app = Flask(__name__)
"""
Developers just need to modify call_with_messages themselves
"""
def call_with_messages(user_input):
    # example
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=""
    )

    completion = client.chat.completions.create(
        model="meta/llama3-70b-instruct",
        messages=[{"role": "user", "content": '你必须用简体中文回答我'+user_input}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )

    re = ''
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            re += chunk.choices[0].delta.content
    return re



"""
以下函数不需要修改
"""

HTML_TEMPLATE = '''
<!doctype html>
    <html lang="zh">
    <head>
        <meta charset="utf-8">
        <title>项目体验</title>
    </head>
    <style>
        /* 一些基本样式 */
    body {
        margin: 0;
        font-family: Arial, sans-serif;
        background-color: #222;
        color: #fff;
    }
    
    .chat-container {
        max-width: 90%;
        margin: 20px auto;
        background-color: #333;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
    }
    
    .chat-header {
        padding: 10px;
        background-color: #444;
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
    }
    
    .chat-body {
        height: 600px;
        padding: 10px;
        overflow-y: scroll;
    }
    
    .chat-input {
        display: flex;
        padding: 10px;
        background-color: #444;
        border-bottom-left-radius: 10px;
        border-bottom-right-radius: 10px;
    }
    
    .chat-input input {
        flex-grow: 1;
        padding: 5px;
        border: none;
        border-radius: 10px;
        background-color: #333;
    }
    
    .chat-input button {
        margin-left: 10px;
        padding: 5px 10px;
        background-color: #fff;
        color: #000000;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    
    /* 消息样式 */
    .chat-message {
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 10px;
        max-width: 80%;
    }
    
    .user-message {
        background-color: #333;
        align-self: flex-end;
    }
    
    .bot-message {
        background-color: #333;
        align-self: flex-start;
    }
    
    /* 加载动画 */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #fff;
        border-top-color: transparent;
        border-radius: 50%;
        animation: rotate 1s linear infinite;
    }
    .code-block {
        background-color: #444;
        padding: 10px;
        margin: 10px 0;
        border-radius: 5px;
        overflow-x: auto;
        white-space: pre-wrap;
        font-family: monospace;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    <body>
        <div class="chat-container">
            <div class="chat-header">
                <h2>EartAgent WebUI旧</h2>
            </div>
            <div class="chat-body">
                <div class="chat-messages"></div>
            </div>
            <div class="chat-input">
                <input type="text" id="userInput" placeholder="输入你的消息...">
                <input type="file" id="imageInput" accept="image/*">
                <button id="sendBtn">发送</button>
            </div>
        </div>
    
        <script>
             const chatMessages = document.querySelector('.chat-messages');
            const userInput = document.getElementById('userInput');
            const imageInput = document.getElementById('imageInput');
            const sendBtn = document.getElementById('sendBtn');
    
            sendBtn.addEventListener('click', sendMessage);
            userInput.addEventListener('keydown', (event) => {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            });
    
            function sendMessage() {
        const userMessage = userInput.value.trim();
        const imageFile = imageInput.files[0];
    
        if (userMessage || imageFile) {
            if (userMessage && imageFile) {
                // 同时处理文本和图片输入
                addMessageToChat('user', userMessage);
                userInput.value = '';
                addMessageToChat('bot', 'Loading...', true);
                processInputs(userMessage, imageFile)
                    .then(botReply => updateBotMessage(botReply))
                    .catch(error => updateBotMessage('抱歉,出现了一些问题,请稍后再试。'));
            } else if (userMessage) {
                // 只处理文本输入
                addMessageToChat('user', userMessage);
                userInput.value = '';
                addMessageToChat('bot', 'Loading...', true);
                processUserInput(userMessage)
                    .then(botReply => updateBotMessage(botReply))
                    .catch(error => updateBotMessage('抱歉,出现了一些问题,请稍后再试。'));
            } else if (imageFile) {
                // 只处理图片输入
                addMessageToChat('user', '图片上传中...');
                addMessageToChat('bot', 'Loading...', true);
                processImageUpload(imageFile, '')
                    .then(botReply => updateBotMessage(botReply))
                    .catch(error => updateBotMessage('抱歉,图片上传失败,请稍后再试。'));
            }
        }
    }
    
    
    
            function addMessageToChat(sender, message, isLoading = false) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('chat-message', `${sender}-message`);
                if (isLoading) {
                    const loadingElement = document.createElement('div');
                    loadingElement.classList.add('loading');
                    messageElement.appendChild(loadingElement);
                } else {
                    messageElement.textContent = message;
                }
                chatMessages.appendChild(messageElement);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
    
        
        function updateBotMessage(message) {
            const loadingElement = chatMessages.querySelector('.bot-message .loading');
            if (loadingElement) {
                const botMessage = loadingElement.parentNode;
                botMessage.innerHTML = ''; // 清空之前的内容
                 // 检查响应是否为图片数据
                if (message instanceof Blob) {
                    const imageElement = document.createElement('img');
                    imageElement.src = URL.createObjectURL(message);
                    botMessage.appendChild(imageElement);
                } else {
                // 提取代码部分
                const codeRegex = /<code>([\s\S]*?)<\/code>/g;
                let match;
                let lastIndex = 0;
                
                while ((match = codeRegex.exec(message)) !== null) {
                    const textBefore = message.slice(lastIndex, match.index);
                    lastIndex = match.index + match[0].length;
                    
                    // 逐字输出文本部分
                    let i = 0;
                    function typeText() {
                        if (i < textBefore.length) {
                            botMessage.innerHTML += textBefore.charAt(i);
                            i++;
                            setTimeout(typeText, 3);
                        } else {
                            // 将代码部分放在文本框中
                            const codeElement = document.createElement('div');
                            codeElement.classList.add('code-block');
                            codeElement.textContent = match[1];
                            botMessage.appendChild(codeElement);
                        }
                    }
                    setTimeout(typeText, 3);
                }
                
                // 逐字输出剩余的文本部分
                const textAfter = message.slice(lastIndex);
                let j = 0;
                function typeRemainingText() {
                    if (j < textAfter.length) {
                        botMessage.innerHTML += textAfter.charAt(j);
                        j++;
                        setTimeout(typeRemainingText, 3);
                    }
                }
                setTimeout(typeRemainingText, 3);
                }
                botMessage.classList.remove('loading');
            }
        }
        function processUserInput(input) {
                // 向后端发送请求,获取处理后的数据
                return fetch('/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `userInput=${encodeURIComponent(input)}`,
                })
                .then(response => response.text())
                .then(data => {
                    // 返回后端处理后的数据
                    return data;
                });
            }
    function processImageUpload(imageFile, sysPrompt) {
        const formData = new FormData();
        formData.append('imageFile', imageFile);
        formData.append('sysPrompt', sysPrompt);
    
        return fetch('/process_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            // 返回后端处理后的数据
            return data;
        });
    }
    
    
    function processInputs(userInput, imageFile) {
        const formData = new FormData();
        formData.append('userInput', userInput);
        formData.append('imageFile', imageFile);
        formData.append('sysPrompt', ''); // 可以根据需要设置系统提示
    
        return fetch('/process_inputs', {
            method: 'POST',
            body: formData
        })
        .then(response => response.text())
        .then(data => {
            // 返回后端处理后的数据
            return data;
        });
    }
    
        </script>
    </body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['userInput']
        processed_data = process_input(user_input)
        # 将代码部分用<code>标签包裹起来
        processed_data = processed_data.replace('```', '<code>').replace('```', '</code>')
        return processed_data
    else:
        return render_template_string(HTML_TEMPLATE)


@app.route('/process_image', methods=['POST'])
def process_image():
    image_file = request.files['imageFile']
    sys_prompt = request.form['sysPrompt']
    processed_response = process_multimodal_input(image_file, sys_prompt)
    return processed_response


@app.route('/process_inputs', methods=['POST'])
def process_inputs():
    user_input = request.form['userInput']
    image_file = request.files['imageFile']
    sys_prompt = request.form['sysPrompt']

    # 如果有用户输入文本,则将其与系统提示合并
    if user_input:
        sys_prompt = f"{user_input} {sys_prompt}"

    processed_response = process_multimodal_input(image_file, sys_prompt)
    return processed_response


def process_multimodal_input(image_file, sys_prompt):
    """
    Process the uploaded image file and system prompt, and generate a response.

    Args:
        image_file (werkzeug.datastructures.FileStorage): The uploaded image file.
        sys_prompt (str): The system prompt for the analysis.

    Returns:
        str: The generated response.
    """
    # 获取上传图片的完整路径
    image_path = os.path.join('D:/images', image_file.filename)

    # 保存上传的图片到指定路径
    image_file.save(image_path)

    # 构建本地文件路径
    local_file_path = f'file://{image_path}'

    messages = [
        {
            'role': 'system',
            'content': [{
                'text': '你是我的好助手'

            }]
        },
        {
            'role': 'user',
            'content': [
                {
                    'image': local_file_path
                },
                {
                    'text': sys_prompt
                },
            ]
        }
    ]

    response = MultiModalConversation.call(model='qwen-vl-max', messages=messages)

    if response["status_code"] == 200:
        res = response["output"]["choices"][0]["message"]["content"][0]["text"]
    else:
        raise Exception("Failed to process the input. Please check your network connection or image URL.")

    return res


# 文字处理函数
def process_input(input_text):
    """处理函数，这里简单地将输入文本"""
    return call_with_messages(input_text)


if __name__ == '__main__':
    app.run(debug=True)
