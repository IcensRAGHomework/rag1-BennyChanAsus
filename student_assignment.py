import json
import traceback

from model_configurations import get_model_configuration
from pydantic import BaseModel, Field

import re
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import PromptTemplate

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )

    class Holiday(BaseModel):
        date: str = Field(description="年份-月份-日期")
        name: str = Field(description="紀念日名稱")
    parser = JsonOutputParser(pydantic_object=Holiday)
    # parser = StrOutputParser()

    prompt = PromptTemplate(
        template="列出{year}年台灣{month}月的所有紀念日，並以JSON格式呈現於最前面，每個紀念日包含日期和名稱，例如：{{'date': '年份-月份-日期', 'name': '紀念日名稱'}}。\n{format_instructions}",
        input_variables=["year", "month"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )


    chain = prompt | llm | parser

    match = re.search(r'(\d{4})年台灣(\d{1,2})月', question)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)
        #print(year)
        #print(month)

        respond = chain.invoke({"year": year, "month": month})
        # print(respond)
        result = {"Result": respond}
    else:
        result = {"Result": []}

    # match = re.search(r'(\d{4})年台灣(\d{1,2})月', question)
    # if match:
    #     year = match.group(1)
    #     month = match.group(2).zfill(2) 
    #     #print(year)
    #     #print(month)
    #     prompt = f"列出{year}年台灣{month}月的所有紀念日，並以JSON格式呈現，每個紀念日包含日期和名稱，例如：{{'date': '年份-月份-日期', 'name': '紀念日名稱'}}。"
    #     response = llm.invoke(prompt)

    #     json_parser = JsonOutputParser()
    #     json_output = json_parser.invoke(response)
    #     print(response)
    #     result = {"Result": json_output}
    # else:
    #     result = {"Result": []}
    
    # print(result)
    return json.dumps(result, ensure_ascii=False, indent=2)
    # return " "
    
def generate_hw02(question):
    pass
    
def generate_hw03(question2, question3):
    pass
    
def generate_hw04(question):
    pass
    
def demo(question):
    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])
    
    return response

# if __name__ == "__main__":
#     # print("asd")
#     print(generate_hw01("2023年台灣10月紀念日有哪些?"))
