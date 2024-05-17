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

import abc
from dataclasses import dataclass
from http import HTTPStatus
from urllib.parse import urlparse, unquote
from pathlib import PurePosixPath

import dashscope
import requests
from dashscope import ImageSynthesis


@dataclass
class TAgentConfig:
    """
    Agent configuration information
    """
    name: str


class ImageAgent(abc.ABC):
    """
    Image generation proxy base class
    """

    def __init__(self, config: TAgentConfig, api_key: str):
        self.config = config
        self.api_key = api_key

    @abc.abstractmethod
    def generate_image(self, prompt: str, **kwargs) -> list:

        raise NotImplementedError


class WanxAgent(ImageAgent):

    def generate_image(self, prompt: str):
        dashscope.api_key = self.api_key
        rsp = ImageSynthesis.call(model=ImageSynthesis.Models.wanx_v1,
                                  prompt=prompt,
                                  n=4,
                                  size='1024*1024')
        if rsp.status_code == HTTPStatus.OK:

            # save file to current directory
            for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open('./%s' % file_name, 'wb+') as f:
                    f.write(requests.get(result.url).content)
                    print(f"Image saved as {file_name}")

        else:
            print('Failed, status_code: %s, code: %s, message: %s' %
                  (rsp.status_code, rsp.code, rsp.message))






